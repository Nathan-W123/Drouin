"""Minimal, explicit readers/writers for Pickett's SPFIT/SPCAT files and runners.

Formats follow spinv.pdf ("Format of the .lin / .par / .int / .cat File"):
  * .lin : 12 quantum numbers in I3 (upper state first), FREQ ERR [WT] free-form from column 37.
           Consecutive lines with identical FREQ and ERR are treated by SPFIT as a blend.
  * .par : title / NPAR NLINE NITR NXPAR THRESH ERRTST FRAC CAL / option line(s) /
           IDPAR PAR ERPAR /LABEL.  ERPAR is an a-priori uncertainty (a constraint);
           1e36 means unconstrained, ~1e-37 means fixed.
  * .cat : F13.4 F8.4 F8.4 I2 F10.4 I3 I7 I4 12I2.

With a single vibronic state (NVIB=1) the vibrational quantum number is omitted, so each
state is labelled by (N, Ka, Kc) and a transition by a 6-tuple (N', Ka', Kc', N", Ka", Kc").
"""
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_BIN = os.path.join(ROOT, "external", "pickett_src", "Pickett")
SPFIT = os.environ.get("PYCKETT_SPFIT_PATH", os.path.join(_BIN, "spfit"))
SPCAT = os.environ.get("PYCKETT_SPCAT_PATH", os.path.join(_BIN, "spcat"))

FIXED_ERR = 1e-37
FREE_ERR = 1e36
MHZ_PER_CM = 29979.2458


@dataclass
class Param:
    idpar: int
    value: float
    prior: float = FREE_ERR  # a-priori uncertainty passed to SPFIT
    label: str = ""

    @property
    def free(self):
        return self.prior > 1e-30


@dataclass
class ParFile:
    title: str
    option_lines: list
    params: list = field(default_factory=list)
    nitr: int = 10
    errtst: float = 1e6  # we do our own outlier handling
    frac: float = 1.0  # parameter errors are NOT rescaled by the rms

    def copy(self):
        return ParFile(self.title, list(self.option_lines),
                       [Param(p.idpar, p.value, p.prior, p.label) for p in self.params],
                       self.nitr, self.errtst, self.frac)

    def get(self, idpar):
        for p in self.params:
            if p.idpar == idpar:
                return p
        return None

    def write(self, path, nline=9999):
        out = [self.title[:60],
               f"{len(self.params):5d} {nline:5d} {self.nitr:4d}    0  0.0000E+000 "
               f"{self.errtst:12.4E} {self.frac:12.4E} 1.0000000000"]
        out += self.option_lines
        for p in self.params:
            out.append(f"{p.idpar:>16d} {p.value: .15E} {p.prior:.8E} /{p.label}")
        with open(path, "w") as f:
            f.write("\n".join(out) + "\n")


def read_par(path, n_option_lines):
    """Read parameters (not the correlation block) of a .par/.var file."""
    L = open(path).read().splitlines()
    title, opts = L[0], L[2:2 + n_option_lines]
    params = []
    npar = int(L[1].split()[0])
    for line in L[2 + n_option_lines:2 + n_option_lines + npar]:
        body, _, label = line.partition("/")
        t = body.split()
        params.append(Param(int(t[0]), float(t[1].replace("D", "E")),
                            float(t[2].replace("D", "E")), label.strip()))
    return ParFile(title, opts, params)


def write_lin(path, rows):
    """rows: list of dicts with keys up (3-tuple), lo (3-tuple), freq, err, wt (optional).
    Rows that form a blend must be adjacent and carry identical freq/err."""
    out = []
    for r in rows:
        qn = "".join(f"{q:3d}" for q in tuple(r["up"]) + tuple(r["lo"]))
        wt = r.get("wt")
        s = f"{qn:<36s}{r['freq']:18.6f} {r['err']:12.6f}"
        if wt is not None:
            s += f" {wt:8.4f}"
        out.append(s)
    with open(path, "w") as f:
        f.write("\n".join(out) + "\n")


def write_int(path, title, tag, qrot, fend, fmax_ghz, dipoles, str0=-30.0, str1=-30.0, temp=300.0):
    with open(path, "w") as f:
        f.write(f"{title}\n0 {tag} {qrot} 0 {fend} {str0} {str1} {fmax_ghz} {temp}\n")
        for idip, mu in dipoles:
            f.write(f" {idip} {mu}\n")


def _run(exe, workdir, args, timeout=600):
    p = subprocess.run([exe] + args, cwd=workdir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       timeout=timeout, text=True, errors="replace")
    return p.stdout


# ---------------------------------------------------------------- .cat
def _qn(s):
    """Decode an I2 quantum-number field, including the letter codes for |q|>=100 or q<=-10."""
    s = s.strip()
    if not s:
        return 0
    c = s[0]
    if c.isalpha():
        if c.isupper():
            return 100 + (ord(c) - ord("A")) * 10 + int(s[1])
        return -(10 + (ord(c) - ord("a")) * 10 + int(s[1]))
    return int(s)


@dataclass
class Catalog:
    freq: np.ndarray
    err: np.ndarray
    lgint: np.ndarray
    elo: np.ndarray
    up: np.ndarray  # (n, nqn)
    lo: np.ndarray

    def keys(self):
        return [tuple(int(x) for x in u[:3]) + tuple(int(x) for x in l[:3]) for u, l in zip(self.up, self.lo)]

    def __len__(self):
        return len(self.freq)


