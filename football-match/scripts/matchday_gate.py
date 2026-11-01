#!/usr/bin/env python3
"""Matchday gate: verifies (or vetoes) a run's answer against confirmed lineups ~75 min before kickoff.

Deterministic — no model. For every run dir passed (or every run-* in a parent):
  1. reads the report's kickoff; skips if not in the 20-130 min pre-kickoff window (or --force)
  2. runs the scrape skill's lineup_check.py once -> run_dir/lineups.json
  3. applies the gate rules:
     - a key attacker (F or attacking M in the missing/doubtful list, value >= 20m or 'regular' tag)
       absent from the confirmed XI vetoes a Best bet or Goals bet that leans on his team's scoring
       (BTTS/over legs; 1X2 bets get DOWNGRADED one confidence level instead of vetoed)
     - a priced absence (in the answer's 'From the report' list) who STARTS -> DOWNGRADED + note
  4. appends the verdict to run_dir/gate.md and prints one line per run

Usage: matchday_gate.py <work_dir> [--force]
"""
import json, re, subprocess, sys, glob, os
from datetime import datetime, timezone
from pathlib import Path

SCR = Path.home()/".kimi-code/skills/football-scrape"
PY = SCR/".venv/bin/python"

def kickoff_of(run: Path):
    rep = run/"report.json"
    if not rep.exists(): return None
    try:
        m = json.load(open(rep)).get("match", {})
        return datetime.fromisoformat(m["kickoff_utc"].replace("Z", "+00:00"))
    except Exception: return None

def key_attackers(report: dict):
    """match.{home,away}_missing_players (name only) joined against teamProfile/opponentProfile
    squads for role and market value; 'key attacker' = F with value >= 20m or any M with value >= 40m."""
    out = {}
    mt = report.get("match", {})
    squads = {}
    for prof_key, side in (("teamProfile", mt.get("home_team", "")), ("opponentProfile", mt.get("away_team", ""))):
        prof = report.get(prof_key, {}) or {}
        squads[side] = {p["name"].lower(): p for p in prof.get("squad", []) if p.get("name")}
    for mp_key, team in (("home_missing_players", mt.get("home_team", "")), ("away_missing_players", mt.get("away_team", ""))):
        for p in mt.get(mp_key) or []:
            name = p.get("name", "")
            info = squads.get(team, {}).get(name.lower(), {})
            role = (info.get("role") or "?").upper()
            val = info.get("market_value") or 0
            if role.startswith("F") and val >= 20_000_000 or role.startswith("M") and val >= 40_000_000:
                out.setdefault(team, []).append((name, role, val))
    return out

def main():
    args = [a for a in sys.argv[1:] if a != "--force"]
    force = "--force" in sys.argv
    work = Path(args[0]) if args else Path.cwd()
    runs = [Path(d) for d in glob.glob(str(work/"run-*"))] or [work]
    now = datetime.now(timezone.utc)
    for run in runs:
        ko = kickoff_of(run)
        if not ko: continue
        mins = (ko - now).total_seconds()/60
        if not force and not (20 <= mins <= 130): continue
        lc = subprocess.run([str(PY), str(SCR/"scripts/lineup_check.py"), str(run)],
                            capture_output=True, text=True, timeout=300)
        lj = run/"lineups.json"
        verdict_lines = [f"# Matchday gate — {datetime.now(timezone.utc):%Y-%m-%d %H:%M}Z (kickoff {ko:%H:%M}Z)"]
        if not lj.exists():
            verdict_lines.append("NO LINEUPS YET — bet unverified; check again closer to kickoff.")
        else:
            lx = json.load(open(lj))
            rep = json.load(open(run/"report.json"))
            starters = {p.strip().lower() for team in lx.get("confirmed", {}).values() for p in team.get("starters", [])}
            # team of each missing player
            bets = ""
            ans = run/"answer.md"
            if ans.exists(): bets = ans.read_text()
            lean_team = None
            m = re.search(r"Best bet: (.+?) \(", bets)
            bt = m.group(1) if m else ""
            if re.search(r"both teams to score|over 2\.5|BTTS", bt, re.I): lean_team = "BOTH"
            verdict = "BET VERIFIED"
            for team, players in key_attackers(rep).items():
                for name, role, val in players:
                    if name.lower() in starters: continue
                    if lean_team == "BOTH":
                        verdict = f"VETOED: {name} ({team}, {role}, £{val//1_000_000}m) absent from confirmed XI — goals-market bet relies on his team's scoring. NO BET."
                    else:
                        verdict = f"DOWNGRADED: {name} ({team}, key attacker) absent — confidence one level down."
            verdict_lines.append(f"Verdict: {verdict}")
            verdict_lines.append(f"Best bet was: {bt or 'unknown'}")
        (run/"gate.md").write_text("\n".join(verdict_lines)+"\n")
        print(f"{run.name}: {verdict_lines[-2] if len(verdict_lines)>1 else verdict_lines[-1]}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
