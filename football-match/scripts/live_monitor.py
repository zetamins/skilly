#!/usr/bin/env python3
"""Live match monitor: watches a match through the scrape skill's Sofascore browser session,
tracks goals / red cards / penalties, and reprices the 1X2 with a simple in-play model
(remaining-time-scaled Poisson from the pre-match lambdas, with a red-card adjustment:
the short-handed side's rate x0.65, the other side x1.15).

This is the honest live edge: the red card is not predictable pre-match, but a 13' red card
IS information — the reprice after it is arithmetic, not prophecy.

Usage: ~/.venvs/football-scrape/bin/python live_monitor.py <report.json or run_dir> [pre-match lambdas H A]  (needs the scrape venv)
  (lambdas default to the values found in <run_dir>/decision.md or answer.md, else 1.4-1.2)
Polls ~every 60 s until full time. Ctrl-C to stop.
"""
import asyncio, json, math, re, sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, "/home/seerish/.kimi-code/skills/football-scrape/scripts")
from football.sites.sofascore import _session_page, _fetch_json, _find_team   # noqa: E402

def poisson_1x2(lh, la, minutes_left, reds):  # reds: (home_sent_off, away_sent_off)
    scale = max(0.0, minutes_left) / 90.0
    fh = 0.65 if reds[0] else 1.0
    fa = 1.15 if reds[0] else 1.0
    gh = 0.65 if reds[1] else 1.0
    ga = 1.15 if reds[1] else 1.0
    eh = lh * scale * fh * ga
    ea = la * scale * gh * fa
    ph = sum(math.exp(-eh) * eh**i / math.factorial(i) * sum(math.exp(-ea) * ea**j / math.factorial(j) for j in range(i)) for i in range(1, 8))
    pa = sum(math.exp(-ea) * ea**j / math.factorial(j) * sum(math.exp(-eh) * eh**i / math.factorial(i) for i in range(j)) for j in range(1, 8))
    return ph*100, (100 - ph*100 - pa*100), pa*100

def default_lambdas(path: Path):
    for cand in (path/"decision.md", path/"answer.md"):
        if cand.exists():
            m = re.search(r"expected goals ([0-9.]+)-([0-9.]+)", cand.read_text())
            if m:
                return float(m.group(1)), float(m.group(2))
    return 1.4, 1.2

async def main():
    arg = Path(sys.argv[1])
    report = arg/"report.json" if arg.is_dir() else arg
    d = json.load(open(report))
    m = d["match"]
    lh, la = (float(sys.argv[2]), float(sys.argv[3])) if len(sys.argv) > 3 else default_lambdas(arg if arg.is_dir() else report.parent)
    print(f"monitoring {m['home_team']} v {m['away_team']} (pre-match lambdas {lh:.2f}-{la:.2f})")
    reds = [0, 0]
    async with _session_page() as page:
        team = await _find_team(page, m["home_team"])
        evs = await _fetch_json(page, f"https://www.sofascore.com/api/v1/team/{team.id}/events/last/0")
        hit = [e for e in evs["events"] if m["away_team"].split()[-1].lower() in (e["homeTeam"]["name"] + " " + e["awayTeam"]["name"]).lower()
               and abs(e.get("startTimestamp", 0) - datetime.fromisoformat(m["kickoff_utc"].replace("Z", "+00:00")).timestamp()) < 86400][0]
        eid = hit["id"]
        seen = set()
        while True:
            evs2 = await _fetch_json(page, f"https://www.sofascore.com/api/v1/team/{team.id}/events/last/0")
            ev = [e for e in evs2["events"] if e["id"] == eid][0]
            status = ev["status"]["description"]
            hs, as_ = ev["homeScore"]["current"], ev["awayScore"]["current"]
            minute = ev.get("time", {}).get("currentMinute") or 0
            try:
                inc = await _fetch_json(page, f"https://www.sofascore.com/api/v1/event/{eid}/incidents")
            except Exception:
                inc = {"incidents": []}
            for it in inc.get("incidents", []):
                key = it.get("id") or f"{it.get('incidentType')}{it.get('time')}{it.get('player',{}).get('name') if isinstance(it.get('player'), dict) else ''}"
                if key in seen: continue
                seen.add(key)
                t = it.get("incidentType"); txt = it.get("incidentClass") or ""
                side = it.get("isHome") and m["home_team"] or m["away_team"]
                if t == "card" and "red" in txt.lower():
                    reds[0 if it.get("isHome") else 1] = 1
                    print(f"  [{it.get('time')}''] RED CARD {side} — repricing 10v11")
                elif t == "penalty" and it.get("isConfirmed"):
                    print(f"  [{it.get('time')}''] PENALTY {side}")
                elif t == "goal" and txt != "disallowed":
                    print(f"  [{it.get('time')}''] GOAL {side}")
            ml = max(0, 95 - minute)
            p = poisson_1x2(lh - hs * (lh/ (lh+la)) * 0, la, ml, reds)  # lambdas stay pre-match; goals scored enter via the score? kept simple: report from here on
            print(f"{minute}'  {m['home_team']} {hs}-{as_} {m['away_team']}  |  reds {reds[0]}v{reds[1]}  |  from here: {p[0]:.0f}%/{p[1]:.0f}%/{p[2]:.0f}  |  {status}")
            if status.lower() in ("ended", "full time", "ft", "after penalties"): break
            await asyncio.sleep(60)
asyncio.run(main())
