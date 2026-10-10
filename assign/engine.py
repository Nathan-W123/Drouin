"""The assignment loop.

Arms
  greedy : no judgement. Every round: predict, nearest-match every prediction within 3 sigma (from
           scratch), refit, release parameters by the same statistical rule. Stops when the
           assignment set no longer changes.
  rules  : the full deterministic pipeline (bootstrap hypothesis search, Bayesian candidate
           probabilities, outlier and parameter-release tests) with every default applied
           automatically.
  ai     : the same pipeline, but each round stops and waits for a decision file
           decisions/<case>_s<seed>/round_NN.csv written by the decision-maker (in this prototype:
           Claude in the Claude Code session, reviewed by a human).  Every applied decision is logged
           with a one-line reason; departures from the rule-based default are counted.

One round = [decide on: bootstrap hypothesis | outliers of the last fit, parameter releases,
new candidate assignments] -> refit (SPFIT) -> predict (SPCAT + covariance).

The engine never reads truth.csv; scoring is done separately by assign.score.
"""
import csv
import json
import math
import os
import shutil

import numpy as np

from . import pickett as pk
from .match import Peaks, bootstrap, candidates, greedy, key_str, parse_key
from .model import Model, load_case, order
from .predict import Predictor

SETTINGS = dict(
    int_margin=0.5,  # predictions down to (detection limit - margin) are considered
    sigma_I=0.3,  # intensity agreement scale (dex) for the probability model
    n_win=4.0,  # candidate window in sigma
    p_accept=0.95,  # default: accept if posterior probability >= this
    p_show=0.01,
    max_in_window=40,
    p_have0=0.5,
    p_have_min_n=30,
    outlier_t=4.0,  # |studentized residual| above which the worst line is rejected by default
    release_dchi2=9.0,  # parameter release: chi2 improvement required ...
    release_snr=3.0,  # ... and |value/sigma| required
    relax_ratio=0.1,  # prior removed once posterior sigma < relax_ratio * prior (Kisiel's rule) ...
    relax_min_ratio=3.0,  # ... and only once there are >= 3 lines per floating parameter
    # a batch of accepts whose fit diverges is rolled back and re-added one line at a time
    max_rounds=40,
    greedy_max_rounds=20,
)


class NeedDecision(Exception):
    pass


def _w(path, rows, cols):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def _fmt(r):
    return {k: (f"{v:.6g}" if isinstance(v, float) else v) for k, v in r.items()}


