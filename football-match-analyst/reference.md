# Reference (football-match-analyst)

Read only when the sheet prints no usable anchor, or when auditing/calibrating. For a routine run the SKILL.md protocol is sufficient.

## Forming your own expected goals (when the sheet prints no anchor)
Blend these by judgement, then apply the venue edge (home x1.10 / away x0.91 when the venue is in the home side's country; give the edge to the away side when the label contradicts the venue; none at a neutral venue). Cap sanity: a combined expectation above ~6 goals is a data error, not a match.
| source | built from | guidance |
|---|---|---|
| xG | shrunk xG for/against per game, attack x opposing defence | strongest single source when 8+ games exist |
| results | last 10, recency-weighted (0.9 decay, friendlies x0.7), shrunk toward the league mean | robust when xG missing |
| strength | Elo gap (half weight if form-only) + squad value ratio -> expected goal difference | best for cross-league ties and early season |

Shrink small samples toward the league mean (a 4-game xG average is half evidence, half prior). The league's own scoring rate sets the goal level (LaLiga ~2.54, Premier League ~2.88; internationals ~3.08).

## Team-news pricing
Absentee impact = the player's share of the side's xG (attackers by xG share; defenders/keepers by the xGA share they protect; half-weight midfielders) minus what the replacement adds. A side's total move from absences rarely exceeds +-0.30. An absentee not in the squad list has unknown impact: name it as a data gap, never price it.

## Evidence lines in the sheet
Form letters, per-side results/xG/ratings/table/stakes/rotation/fatigue/manager/availability, venue and weather, referee, travel, H2H (with its n and a RELEVANT/not verdict), confirmed-or-guessed lineups, set-piece numbers, error-prone players, UNDERDOG STRENGTH count. Quote them, with their numbers; a 2-3 game rate is thin and labelled thin.

## Measured baselines from our corpus (104 StatsBomb matches: WC 2018 + La Liga 2015/16 sample)
Computed from `~/football-corpus.local/datasets/statsbomb/` (script-driven; never read the JSONs raw):
- Result split: home win 48.1%, draw 20.2%, away win 31.7% across the mixed corpus — but split by competition the league sample (La Liga 15/16, 40 matches) is much more home-heavy: **57.5% home / 22.5% draw / 20.0% away**, while the WC 2018 is 48.1/20.2/31.7. The venue edge is worth more in domestic league play (real grounds, no neutral designations); use the league split as the prior for club games and the WC split for internationals/neutral venues.
- Comeback wins (side conceding first) are ~12.5-13% in BOTH samples — a universal base rate, no league/international adjustment.
- Goal environment: 2.88-2.92 goals/match; ~63% of goals in the 2nd half.
- Game state: the side scoring first won 69.3%; the trailer won only 12.9% — comebacks are rare, treat comeback cases as exceptional.
- Set plays: ~21% of goals came from set plays including penalties.
- League matches between equals are decided by shot quality (box share), not shot volume — the WC upset pattern (volume with the loser) reverses in open league games; full league analysis in `~/football-corpus.local/reports/league-laliga-analysis.md`.
- Calibration: sum of StatsBomb xG = 305.9 vs 300 actual goals (ratio 0.98) across 2,657 shots — vendor per-match xG totals are a trustworthy anchor; per-shot noise under ~0.05 xG is not meaningful.
Caveat: small, mixed-competition sample; use as a sanity band, not as fitted parameters.
