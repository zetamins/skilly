#!/usr/bin/env python3
"""Recalibration advisor: compares our quoted probabilities against scored results and
suggests market-level adjustments. GATED: it advises nothing until n >= 30 settled matches
(below that, calibration signals are noise — do not retune on them).

Reads <work_dir>/results.csv + each run's answer.md (like score.py), bins every quoted
probability for 1X2/BTTS/Over-Under by the FINAL result, and reports observed hit rate per bin
against the quoted average. Suggested shifts go to <work_dir>/recalibration.json ONLY when
n >= 30 and a bin has >= 8 samples; otherwise the file says "hold".

Usage: recalibrate.py <work_dir>
"""
import json, re, sys, glob
from pathlib import Path

MIN_N, MIN_BIN = 30, 8

def main():
    work = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    res = {}
    for line in (work/"results.csv").read_text().splitlines()[1:]:
        if not line.strip(): continue
        date, h, a, hs, as_ = line.split(",")[:5]
        res[(h, a)] = (int(hs), int(as_))
    bins = {}  # (market, bin) -> [sum_p, n, hits]
    settled = 0
    for run in glob.glob(str(work/"run-*")):
        ans = Path(run)/"answer.md"; rep = Path(run)/"report.json"
        if not (ans.exists() and rep.exists()): continue
        m = json.load(open(rep)).get("match", {})
        key = (m.get("home_team",""), m.get("away_team",""))
        if key not in res: continue
        settled += 1
        hs, as_ = res[key]
        text = ans.read_text()
        hl = re.search(r"\*\*(\S[^*]+) ([0-9.]+)% / Draw ([0-9.]+)% / (\S[^*]+) ([0-9.]+)%", text)
        if hl:
            ph, pd_, pa = float(hl.group(2)), float(hl.group(3)), float(hl.group(5))
            outcome = 0 if hs > as_ else 1 if hs == as_ else 2
            for i, p in enumerate((ph, pd_, pa)):
                b = min(9, int(p/10))
                bins.setdefault(("1X2", b), [0.0, 0, 0])
                bins[("1X2", b)][0] += p; bins[("1X2", b)][1] += 1
                if i == outcome: bins[("1X2", b)][2] += 1
        g = re.search(r"Goals bet: (.+?) \(([0-9.]+)%\)", text)
        if g:
            sel, p = g.group(1), float(g.group(2))
            b = min(9, int(p/10))
            total = hs + as_
            hit = ("Over 2.5" in sel and total > 2) or ("Under 2.5" in sel and total < 3) or ("both teams to score: yes" in sel.lower() and hs > 0 and as_ > 0) or ("both teams to score: no" in sel.lower() and (hs == 0 or as_ == 0))
            mk = "BTTS" if "both teams" in sel.lower() else "O/U 2.5"
            bins.setdefault((mk, b), [0.0, 0, 0])
            bins[(mk, b)][0] += p; bins[(mk, b)][1] += 1
            bins[(mk, b)][2] += int(hit)
    out = {"settled": settled, "gate": f"n>={MIN_N} required; advising {'ON' if settled >= MIN_N else 'OFF (hold)'}", "bins": {}, "suggested_shifts": {}}
    for (mk, b), (sp, n, hits) in sorted(bins.items()):
        avg, obs = sp/n, hits/n*100
        out["bins"][f"{mk} {b*10}-{b*10+10}%"] = {"n": n, "quoted_avg": round(avg,1), "observed": round(obs,1), "gap": round(obs-avg,1)}
        if settled >= MIN_N and n >= MIN_BIN:
            out["suggested_shifts"][f"{mk} {b*10}-{b*10+10}%"] = round((obs-avg)/2, 1)   # half the gap: shrink toward honesty, never lurch
    (work/"recalibration.json").write_text(json.dumps(out, indent=1))
    print(f"settled={settled} | gate {'OPEN' if settled >= MIN_N else 'CLOSED (hold until n=30)'}")
    for k, v in out["bins"].items():
        print(f"  {k:22s} n={v['n']:2d} quoted {v['quoted_avg']:5.1f} observed {v['observed']:5.1f} gap {v['gap']:+.1f}")
    if out["suggested_shifts"]:
        print("suggested shifts (half-gap, apply in calc.py):", out["suggested_shifts"])

if __name__ == "__main__":
    main()