class Run:
    def __init__(self, case, seed=1, arm="rules", tag="", settings=None):
        self.cfg = load_case(case)
        self.case, self.seed, self.arm = self.cfg["key"], seed, arm
        self.s = dict(SETTINGS, **(settings or {}))
        self.tc = os.path.join(pk.ROOT, "testcases", f"{self.case}_s{seed}")
        meta = json.load(open(os.path.join(self.tc, "testcase.json")))
        self.s["i_det"] = meta["detection_limit_lgint"]
        self.s["fwhm_factor"] = 7.162e-7 * math.sqrt(self.cfg.get("temperature_K", 300.0) / self.cfg["mass_amu"])
        self.peaks = Peaks.load(os.path.join(self.tc, "peaks.csv"))
        self.dir = os.path.join(pk.ROOT, "runs", f"{self.case}_s{seed}_{arm}{tag}")
        self.dec_dir = os.path.join(pk.ROOT, "decisions", f"{self.case}_s{seed}{tag}")
        self.pred_ = Predictor(self.cfg, self.cfg["fmin_mhz"], self.cfg["fmax_mhz"])
        self.state_path = os.path.join(self.dir, "state.json")
        if os.path.exists(self.state_path):
            st = json.load(open(self.state_path))
            self.round = st["round"]
            self.model = Model.from_json(self.cfg, st["model"])
            self.assign = {int(k): [tuple(x) for x in v] for k, v in st["assign"].items()}
            self.assign_meta = {int(k): v for k, v in st["assign_meta"].items()}
            self.rejected = {(int(a), tuple(b)) for a, b in st["rejected"]}
            self.history, self.done, self.boot = st["history"], st["done"], st["boot"]
            self.var_text, self.resid = st["var_text"], {int(k): v for k, v in st["resid"].items()}
        else:
            os.makedirs(self.dir, exist_ok=True)
            self.round = 0
            self.model = Model.from_json(self.cfg, json.load(open(os.path.join(self.tc, "model.json"))))
            self.assign, self.assign_meta, self.rejected = {}, {}, set()
            self.history, self.done, self.boot = [], False, arm == "greedy"
            self.var_text, self.resid = "", {}
            self.save()

    # ------------------------------------------------------------ persistence
    def save(self):
        st = dict(round=self.round, model=self.model.to_json(),
                  assign={str(k): [list(x) for x in v] for k, v in self.assign.items()},
                  assign_meta={str(k): v for k, v in self.assign_meta.items()},
                  rejected=[[a, list(b)] for a, b in sorted(self.rejected)], history=self.history,
                  done=self.done, boot=self.boot, var_text=self.var_text,
                  resid={str(k): v for k, v in self.resid.items()},
                  steps={str(k): v for k, v in self.pred_.steps.items()})
        tmp = self.state_path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(st, f)
        os.replace(tmp, self.state_path)

    # ------------------------------------------------------------ helpers
    def peak(self, pid):
        n = self.peaks.pos[pid]
        return self.peaks.freq[n], self.peaks.err[n], self.peaks.lgint[n]

    def assigned_list(self):
        return [(tuple(ks), self.peak(pid)[1]) for pid, ks in self.assign.items()]

    def lin_rows(self, assign=None):
        rows, order_ = [], []
        for pid, ks in sorted((assign or self.assign).items(), key=lambda kv: self.peak(kv[0])[0]):
            f, e, _ = self.peak(pid)
            for k in ks:
                rows.append(dict(up=k[:3], lo=k[3:], freq=f, err=e, wt=1.0 if len(ks) > 1 else None))
                order_.append(pid)
        return rows, order_

    def predict(self):
        return self.pred_.predict(self.model, self.assigned_list(), self.var_text or None)

    def fit(self, model=None, assign=None):
        """SPFIT with the current assignments. Returns (FitResult, residual dict, chi2 total)."""
        model = model or self.model
        rows, order_ = self.lin_rows(assign)
        if not rows:
            return None, {}, 0.0
        r = pk.spfit(model.to_parfile(), rows)
        resid, chi2 = {}, 0.0
        for n, pid in enumerate(order_, start=1):
            if pid in resid or n not in r.calc:
                continue
            f, e, _ = self.peak(pid)
            resid[pid] = dict(obs=f, calc=r.calc[n], res=f - r.calc[n], z=(f - r.calc[n]) / e)
            chi2 += resid[pid]["z"] ** 2
        prior_chi2 = sum(((r.params.get(p.idpar).value - p.center) / p.prior) ** 2
                         for p in model.floating() if p.prior < 1e30)
        return r, resid, chi2 + prior_chi2

    def apply_fit(self, r, resid):
        for p in self.model.floating():
            p.value = r.params.get(p.idpar).value
        relaxed = []
        n_lines = len(resid)
        for p in self.model.floating():
            if n_lines < self.s["relax_min_ratio"] * len(self.model.floating()):
                break
            if p.prior < 1e30 and r.errors.get(p.idpar, 1e99) < self.s["relax_ratio"] * p.prior:
                p.prior = pk.FREE_ERR
                relaxed.append(p.label)
        self.var_text, self.resid = r.var_text, resid
        return relaxed

    # ------------------------------------------------------------ diagnostics
    def _requested_outliers(self):
        """Peaks the decision file wants to act on, so they appear in the outlier table even if they
        are not flagged by the statistics."""
        if self.arm != "ai":
            return set()
        path = os.path.join(self.dec_dir, f"round_{self.round:02d}.csv")
        if not os.path.exists(path):
            return set()
        return {int(d["item"]) for d in csv.DictReader(open(path)) if d["kind"] == "outlier"}

    def outlier_table(self, pred, extra=()):
        rows = []
        for pid, ks in self.assign.items():
            if pid not in self.resid:
                if pid in extra:  # e.g. the last fit failed: still allow an explicit decision on it
                    rows.append(dict(peak=pid, keys=";".join(key_str(k) for k in ks), obs_freq=self.peak(pid)[0],
                                     err=self.peak(pid)[1], res=float("nan"), t=float("nan"), leverage=float("nan"),
                                     dI=float("nan"), round=self.assign_meta[pid]["round"],
                                     how=self.assign_meta[pid]["how"]))
                continue
            f, e, lg = self.peak(pid)
            ii = [pred.index[k] for k in ks if k in pred.index]
            if not ii:
                continue
            Jr = pred.J[ii].mean(axis=0)
            h = float(Jr @ pred.cov @ Jr) / e ** 2
            res = self.resid[pid]["res"]
            t = res / (e * math.sqrt(max(1 - min(h, 0.999), 1e-3)))
            pl = math.log10(sum(10 ** pred.lgint[i] for i in ii))
            rows.append(dict(peak=pid, keys=";".join(key_str(k) for k in ks), obs_freq=f, err=e, res=res,
                             t=t, leverage=h, dI=lg - pl, round=self.assign_meta[pid]["round"],
                             how=self.assign_meta[pid]["how"]))
        if len(self.assign) < len(self.model.floating()) + 5:  # too few dof for a statistical outlier test
            for r in rows:
                r["default"], r["reason"] = "keep", f"t={r['t']:+.1f} h={r['leverage']:.2f} (too few dof to test)"
            return [r for r in rows if r["peak"] in extra]
        rows.sort(key=lambda r: -abs(r["t"]) if r["leverage"] < 0.9 else 0)  # nan rows sort last
        worst = rows[0] if rows and rows[0]["leverage"] < 0.9 else None
        for r in rows:
            r["default"] = "keep"
            r["reason"] = f"t={r['t']:+.1f} h={r['leverage']:.2f}"
            if worst and r is worst and abs(r["t"]) > self.s["outlier_t"]:
                r["default"] = "reject"
            elif abs(r["t"]) > 2 * self.s["outlier_t"] and r["leverage"] < 0.9:
                r["default"] = "reject"
        return [r for r in rows if abs(r["t"]) > 3 or r["leverage"] > 0.8 or r["peak"] in extra]

    def param_table(self):
        fl = self.model.floating()
        if not self.assign or len(self.assign) < len(fl) + 10:
            return []
        maxo = max(order(p.idpar) for p in fl)
        base, _, chi0 = self.fit()
        if base is None or not base.ok:
            return []
        rows = []
        for p in self.model.absent():
            if order(p.idpar) > maxo + 2:
                continue
            r, _, chi = self.fit(model=_with_trial(self.model, p))
            if r is None or not r.ok:
                rows.append(dict(idpar=p.idpar, label=p.label, order=order(p.idpar), dchi2=float("nan"),
                                 value=float("nan"), sigma=float("nan"), snr=0.0, scale=p.scale, ratio=float("nan")))
                continue
            v, sg = r.params.get(p.idpar).value, r.errors.get(p.idpar, float("nan"))
            rows.append(dict(idpar=p.idpar, label=p.label, order=order(p.idpar), dchi2=chi0 - chi, value=v, sigma=sg,
                             snr=abs(v / sg) if sg > 0 else 0.0, scale=p.scale, ratio=abs(v) / p.scale))
        rows.sort(key=lambda r: -(r["dchi2"] if np.isfinite(r["dchi2"]) else -1e9))
        for n, r in enumerate(rows):
            good = np.isfinite(r["dchi2"]) and r["dchi2"] >= self.s["release_dchi2"] and r["snr"] >= self.s["release_snr"]
            r["default"] = "release" if (n == 0 and good) else "hold"
            r["reason"] = f"dchi2={r['dchi2']:.1f} |v/s|={r['snr']:.1f} |v|/scale={r['ratio']:.2g}"
        if self.s.get("release_multi"):
            self._forward_select(rows, chi0)
        return rows

    def _most_influential(self):
        """Leave-one-out: the assigned peak whose removal lowers chi2 most, and the fraction of the
        excess chi2 (chi2 - N) it removes."""
        r0, res0, chi0 = self.fit()
        if r0 is None:
            return None, 0.0
        excess = chi0 - len(res0)
        best = (None, 0.0)
        for pid in list(self.assign):
            a = {p: k for p, k in self.assign.items() if p != pid}
            r, res, chi = self.fit(assign=a)
            if r is not None and r.ok and excess > 0 and (chi0 - chi) / excess > best[1]:
                best = (pid, (chi0 - chi) / excess)
        return best

    def _forward_select(self, rows, chi0):
        """rules+ : stepwise forward selection of several terms in one round; a term is eligible only if
        its value is within release_max_ratio x its order-of-magnitude scale (else it is compensating)."""
        for r in rows:
            r["default"] = "hold"
        chosen, model, chi_cur = [], self.model, chi0
        for _ in range(self.s.get("release_max", 5)):
            best = None
            for r in rows:
                if r["idpar"] in chosen:
                    continue
                p = self.model.get(r["idpar"])
                if order(p.idpar) > max(order(q.idpar) for q in model.floating()) + 2:
                    continue
                f, _, chi = self.fit(model=_with_trial(model, p))
                if f is None or not f.ok:
                    continue
                v, sg = f.params.get(p.idpar).value, f.errors.get(p.idpar, float("nan"))
                d = chi_cur - chi
                if d >= self.s["release_dchi2"] and sg > 0 and abs(v / sg) >= self.s["release_snr"] \
                        and abs(v) <= self.s.get("release_max_ratio", 10.0) * p.scale and (best is None or d > best[0]):
                    best = (d, r, chi)
            if best is None:
                break
            d, r, chi = best
            chosen.append(r["idpar"])
            model = _with_trial(model, self.model.get(r["idpar"]))
            chi_cur = chi
            r["default"] = "release"
            r["reason"] += f" [forward selection step {len(chosen)}: dchi2={d:.1f}]"

    # ------------------------------------------------------------ decisions
    def decisions(self, kind_rows, rdir):
        """Return {(kind, item): (action, reason, source)} for every row.  rules: defaults.
        ai: read the decision file; rows not overridden take the default, confirmed by the
        reviewer through an 'all,defaults,confirm,<reason>' line."""
        out, alias = {}, {}
        for kind, rows, idk in kind_rows:
            for r in rows:
                out[(kind, str(r[idk]))] = (r["default"], "default: " + r["reason"], "default")
                if kind == "assign":  # candidates can be referred to stably as "<key>@<peak>"
                    alias[("assign", f"{r['key']}@{r['peak']}")] = ("assign", r["cid"])
        if self.arm != "ai":
            return out, 0
        path = os.path.join(self.dec_dir, f"round_{self.round:02d}.csv")
        if not os.path.exists(path):
            raise NeedDecision(path)
        confirm, n_over, blanket = None, 0, {}
        for d in csv.DictReader(open(path)):
            kind, item, action, reason = d["kind"], d["item"], d["action"], d["reason"]
            if kind == "all":
                if item == "defaults":
                    confirm = reason
                else:  # e.g. all,assign,defer,<reason>: applies to every row of that kind not listed
                    blanket[item] = (action, reason)
                continue
            kind, item = alias.get((kind, item), (kind, item))
            if (kind, item) not in out and kind not in ("stop",):
                raise ValueError(f"decision for unknown item {kind} {item} in {path}")
            if kind == "stop":
                out[("stop", "stop")] = (action, "AI: " + reason, "ai")
                continue
            if action != out[(kind, item)][0]:
                n_over += 1
                out[(kind, item)] = (action, "AI override: " + reason, "ai-override")
            else:
                out[(kind, item)] = (action, "AI: " + reason, "ai")
        if confirm is None:
            raise ValueError(f"{path}: missing 'all,defaults,confirm,<reason>' line")
        for k, v in list(out.items()):
            if v[2] == "default" and k[0] in blanket:
                action, reason = blanket[k[0]]
                if action != v[0]:
                    n_over += 1
                    out[k] = (action, "AI override (blanket): " + reason, "ai-override")
                else:
                    out[k] = (action, "AI (blanket): " + reason, "ai")
        for k, v in out.items():
            if v[2] == "default":
                out[k] = (v[0], f"AI confirmed default ({confirm}); " + v[1], "ai-confirmed")
        return out, n_over

    # ------------------------------------------------------------ one round
    def step(self):
        if self.done:
            return False
        self.round += 1
        rdir = os.path.join(self.dir, f"round_{self.round:02d}")
        os.makedirs(rdir, exist_ok=True)
        try:
            if self.arm == "greedy":
                self._step_greedy(rdir)
            else:
                self._step_judged(rdir)
        except NeedDecision:
            self.round -= 1
            raise
        self.save()
        return not self.done

    def _record(self, rdir, entry):
        entry.update(round=self.round, n_assigned=len(self.assign), n_lines=sum(len(v) for v in self.assign.values()),
                     n_float=len(self.model.floating()))
        self.history.append(entry)
        _w(os.path.join(rdir, "assignments.csv"),
           [dict(peak=p, keys=";".join(key_str(k) for k in ks), round=self.assign_meta[p]["round"],
                 how=self.assign_meta[p]["how"]) for p, ks in sorted(self.assign.items())],
           ["peak", "keys", "round", "how"])
        _w(os.path.join(rdir, "params.csv"),
           [dict(idpar=p.idpar, label=p.label, value=f"{p.value:.12e}", prior=f"{p.prior:.3e}", status=p.status)
            for p in self.model.params], ["idpar", "label", "value", "prior", "status"])
        with open(os.path.join(rdir, "fit_summary.json"), "w") as f:
            json.dump(entry, f, indent=1, default=str)

    def _fit_and_update(self):
        r, resid, chi2 = self.fit()
        if r is None:
            return dict(rms=float("nan"), chi2=0.0, fit_ok=True, relaxed=[])
        if not r.ok:
            return dict(rms=r.rms, chi2=chi2, fit_ok=False, relaxed=[])
        relaxed = self.apply_fit(r, resid)
        n = max(len(resid), 1)
        return dict(rms=math.sqrt(sum(v["z"] ** 2 for v in resid.values()) / n), chi2=chi2, fit_ok=True,
                    relaxed=relaxed)

    def _step_greedy(self, rdir):
        pred = self.predict()
        pairs = greedy(pred, self.peaks, self.s)
        new = {}
        for pid, k in pairs:
            new.setdefault(pid, []).append(k)
        changed = {p: sorted(v) for p, v in new.items()} != {p: sorted(v) for p, v in self.assign.items()}
        self.assign = new
        self.assign_meta = {p: dict(round=self.round, how="greedy") for p in new}
        fit = self._fit_and_update()
        released = []
        if fit["fit_ok"]:
            prow = self.param_table()
            for r in prow:
                if r["default"] == "release":
                    _release(self.model, r)
                    released.append(r["label"])
            if released:
                fit = self._fit_and_update()
        _w(os.path.join(rdir, "decisions_applied.csv"),
           [dict(kind="assign", item=p, action="accept", reason="greedy nearest match", source="greedy") for p in new],
           ["kind", "item", "action", "reason", "source"])
        self._record(rdir, dict(n_accept=len(new), n_reject=0, released=released, overrides=0, **fit))
        if (not changed and not released) or self.round >= self.s["greedy_max_rounds"]:
            self.done = True

    def _step_judged(self, rdir):
        pred = self.predict()
        from .plots import round_plots
        if not self.boot:
            clusters, anchors = bootstrap(pred, self.peaks, self.s)
            hrows = []
            for n, c in enumerate(clusters, 1):
                hrows.append(dict(rank=n, Z=c["Z"], n_match=c["n_match"], n_scored=c["n_scored"],
                                  n_expected=c["n_expected"], support=c["support"],
                                  anchors=";".join(f"{key_str(k)}->{p}" for k, p in c["anchors"]),
                                  matched=len(c["matched"]),
                                  default="accept" if n == 1 else "reject",
                                  reason=f"Z={c['Z']:.1f} ({c['n_match']}/{c['n_scored']} matched, {c['n_expected']:.1f} by chance), support={c['support']}"))
            _w(os.path.join(rdir, "proposal_bootstrap.csv"), [_fmt(r) for r in hrows], list(hrows[0]) if hrows else ["rank"])
            self._summary_boot(rdir, hrows, anchors)
            dec, n_over = self.decisions([("hyp", hrows, "rank")], rdir)
            acc = [r for r in hrows if dec[("hyp", str(r["rank"]))][0] == "accept"]
            log = [dict(kind="hyp", item=r["rank"], action=dec[("hyp", str(r["rank"]))][0],
                        reason=dec[("hyp", str(r["rank"]))][1], source=dec[("hyp", str(r["rank"]))][2]) for r in hrows]
            _w(os.path.join(rdir, "decisions_applied.csv"), log, ["kind", "item", "action", "reason", "source"])
            for r in acc[:1]:
                for a in r["anchors"].split(";"):
                    k, p = a.split("->")
                    self.assign.setdefault(int(p), [])
                    if parse_key(k) not in self.assign[int(p)]:
                        self.assign[int(p)].append(parse_key(k))
                    self.assign_meta[int(p)] = dict(round=self.round, how="bootstrap")
            self.boot = bool(acc)
            fit = self._fit_and_update()
            self._record(rdir, dict(n_accept=sum(len(r["anchors"].split(";")) for r in acc[:1]), n_reject=0,
                                    released=[], overrides=n_over, bootstrap=True, **fit))
            round_plots(self, self.predict(), rdir)
            return

        orows = self.outlier_table(pred, extra=self._requested_outliers())
        prows = self.param_table()
        release_pending = any(r["default"] == "release" for r in prows)
        if self.s.get("release_before_reject") and release_pending:
            for r in orows:  # rules+ : an incomplete model is fixed before any line is rejected
                if r["default"] == "reject":
                    r["default"] = "keep"
                    r["reason"] += " [kept: parameter release pending, model incomplete]"
        clean_first = False
        if self.s.get("clean_first") and self.history and self.history[-1]["rms"] > 3 and not release_pending:
            # rules+ : contaminated fit -> no growth this round; reject the most influential line instead
            clean_first = True
            for r in orows:
                if r["default"] == "reject":
                    r["default"] = "keep"
            pid, frac = self._most_influential()
            if pid is not None and frac >= 0.3:
                hit = [r for r in orows if r["peak"] == pid]
                if not hit:
                    orows.append(dict(peak=pid, keys=";".join(key_str(k) for k in self.assign[pid]), obs_freq=0.0, err=0.0,
                                      res=0.0, t=0.0, leverage=0.0, dI=0.0, round=self.assign_meta[pid]["round"],
                                      how=self.assign_meta[pid]["how"]))
                    hit = orows[-1:]
                hit[0]["default"] = "reject"
                hit[0]["reason"] = f"leave-one-out: removing it removes {100 * frac:.0f}% of the excess chi2"
        crows, info = candidates(pred, self.peaks, set(self.assign), {k for v in self.assign.values() for k in v},
                                 self.rejected, self.s)
        _w(os.path.join(rdir, "proposal.csv"), [_fmt(r) for r in crows],
           ["cid", "key", "pred_freq", "pred_sigma", "pred_lgint", "peak", "obs_freq", "obs_err", "obs_lgint", "z", "dI", "P",
            "n_win", "rival", "contest", "blend_with", "flags", "default", "reason"])
        _w(os.path.join(rdir, "outliers.csv"), [_fmt(r) for r in orows],
           ["peak", "keys", "obs_freq", "err", "res", "t", "leverage", "dI", "round", "how", "default", "reason"])
        _w(os.path.join(rdir, "param_release.csv"), [_fmt(r) for r in prows],
           ["idpar", "label", "order", "dchi2", "value", "sigma", "snr", "scale", "ratio", "default", "reason"])
        self._summary(rdir, crows, orows, prows, info)
        round_plots(self, pred, rdir, crows)
        if self.s.get("series_rule"):
            self._apply_series_rule(crows)
        if clean_first:
            for r in crows:
                if r["default"] == "accept":
                    r["default"] = "defer"
                    r["reason"] += " [deferred: last fit contaminated (rms>3), clean first]"
        dec, n_over = self.decisions([("assign", crows, "cid"), ("outlier", orows, "peak"), ("param", prows, "idpar")], rdir)
        log = [dict(kind=k, item=i, action=a, reason=r, source=s) for (k, i), (a, r, s) in dec.items()]
        _w(os.path.join(rdir, "decisions_applied.csv"), log, ["kind", "item", "action", "reason", "source"])

        n_rej = 0
        for r in orows:
            act = dec[("outlier", str(r["peak"]))][0]
            if act in ("reject", "unassign"):  # 'unassign' removes without blacklisting the pairs
                for k in self.assign.pop(r["peak"], []):
                    if act == "reject":
                        self.rejected.add((r["peak"], k))
                self.assign_meta.pop(r["peak"], None)
                n_rej += 1
        released = []
        for r in prows:
            if dec[("param", str(r["idpar"]))][0] == "release":
                _release(self.model, r)
                released.append(r["label"])
        n_acc = 0
        for r in crows:
            a = dec[("assign", r["cid"])][0]
            k, pid = parse_key(r["key"]), int(r["peak"])
            if a == "accept":
                if any(k in v for v in self.assign.values()):
                    continue  # each prediction is assigned at most once
                self.assign.setdefault(pid, []).append(k)
                self.assign_meta[pid] = dict(round=self.round, how=self.arm)
                n_acc += 1
            elif a == "reject":
                self.rejected.add((pid, k))
        stop = dec.get(("stop", "stop"), ("no",))[0] == "yes"
        snapshot = (self.model.to_json(), self.var_text, dict(self.resid))
        fit = self._fit_and_update()
        n_broke = 0
        # only a *diverged* fit triggers the fallback: a higher rms after adding correct lines usually means
        # the Hamiltonian is incomplete, which the parameter-release test (next round) addresses
        if n_acc and not fit["fit_ok"]:
            # the batch made the fit worse: restore and add the new lines one at a time (highest P first);
            # a line that breaks the fit on its own is rejected
            self.model = Model.from_json(self.cfg, snapshot[0])
            self.var_text, self.resid = snapshot[1], snapshot[2]
            new = [(int(r["peak"]), parse_key(r["key"])) for r in crows
                   if dec[("assign", r["cid"])][0] == "accept" and parse_key(r["key"]) in self.assign.get(int(r["peak"]), [])
                   and self.assign_meta.get(int(r["peak"]), {}).get("round") == self.round]
            for pid, k in new:
                self.assign[pid].remove(k)
                if not self.assign[pid]:
                    del self.assign[pid], self.assign_meta[pid]
            for pid, k in new:
                good = self.model.to_json()
                self.assign.setdefault(pid, []).append(k)
                self.assign_meta[pid] = dict(round=self.round, how=self.arm)
                f1 = self._fit_and_update()
                if not f1["fit_ok"]:
                    self.assign[pid].remove(k)
                    if not self.assign[pid]:
                        del self.assign[pid], self.assign_meta[pid]
                    self.rejected.add((pid, k))
                    self.model = Model.from_json(self.cfg, good)
                    n_broke += 1
                    n_acc -= 1
            fit = self._fit_and_update()
            fit["sequential"] = True
        fit["n_broke_fit"] = n_broke
        self._record(rdir, dict(n_accept=n_acc, n_reject=n_rej, released=released, overrides=n_over,
                                p_have=info["p_have"], n_candidates=len(crows), **fit))
        if stop or (n_acc == 0 and n_rej == 0 and not released) or self.round >= self.s["max_rounds"]:
            self.done = True

    def _apply_series_rule(self, crows):
        """Automated version of the series-coherence judgement (ablation arm 'rules+series'):
        accept members of coherent series (>= series_min lines, chance probability < series_p) that are
        the best candidate of their prediction, not contested and within 3 sigma."""
        from .series import analyse
        chains = analyse(crows, min_members=self.s.get("series_min", 4))
        best = {}
        for r in crows:
            if r["key"] not in best or r["P"] > best[r["key"]]["P"]:
                best[r["key"]] = r
        for c in chains:
            if c["p_chance"] > self.s.get("series_p", 1e-4) or c["members"][0]["sr"] > 0.05:
                continue
            for m in c["members"]:
                r = m["row"]
                if r is best[r["key"]] and r["contest"] <= 0.05 and abs(r["z"]) <= 3 and r["default"] != "accept":
                    r["default"] = "accept"
                    r["reason"] += f" [series rule: {c['n']} coherent, P(chance)={c['p_chance']:.0e}]"

    # ------------------------------------------------------------ summaries for the decision-maker
    def _summary_boot(self, rdir, hrows, anchors):
        L = [f"# {self.case} seed {self.seed} arm {self.arm} -- round {self.round}: BOOTSTRAP", "",
             "Anchor lines (best-predicted, strong) and their number of intensity-consistent candidate peaks:"]
        L += [f"- {key_str(k)}: {len(js)} candidates (peaks {js})" for k, js in anchors]
        L += ["", "| rank | Z | matched/scored | chance | support | anchors | default |", "|---|---|---|---|---|---|---|"]
        L += [f"| {r['rank']} | {r['Z']:.1f} | {r['n_match']}/{r['n_scored']} | {r['n_expected']:.1f} | {r['support']} | {r['anchors']} | {r['default']} |" for r in hrows]
        open(os.path.join(rdir, "summary.md"), "w").write("\n".join(L) + "\n")

    def _summary(self, rdir, crows, orows, prows, info):
        acc = [r for r in crows if r["default"] == "accept"]
        flagged = [r for r in crows if r["default"] != "accept" and r["P"] >= 0.5]
        fl_acc = [r for r in acc if r["flags"]]
        h = self.history[-1] if self.history else {}
        L = [f"# {self.case} seed {self.seed} arm {self.arm} -- round {self.round}", "",
             f"assigned peaks {len(self.assign)}, floating params {len(self.model.floating())}, "
             f"last rms (weighted) {h.get('rms', float('nan')):.3f}",
             f"predictions considered {info['n_predictions']}, with candidates {info['n_with_candidates']}, "
             f"unresolvable windows {info['n_unresolvable']}, p_have={info['p_have']:.2f} (from {info['n_calib']} sharp predictions)",
             f"candidate rows {len(crows)}: default accept {len(acc)} (of which flagged {len(fl_acc)}), "
             f"deferred with P>=0.5: {len(flagged)}", ""]
        L += ["## Outliers / high leverage in last fit", "| peak | keys | res MHz | t | h | dI | round | default |", "|---|---|---|---|---|---|---|---|"]
        L += [f"| {r['peak']} | {r['keys']} | {r['res']:+.4f} | {r['t']:+.1f} | {r['leverage']:.2f} | {r['dI']:+.2f} | {r['round']} | {r['default']} |" for r in orows[:25]]
        L += ["", "## Parameter release trials", "| id | label | order | dchi2 | value | |v/s| | |v|/scale | default |", "|---|---|---|---|---|---|---|---|"]
        L += [f"| {r['idpar']} | {r['label']} | {r['order']} | {r['dchi2']:.1f} | {r['value']:.4g} | {r['snr']:.1f} | {r['ratio']:.2g} | {r['default']} |" for r in prows[:12]]
        L += ["", "## Default-accepted candidates carrying flags", "| cid | key | peak | z | dI | P | flags | blend |", "|---|---|---|---|---|---|---|---|"]
        L += [f"| {r['cid']} | {r['key']} | {r['peak']} | {r['z']:+.2f} | {r['dI']:+.2f} | {r['P']:.3f} | {r['flags']} | {r['blend_with']} |" for r in fl_acc[:40]]
        L += ["", "## Deferred candidates with P >= 0.5", "| cid | key | sigma MHz | peak | z | dI | P | rival | contest | flags |", "|---|---|---|---|---|---|---|---|---|---|"]
        L += [f"| {r['cid']} | {r['key']} | {r['pred_sigma']:.3g} | {r['peak']} | {r['z']:+.2f} | {r['dI']:+.2f} | {r['P']:.3f} | {r['rival']:.2f} | {r['contest']:.2f} | {r['flags']} |" for r in flagged[:60]]
        if len(acc) - len(fl_acc):
            ps = np.array([r["P"] for r in acc if not r["flags"]])
            zs = np.array([abs(r["z"]) for r in acc if not r["flags"]])
            L += ["", f"Unflagged default accepts: {len(ps)}, min P {ps.min():.3f}, max |z| {zs.max():.2f}"]
        open(os.path.join(rdir, "summary.md"), "w").write("\n".join(L) + "\n")


