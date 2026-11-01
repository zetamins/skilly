#!/usr/bin/env python3
"""Standing scorer: for every run dir with an answer.md, find the match result (ESPN) and
maintain a cumulative calibration table. Run after matches finish: auto_score.py <work_dir>

Writes <work_dir>/results.csv (all finished answers) and prints the running table.
Answers whose match has no result yet are listed as pending. Requires score.py beside this file.
"""
import json, re, subprocess, sys, glob, urllib.request
from pathlib import Path
from datetime import datetime, timezone

LEAGUES = ["eng.1", "eng.2", "esp.1", "ita.1", "ger.1", "fra.1"]

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return json.load(urllib.request.urlopen(req, timeout=20))

def find_result(home, away, date):
    for lg in LEAGUES:
        try:
            d = get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard?dates={date}")
        except Exception:
            continue
        for e in d.get("events", []):
            comp = e.get("competitions", [{}])[0]
            if comp.get("status", {}).get("type", {}).get("state") != "post":
                continue
            names = {c["team"]["displayName"]: c for c in comp.get("competitors", [])}
            def sig(s):
                return [w for w in re.split(r"\s+", s.lower()) if len(w) > 3 and w not in
                        ("manchester", "united", "city", "real", "paris", "saint", "germain", "fc", "ac")]
            def norm(s): return re.sub(r"[^a-z]", "", s.lower())
            def hits(team, pool):
                nw = norm(pool)
                return all(norm(w) in nw for w in sig(team)) or norm(team) in nw
            if len(names) == 2 and hits(home, " | ".join(names)) and hits(away, " | ".join(names)):
                hs = next(c for n, c in names.items() if hits(home, n))
                as_ = next(c for n, c in names.items() if n != next(nn for nn in names if hits(home, nn)))
                return int(hs["score"]), int(as_["score"])
    return None

def main():
    work = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    rows, pending = [], []
    for run in sorted(glob.glob(str(work / "run-*"))):
        ans = Path(run) / "answer.md"
        rep = Path(run) / "report.json"
        if not (ans.exists() and rep.exists()):
            continue
        m = json.load(open(rep)).get("match", {})
        ko = m.get("kickoff_utc", "")[:10].replace("-", "")
        res = find_result(m["home_team"], m["away_team"], ko)
        bet = re.search(r"Best bet: (.+?) \(([0-9.]+)%\)", ans.read_text())
        if not res:
            pending.append(f"{m['home_team']} v {m['away_team']} ({m.get('kickoff_utc','?')[:10]})")
            continue
        rows.append(f"{m['kickoff_utc'][:10]},{m['home_team']},{m['away_team']},{res[0]},{res[1]}")
    csv = work / "results.csv"
    old = set(csv.read_text().splitlines()[1:]) if csv.exists() else set()
    new = [r for r in rows if r not in old]
    if new or not csv.exists():
        with open(csv, "a") as f:
            if f.tell() == 0:
                f.write("date,home_team,away_team,home_score,away_score\n")
            f.write("\n".join(new) + "\n")
    if csv.exists():
        out = subprocess.run([sys.executable, str(Path(__file__).parent / "score.py"),
                              "--answers", str(work), str(csv)], capture_output=True, text=True)
        for line in out.stdout.splitlines():
            if any(k in line for k in ("Hit rate", "Brier (", "picks hit", "Settled")):
                print(line)
    print(f"\nscored {len(rows)} results ({len(new)} new); pending: {len(pending)}")
    for p in pending:
        print("  -", p)

if __name__ == "__main__":
    main()
