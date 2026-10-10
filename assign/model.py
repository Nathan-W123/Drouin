"""Hamiltonian parameter model: official constants, perturbed starting constants, priors.

Every parameter carries
  value   current value
  center  centre of its Gaussian prior (the starting "quantum-chemistry" estimate)
  prior   prior 1-sigma (FREE_ERR = unconstrained, FIXED_ERR = fixed)
  status  'float' (in the fit) or 'absent' (not yet in the model, contributes only model error)

SPFIT centres its prior on the value given in the .par file, so constrained parameters are always
written with value=center (see ParFile construction in to_parfile); unconstrained ones use the
current value.
"""
import json
import math
import os
from dataclasses import dataclass, asdict

import numpy as np

from . import pickett as pk

ROOT = pk.ROOT


def load_case(name):
    path = name if name.endswith(".json") else os.path.join(ROOT, "cases", f"{name}.json")
    with open(path) as f:
        cfg = json.load(f)
    cfg["key"] = os.path.splitext(os.path.basename(path))[0]
    return cfg


def rel(path):
    return os.path.join(ROOT, path)


# ------------------------------------------------------------------ IDPAR decoding
def decode(idpar):
    """Return (typ, ksq, nsq) for a rotational/centrifugal-distortion IDPAR (no spins)."""
    a = abs(idpar)
    nsq = (a // 100) % 10
    ksq = (a // 1000) % 10
    typ = (a // 10000) % 100
    return typ, ksq, nsq


def powers(idpar):
    """(p_eff, q): effective powers of N^2 and Nz^2.  TYP=4..12 operators (N+^2n + N-^2n)
    count as n extra powers of N^2 for order-of-magnitude purposes."""
    typ, ksq, nsq = decode(idpar)
    if typ in (1, 2, 3):
        return None
    extra = typ - 3 if 4 <= typ <= 12 else 0
    return nsq + extra, ksq


def order(idpar):
    pq = powers(idpar)
    return 2 if pq is None else 2 * (pq[0] + pq[1])


# ------------------------------------------------------------------ official constants
def official_params(cfg):
    """Official ground-state constants as {idpar: (value, sigma, label)}; rotational
    constants always expressed as A, B, C (IDs 10000/20000/30000)."""
    par = pk.read_par(rel(cfg["official_var"]), cfg["official_nopt"])
    out = {}
    for p in par.params:
        if p.idpar <= 0 or p.idpar >= 1_000_000 or (p.idpar % 100) not in cfg["official_state_suffixes"]:
            continue
        if p.prior < 1e-30:  # parameters fixed in the official fit are not part of the model
            continue
        out[p.idpar] = (p.value, p.prior, p.label)
    if cfg.get("official_symmetric_form"):
        x1, s1, _ = out.pop(1099)
        x2, s2, _ = out.pop(199)
        x3, s3, _ = out.pop(40099)
        out[10000] = (x1 + x2, math.hypot(s1, s2), "A")
        out[20000] = (x2 + 2 * x3, math.hypot(s2, 2 * s3), "B")
        out[30000] = (x2 - 2 * x3, math.hypot(s2, 2 * s3), "C")
    return out


# ------------------------------------------------------------------ model state
@dataclass
class P:
    idpar: int
    label: str
    value: float
    center: float
    prior: float
    status: str  # 'float' | 'absent'
    scale: float = 0.0  # order-of-magnitude scale used as model-error prior while absent

    @property
    def constrained(self):
        return self.status == "float" and self.prior < 1e30


class Model:
    def __init__(self, cfg, params):
        self.cfg = cfg
        self.params = params  # list of P

    def get(self, idpar):
        for p in self.params:
            if p.idpar == idpar:
                return p
        raise KeyError(idpar)

    def floating(self):
        return [p for p in self.params if p.status == "float"]

    def absent(self):
        return [p for p in self.params if p.status == "absent"]

    def to_parfile(self, title=None, extra=None, nitr=20):
        """ParFile for SPFIT/SPCAT. extra: list of P to include as unconstrained floats (trial release)."""
        ps = []
        for p in self.floating() + list(extra or []):
            if p in (extra or []):
                ps.append(pk.Param(p.idpar, p.value, pk.FREE_ERR, p.label))
            elif p.prior < 1e30:
                ps.append(pk.Param(p.idpar, p.center, p.prior, p.label))
            else:
                ps.append(pk.Param(p.idpar, p.value, pk.FREE_ERR, p.label))
        return pk.ParFile(title or self.cfg["name"], [self.cfg["option_line"]], ps, nitr=nitr)

    def current_parfile(self, extra_values=None):
        """ParFile with the *current* values (for SPCAT predictions). extra_values: {idpar: value}
        adds/overrides parameters (used for finite differences)."""
        vals = {p.idpar: p.value for p in self.floating()}
        labels = {p.idpar: p.label for p in self.params}
        for k, v in (extra_values or {}).items():
            vals[k] = v
        ps = [pk.Param(k, v, 0.0, labels.get(k, "")) for k, v in vals.items()]
        return pk.ParFile(self.cfg["name"], [self.cfg["option_line"]], ps)

    def to_json(self):
        return [asdict(p) for p in self.params]

    @classmethod
    def from_json(cls, cfg, data):
        return cls(cfg, [P(**d) for d in data])

    def prior_chi2(self):
        return sum(((p.value - p.center) / p.prior) ** 2 for p in self.floating() if p.prior < 1e30)


def magnitude_scales(start, abc, factor):
    """Order-of-magnitude scales for every (p, q) power pair, from the starting quartic
    constants:  M(p,q) = max(M(p-1,q)*eJ, M(p,q-1)*eK),  eJ = M(2,0)/B, eK = M(0,2)/A.
    Returns a function idpar -> factor * M."""
    A, B = abc
    base = {}
    for idp, val in start.items():
        pq = powers(idp)
        if pq is not None and sum(pq) == 2:
            base[pq] = max(base.get(pq, 0.0), abs(val))
    for pq in [(2, 0), (1, 1), (0, 2)]:
        base.setdefault(pq, math.sqrt(base.get((2, 0), 1e-9) * base.get((0, 2), 1e-9)))
    eJ, eK = base[(2, 0)] / B, base[(0, 2)] / A
    memo = dict(base)

    def M(p, q):
        if (p, q) in memo:
            return memo[(p, q)]
        c = []
        if p > 0 and p + q - 1 >= 2:
            c.append(M(p - 1, q) * eJ)
        if q > 0 and p + q - 1 >= 2:
            c.append(M(p, q - 1) * eK)
        memo[(p, q)] = max(c)
        return memo[(p, q)]

    return lambda idp: factor * M(*powers(idp))


def starting_model(cfg, rng, settings):
    """Perturb official constants to mimic a quantum-chemistry estimate.

    * A, B, C: random sign, |rel. error| ~ U(abc_lo, abc_hi);  prior sigma = abc_prior * value
    * quartic constants in cfg['start_params']: |rel. error| ~ U(q_lo, q_hi); prior = q_prior*|value|
    * every other official parameter is dropped ('absent') and gets an order-of-magnitude scale
    """
    off = official_params(cfg)
    rid = cfg["rot_ids"]
    params, start = [], {}
    for idp in cfg["start_params"]:
        val, _, lab = off[idp]
        if idp in rid.values():
            r = rng.uniform(settings["abc_lo"], settings["abc_hi"]) * rng.choice([-1, 1])
            v = val * (1 + r)
            prior = settings["abc_prior"] * abs(v)
        else:
            r = rng.uniform(settings["q_lo"], settings["q_hi"]) * rng.choice([-1, 1])
            v = val * (1 + r)
            prior = settings["q_prior"] * abs(v)
        start[idp] = v
        params.append(P(idp, lab, v, v, prior, "float"))
    scale = magnitude_scales(start, (start[rid["A"]], start[rid["B"]]), settings["absent_factor"])
    for idp, (val, _, lab) in sorted(off.items(), key=lambda kv: (order(kv[0]), kv[0])):
        if idp in start:
            continue
        params.append(P(idp, lab, 0.0, 0.0, pk.FREE_ERR, "absent", scale(idp)))
    return Model(cfg, params)