def _with_trial(model, p):
    m = Model.from_json(model.cfg, model.to_json())
    q = m.get(p.idpar)
    q.status, q.prior, q.value, q.center = "float", pk.FREE_ERR, 0.0, 0.0
    return m


def _release(model, row):
    p = model.get(int(row["idpar"]))
    p.status, p.prior = "float", pk.FREE_ERR
    p.value = p.center = float(row["value"]) if np.isfinite(row["value"]) else 0.0


def run(case, seed=1, arm="rules", tag="", fresh=False, settings=None, quiet=False):
    d = os.path.join(pk.ROOT, "runs", f"{load_case(case)['key']}_s{seed}_{arm}{tag}")
    if fresh and os.path.exists(d):
        shutil.rmtree(d)
    r = Run(case, seed, arm, tag, settings)
    try:
        while r.step():
            if not quiet:
                h = r.history[-1]
                print(f"round {h['round']:2d}: assigned {h['n_assigned']:4d} (+{h['n_accept']}, -{h['n_reject']}) "
                      f"rms {h['rms']:.3f} float {h['n_float']} released {h['released']}", flush=True)
    except NeedDecision as e:
        print(f"waiting for decision file {e}")
        print(f"proposal: {os.path.join(r.dir, f'round_{r.round + 1:02d}', 'summary.md')}")
        return r
    if not quiet and r.history:
        h = r.history[-1]
        print(f"done after round {h['round']}: assigned {h['n_assigned']} rms {h['rms']:.3f}")
    return r


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("case")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--arm", default="rules", choices=["greedy", "rules", "ai"])
    ap.add_argument("--tag", default="")
    ap.add_argument("--fresh", action="store_true")
    ap.add_argument("--p-accept", type=float, default=None)
    ap.add_argument("--series-rule", action="store_true", help="ablation: automated series-coherence acceptance")
    ap.add_argument("--plus", action="store_true", help="rules+: series rule + multi-term forward selection + "
                    "no rejection while a release is pending + magnitude plausibility")
    a = ap.parse_args()
    st = {}
    if a.p_accept is not None:
        st["p_accept"] = a.p_accept
    if a.series_rule:
        st["series_rule"] = True
    if a.plus:  # rules+ : lessons codified from the H2CO AI session
        st.update(series_rule=True, release_multi=True, release_before_reject=True, clean_first=True)
    run(a.case, a.seed, a.arm, a.tag, a.fresh, settings=st)
