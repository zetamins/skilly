#!/usr/bin/env python3
"""Ensemble blend: combine the council's answer with a second (quick-mode) answer on the SAME report.

The 28-match record showed a 50/50 blend of two independent views beat either alone (Brier 0.499 v
0.523 analyst-only). This tool does the arithmetic: parse the headline H/D/A from two answer files,
average them (50/50), and report the blended view plus a disagreement flag. It does NOT choose the
bet — the decider rules (user bet rule, fragility, gate) apply to the blended numbers.

Usage: blend.py <answer_council.md> <answer_quick.md>
"""
import re, sys

def headline(path):
    t = open(path).read()
    m = re.search(r"\*\*(\S[^*]+) ([0-9.]+)% / Draw ([0-9.]+)% / (\S[^*]+) ([0-9.]+)%", t)
    bet = re.search(r"Best bet: (.+?) \(([0-9.]+)%\)", t)
    if not m:
        return None
    return {"home": m.group(1).strip(), "ph": float(m.group(2)), "pd": float(m.group(3)),
            "away": m.group(4).strip(), "pa": float(m.group(5)),
            "bet": bet.group(1) if bet else "?", "bp": float(bet.group(2)) if bet else None}

def main():
    a, b = headline(sys.argv[1]), headline(sys.argv[2])
    if not a or not b:
        print("could not parse a headline from one of the files"); return 2
    if a["home"] != b["home"] or a["away"] != b["away"]:
        print(f"WARNING: different matches? {a['home']} v {a['away']} vs {b['home']} v {b['away']}")
    s = a["ph"] + a["pd"] + a["pa"]
    ph, pd_, pa = a["ph"]/s*100, a["pd"]/s*100, a["pa"]/s*100
    t_ = b["ph"] + b["pd"] + b["pa"]
    qh, qd, qa = b["ph"]/t_*100, b["pd"]/t_*100, b["pa"]/t_*100
    bh, bd, ba = (ph+qh)/2, (pd_+qd)/2, (pa+qa)/2
    print(f"{a['home']} v {a['away']}")
    print(f"  council: {ph:.1f} / {pd_:.1f} / {pa:.1f}   bet {a['bet']} ({a['bp']}%)")
    print(f"  quick:   {qh:.1f} / {qd:.1f} / {qa:.1f}   bet {b['bet']} ({b['bp']}%)")
    print(f"  BLEND:   {bh:.1f} / {bd:.1f} / {ba:.1f}")
    top = max(((bh, a['home']), (bd, 'Draw'), (ba, a['away'])))
    print(f"  blended most-likely: {top[1]} ({top[0]:.1f}%)")
    for lbl, x, y in (("home", ph, qh), ("draw", pd_, qd), ("away", pa, qa)):
        if abs(x - y) >= 8:
            print(f"  DISAGREEMENT {lbl}: {x:.1f} v {y:.1f} — the blend hides a real split; read both cases before betting")
    print("  (the bet itself still follows the decider rules on the blended numbers; this tool only fuses probabilities)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
