# skilly — Football analysis skills for AI coding agents

15 agent skills that turn an AI coding harness into a professional football analysis pipeline:
scrape a match report from up to 13 public sources, then analyse it market-blind through a
council of specialist notes and seven blind advocates, with a decider, independent reviewers,
closing-odds capture and automatic post-match scoring.

## What's here

| Skill | Role |
|---|---|
| `football-scrape` | One team's next match: report JSON from up to 13 sources (guarded runner) |
| `football-match` | **The main skill.** Two modes: council pipeline (default) and quick single-agent |
| `football-match-analyst` | Odds-benchmark variant: audit + odds challenge (needs no bookmaker input to the forecast) |
| `football-team-news` / `football-tactical-matchup` / `football-underlying-stats` / `football-context-motivation` / `football-media-scout` | Specialist notes (one slice of the facts sheet each) |
| `football-home/away/draw/goals/underdog/gamestate/chaos-advocate` | The seven-advocate blind council |
| Shared scripts (`football-match/scripts/`) | facts.py (the sheet), calc.py (Poisson markets), check.py, review.py, blind.py, value.py, score.py, run_collection.py (the pipeline runner), matchday_gate.py (lineup gate), auto_score.py (results → calibration), recalibrate.py (gated), blend.py (ensemble) |

Every step is checkpointed to disk and validated by a checker script; a crash resumes where it stopped.

## Install

```bash
git clone git@github.com:zetamins/skilly.git
cd skilly
./install.sh all        # or: kimi | claude | codex | opencode
```

The installer puts a canonical copy in `~/.football-skills` and symlinks the skills into each
harness's skills directory (Kimi Code, Claude Code `~/.claude/skills`, Codex `~/.codex/skills`,
OpenCode `~/.config/opencode/skills`). One update, every harness. The shared scripts anchor on
`~/.kimi-code/skills` (created by the installer even if you only use other harnesses).

Manual alternative: copy (or symlink) the `football-*` directories into your harness's skills
folder and make sure `~/.kimi-code/skills/football-match/scripts/` resolves.

### Optional dependencies
- Live scraping (`football-scrape`): `python3 -m venv ~/.venvs/football-scrape && ~/.venvs/football-scrape/bin/pip install 'httpx[http2]' playwright && ~/.venvs/football-scrape/bin/python -m playwright install chromium`
- The council pipeline spawns agents via an agent CLI it already knows: opencode, claude, or codex.
- Everything else is Python standard library only.

## Use

"Analyse Arsenal" (or any team / match) — the scrape skill hands off automatically to the
full council pipeline. Say "quick mode" for the single-agent pass.

## Method in one paragraph

Market-blind by construction: the runner strips bookmaker odds before any agent reads the
report; analysts set their own expected goals from rating/xG anchors (which move only for
team news); a calculator turns them into every market's probabilities; seven advocates argue
the home, away, draw, goals, underdog, game-state and chaos cases blind to each other and to
the odds; a decider chairs; two reviewers check; value is judged against the market only after
the answer exists. Calibration is tracked per market and league, with chaos-decided matches
(red cards, missed penalties, 89' equalizers) kept in a separate variance ledger so losses
teach the right lessons.

## License

MIT — see LICENSE. Scraping is your responsibility: respect each source's terms and the
runner's politeness rules (one live run at a time, no retries after blocks).
