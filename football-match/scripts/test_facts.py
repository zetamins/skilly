#!/usr/bin/env python3
"""Regression harness for facts.py: golden-file diff on saved reports.

    test_facts.py          # diff facts.py output against golden/*.txt on the saved reports
    test_facts.py --update # regenerate the golden files after a DELIBERATE change

Any diff is a behaviour change: either a bug or an intended edit. There is no third kind.
Reports are referenced by the golden file name prefix:
  report*                -> /home/seerish/retest/run-chelsea/report.json
  dortmund-2026-10-31*   -> the batch output dir
  fulham-2026-10-31*     -> the batch output dir
"""
import subprocess, sys
from pathlib import Path

HERE = Path(__file__).parent
GOLD = HERE/"golden"
SOURCES = {
    "report": "/home/seerish/retest/run-chelsea/report.json",
    "dortmund": "/home/seerish/football-batch/output/dortmund-2026-10-31T11-55-59-108Z.json",
    "fulham": "/home/seerish/football-batch/output/fulham-2026-10-31T06-30-48-319Z.json",
}

def source_for(golden_name: str):
    for prefix, path in SOURCES.items():
        if golden_name.startswith(prefix):
            return path
    return None

def main():
    update = "--update" in sys.argv
    fails = 0
    for g in sorted(GOLD.glob("*.txt")):
        src = source_for(g.name)
        if not src or not Path(src).exists():
            print(f"SKIP {g.name} (no source report)"); continue
        out = subprocess.run([sys.executable, str(HERE/"facts.py"), src],
                             capture_output=True, text=True, timeout=300).stdout
        if update:
            g.write_text(out)
            print(f"UPDATE {g.name}")
            continue
        want = g.read_text()
        if out == want:
            print(f"PASS {g.name}")
        else:
            fails += 1
            wl, ol = want.splitlines(), out.splitlines()
            diffs = [f"  line {i+1}:\n    golden: {wl[i][:120]}\n    now:    {ol[i][:120]}"
                     for i in range(min(len(wl), len(ol))) if wl[i] != ol[i]][:6]
            print(f"DIFF {g.name} ({len(wl)} v {len(ol)} lines)")
            print("\n".join(diffs))
    if not update:
        print(f"\n{'OK — no behaviour change' if fails == 0 else str(fails) + ' file(s) changed — intended edit? regenerate with --update'}")
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(main())