def read_cat(path, vib=None):
    """Parse a .cat file. If vib is given and the format carries a v quantum number (4th),
    keep only transitions with v'=v"=vib."""
    fr, er, li, el, U, Lo = [], [], [], [], [], []
    for line in open(path):
        if len(line) < 60:
            continue
        try:
            nqn = int(line[51:55]) % 10
            q = [_qn(line[55 + 2 * i:57 + 2 * i]) for i in range(12)]
            float(line[0:13]), float(line[13:21]), float(line[21:29]), float(line[31:41])
        except ValueError:  # overflowing fields (absurd parameter values) -- skip the line
            continue
        up, lo = q[:nqn], q[6:6 + nqn]
        if vib is not None and nqn >= 4 and not (up[3] == vib and lo[3] == vib):
            continue
        fr.append(float(line[0:13])); er.append(float(line[13:21])); li.append(float(line[21:29]))
        el.append(float(line[31:41])); U.append(up[:3]); Lo.append(lo[:3])
    return Catalog(np.array(fr), np.array(er), np.array(li), np.array(el),
                   np.array(U, dtype=int).reshape(-1, 3), np.array(Lo, dtype=int).reshape(-1, 3))


def spcat_var(var_text: str, int_text: str):
    """Run SPCAT on an SPFIT posterior .var (uncertainties propagated by SPCAT with correlations)."""
    d = tempfile.mkdtemp(prefix="spcat_")
    try:
        with open(os.path.join(d, "x.var"), "w") as f:
            f.write(var_text)
        with open(os.path.join(d, "x.int"), "w") as f:
            f.write(int_text)
        _run(SPCAT, d, ["x.var", "x.int"])
        return read_cat(os.path.join(d, "x.cat"))
    finally:
        shutil.rmtree(d, ignore_errors=True)


def spcat(par: ParFile, int_text: str, workdir=None):
    """Run SPCAT on a parameter set (written as a .var with zero errors) and return the Catalog.
    int_text is the full content of the .int file."""
    own = workdir is None
    d = tempfile.mkdtemp(prefix="spcat_") if own else workdir
    try:
        p = par.copy()
        for q in p.params:  # uncertainties are propagated by us, not by SPCAT
            q.prior = 0.0
        p.write(os.path.join(d, "x.var"))
        with open(os.path.join(d, "x.int"), "w") as f:
            f.write(int_text)
        _run(SPCAT, d, ["x.var", "x.int"])
        return read_cat(os.path.join(d, "x.cat"))
    finally:
        if own:
            shutil.rmtree(d, ignore_errors=True)


# ---------------------------------------------------------------- SPFIT
@dataclass
class FitResult:
    params: ParFile  # fitted values, with fitted 1-sigma errors in .prior
    errors: dict  # idpar -> fitted 1-sigma
    rms: float  # weighted rms (dimensionless, = sqrt(chi2/N) as printed by SPFIT)
    calc: dict  # line index (1-based, .lin order) -> calc freq (blend average for blends)
    ok: bool
    log: str
    var_text: str = ""  # SPFIT's posterior .var (values, errors, correlation) for SPCAT


def spfit(par: ParFile, lin_rows, workdir=None):
    """Run SPFIT. Returns FitResult; calc frequencies are taken from the last iteration listing."""
    own = workdir is None
    d = tempfile.mkdtemp(prefix="spfit_") if own else workdir
    try:
        par.write(os.path.join(d, "x.par"), nline=len(lin_rows) + 10)  # SPFIT crashes with NLINE=1
        write_lin(os.path.join(d, "x.lin"), lin_rows)
        log = _run(SPFIT, d, ["x.par", "x.lin"])
        fitp = os.path.join(d, "x.fit")
        if not os.path.exists(fitp) or not os.path.exists(os.path.join(d, "x.var")):
            return FitResult(par, {}, float("nan"), {}, False, log)
        var_text = open(os.path.join(d, "x.var")).read()
        txt = open(fitp).read().splitlines()
        calc = {}
        rms = float("nan")
        for line in txt:
            if "NEW RMS ERROR=" in line:
                rms = float(line.split()[-1])
            s = line.lstrip()
            if ":" in s[:7] and s.split(":")[0].isdigit():
                idx = int(s.split(":")[0])
                body = line.split(":", 1)[1]
                nums = body[36:].split()
                try:
                    obs, cal = float(nums[0]), float(nums[1])
                except (IndexError, ValueError):
                    continue
                # for blends SPFIT prints extra columns: blend calc, diff, weight
                if len(nums) >= 8:
                    cal = float(nums[5])
                calc[idx] = cal  # later iterations overwrite earlier ones
        var = read_par(os.path.join(d, "x.var"), len(par.option_lines))
        errors = {p.idpar: p.prior for p in var.params}
        ok = np.isfinite(rms) and all(np.isfinite(p.value) for p in var.params)
        diverged = "Diverging" in "\n".join(txt[-200:])
        # keep the a-priori constraints of the input in the returned parameter set
        out = par.copy()
        for p, v in zip(out.params, var.params):
            p.value = v.value
        return FitResult(out, errors, rms, calc, ok and not diverged, log, var_text)
    finally:
        if own:
            shutil.rmtree(d, ignore_errors=True)
