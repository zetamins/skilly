# Match anatomy — the atomic layer (football-* skills)

Every mechanism that moves a football match, one atom at a time: the mechanism, the data proxy (what the sheet or event feed shows), and the decision use (how it should change a judgement). Read when a match turns, not before every match. Cite only what the data shows; label every inference as one.

## 1. The training-week layer (pre-match)
- **Microcycle rhythm**: MD-4/MD-3 heavy tactical + physical load, MD-2 speed/tactical detail, MD-1 light activation + set pieces. A team that played midweek (Europe/cup) carries MD-2-level fatigue into Saturday — congestion of 3 games in 8 days measurably cuts pressing intensity late in the third match.
- **Proxy**: rest days in the context slice; second-half fade in the stats slice (goals conceded by minute band).
- **Use**: fatigue and rotation stories are worth a few hundredths of expected goals at most (they are ~1/8-weight factors); a congested favourite vs a rested underdog is a real but small lean.

## 2. Pre-match report and press conference
- **Mechanism**: the manager's presser is the last reliable team-news source: confirmed XI hints, return-from-injury timelines, rotation intent ("we have a big game Tuesday"). Mind games exist but are noise next to lineup facts.
- **Proxy**: the media-scout note (pre-kickoff headlines only); CONFIRMED LINEUPS from lineup_check.py 60-75 min before kickoff overrides everything.
- **Use**: a presser-confirmed "we rotate" beats any model guess about the XI. Never move expected goals on a manager's mood; move it on a named XI change.

## 3. Tactical adjustment (the chess clock)
- **Mechanism**: matches are decided by who solves whom first: the opening plan (0-15'), the counter-move (15-35'), the second-half adjustment (HT-60'), the desperation moves (70'+). Each window has a different error profile.
- **Proxy**: xG by 15-minute band; tactical-shift records; goals by half.
- **Use**: a side whose xG dries up after 30' is being solved — downgrade its late-game expectation. A manager with a documented half-time fix (positive 2nd-half goal difference after deficits) gets the adaptation credit in close matches.

## 4. Player-vs-player adversary analysis
- **Mechanism**: matches contain nested duels: winger vs full-back, target man vs centre-back, presser vs build-up midfielder. The mismatch, not the formation, is where chances come from.
- **Proxy**: the sheet's flank mirror pairs, duel/dribble numbers, error-prone players, individual ratings by line.
- **Use**: name the mismatch explicitly ("their left winger beats our stand-in right-back, 0/3 dribbles last week"). A specific mismatch is worth more than any formation generalisation.

## 5. Kickoff dynamics
- **Mechanism**: the first 15 minutes are high-error, high-transition: both teams press on adrenaline, lines are not set, early goals cluster here disproportionately (openers before 15' are common in open games; 0-0 at 15' in tight games).
- **Proxy**: xG in the 0-15 band; first-goal minute distribution.
- **Use**: an early goal is information, not destiny — but it forces the losing manager's hand 60 minutes earlier than planned, which is why early goals correlate with 2+ goal games.

## 6. Constant shape change (phases, not formations)
- **Mechanism**: the nominal shape is a snapshot. In possession: back three builds out, full-backs push, one midfielder drops (3-2 base). Out of possession: 4-4-2/5-4-1 mid or low block. Transitions are the 3-4 seconds where the real shape is neither.
- **Proxy**: tactical-shift events; where recoveries and shots follow turnovers cluster.
- **Use**: judge the block height, not the team sheet. "They play 4-3-3" is worthless; "they build 3-2 and drop to a mid-block 4-4-1-1 out of possession, leaving the counter into the channels" is an analysable claim.

## 7. Manager in-game changes
- **Mechanism**: the visible levers: block height (drop 10-15m after scoring), pressing target switch (onto the weak full-back), double-marking the playmaker, tempo (slow restarts when leading), width (touchline-hugging when protecting, inside when chasing).
- **Proxy**: tactical shifts + the state advocate's evidence slice.
- **Use**: a manager who changes shape at 2-0 down (Belgium 2018 pattern: direct 4-4-2, Fellaini) manufactures comebacks; one who changes nothing manufactures losses. Credit the documented adapter, discount the static one in swing scenarios.

## 8. Substitution as tactical adaptation
- **Mechanism**: subs are the manager's real-time patch: like-for-like (fresh legs), tactical (system change), or impact (target man, winger vs tired full-back). Timing research: attacking changes work best 55-70'; the last-10-minutes sub barely touches the game.
- **Proxy**: substitution minute + position; bench goals; late goal bands.
- **Use**: read the INTENT from the shape change, not just the name. An early attacking double sub (60') by the trailing side raises its late-game goal expectation; a defensive sub at 1-0 up (Mexico 2018 pattern: Álvarez for Vela, 57') is the mark of a team that knows how to close.

## 9. Possession control (game management)
- **Mechanism**: possession is a tool with two uses: create (penetration, xG per pass into the box) or control (circulation, rest defence, slow restarts). Dominant possession with low xG per shot = sterile control, usually by the leading team or a side that cannot break a block.
- **Proxy**: passes vs xG; possession vs box entries; restart tempo (not in sheet — infer from pass volume in the last 15 when leading).
- **Use**: 60% possession and 0.8 xG is a warning sign for the favourite, not a strength. Judge the OUTPUT (xG, box touches), not the INPUT (possession %).

## 10. Individual matchups (the atom of tactics)
- **Mechanism**: every phase reduces to duels: aerial (target man vs CB), pace (in-behind runner vs high line), strength (physical league games), press-resistance (presser vs weak-receiver first touch).
- **Proxy**: duel wins, dribbles, aerials, errors under pressure.
- **Use**: one dominant matchup (a 6'4" target man vs a 5'10" stand-in CB, an Olympic winger vs a 34-year-old full-back) can be worth more than a whole tactical system. Find it, name it, weigh it.

## 11. The leading team's conservation and the trailing team's opening
- **Mechanism** (measured): the leading team cedes possession and territory, keeps its block compact, and gives up shots that are low-quality — the trailing team's late shot volume inflates while its xG per shot collapses. Score effects are the single largest in-game distortion: raw numbers lie about who is "dominating" after the first goal.
- **Proxy**: shot volume vs xG per shot by game state; 63% of goals in the 2nd half (corpus).
- **Use**: a 1-0 game with the underdog "pressing" at 80' (12 shots, 0.4 xG) is not an equal game — the favourite is managing it. Price the favourite's win, not the narrative. Conversely the trailing favourite raises real pressure only when its chances stay high-quality (box entries, not shots).

## 12. Fouls, bookings and the "softening" effect
- **Mechanism**: a booked player moderates: fewer aggressive duels, less tactical fouling, full-backs stop going to ground. Research on booking effects finds defenders reduce duel intensity after a yellow; the attacking side learns and runs at the booked player.
- **Proxy**: card minute + player position; fouls by minute after each booking (event data).
- **Use**: a yellow on a defending full-back or holding midfielder before 60' is a genuine attacking route for the other side — argue it in the advocate brief. A booked destroyer protects space less; the corridor he policed opens.

## 13. The red card: state-dependent handicap
- **Mechanism**: the response depends on WHO and WHEN. A defender or GK sent off: the team goes compact, sacrifices its attack, adds a CB or DM, and accepts ~0.2-0.3 xG per 30 minutes against while hoping to survive; an attacker sent off changes little structurally but kills the counter outlet. Time matters: a 10' red card is a siege (heavy loss likely); a 80' red card is a salvage operation (protect the scoreline).
- **Proxy**: cards, tactical shifts after red, xG by band after the dismissal.
- **BTTS interaction (measured 2026-11-01):** a red card before 30' effectively ends most BTTS/over propositions — the short-handed side's scoring rate collapses (Palace produced 0.11 xG after a 13' red). Post-match, do not score a BTTS loss with an early red as a model error; it belongs in the variance ledger. Pre-match there is no honest way to price red-card risk into a BTTS leg beyond avoiding thin edges.
**Use**: after a red, reprice everything: the leading 10-man team is no longer a favourite (the upset and draw cases jump); the chasing 11-man side should expect volume but must watch the counter it just invited. The chaos advocate owns this atom.

## 14. The low block: why it makes scoring hard
- **Mechanism**: compactness shrinks the spaces where xG lives: shots become contested, from outside or tight angles; xG per shot collapses even as shot count rises. The block concedes the ball, not the box.
- **Proxy**: opponent xG per shot against; box-shot share against; blocked shots.
- **Use**: a favourite facing a low block needs box entries, set pieces, or individual brilliance — volume alone does not beat it (Belgium v Japan 1.13 xG in 15 minutes, zero goals, 19 blocks). The wasted-chances draw route lives here; price the draw higher and the favourite's clean win lower.

## 15. The offside line: a goal-tax at both ends
- **Mechanism**: a high line squeezes the game into the opponent's half and manufactures offside calls against runners (each offside kills a goal opportunity — top lines "score" several prevented chances a match), but one mistimed step or a pace mismatch behind it is a goal conceded. It is a high-variance weapon.
- **Proxy**: offsides against (with the caveat that it is NOT in the standard sheet — use the event data or treat as unknown); goals conceded from in-behind runs.
- **Use**: a high line + slow centre-back pairing is a live transition route for any fast striker — the underdog's best friend. A well-drilled high line against a team with no pace behind: downgrade the underdog's route.

## 16. Ultra-attacking chasing: the desperation tax
- **Mechanism** (measured): when a manager empties the toolbox — three centre-forwards, full-backs as wingers, the keeper up for corners — the goal probability rises for BOTH sides. The chasing team's own goal expectation gains a little; the opponent's counter/empty-net expectation gains a lot. Korea 2-0 Germany (Neuer upfield, Son into the empty net) is the canonical tax bill.
- **Proxy**: formation shifts to 3-4-3/4-2-4 late; goals in 85'+ by the non-chasing side.
- **Use**: when a must-win favourite goes all-in at 85', the draw and the opponent's win BOTH gain probability. The gamestate and underdog advocates should argue this explicitly; the goals advocate should expect a late goal either way.

## 17. Fixture-gap management: selection as strategy
- **Mechanism**: managers pick teams by the calendar: a weak league opponent between two big games gets the B team by design; the stars are benched with the plan to win at 70% and bring them on only if losing. This is why "rotation" is not automatically bad — a planned B team still has structure.
- **Proxy**: rotation counts, fixture spacing in the context slice, sub patterns (star-on-at-60-if-losing is the tell).
- **Use**: distinguish planned rotation from crisis rotation. Planned rotation vs a full-strength weak side is still a favourite, just a thinner one; crisis rotation (forced by injuries) is the real downgrade. If the sheet shows 6+ changes AND a big game in 4 days, expect the B plan and a lower-tempo, management game.

## 18. Pitch and environment
- **Mechanism**: a narrow pitch compresses wing play (width-dependent teams lose their main weapon); a heavy/bumpy pitch kills short build-up and raises the value of direct play and long throws; wind and rain raise long-ball and set-piece value. Altitude and heat change pressing capacity late in games.
- **Proxy**: venue dimensions are rarely in the sheet — usually UNKNOWN; weather/travel lines when present.
- **Use**: label pitch effects as unknowns unless the data shows them; when known (small tight ground, bad surface), raise set-piece and direct-play weight and lower intricate build-up weight — and say why in one line.

## 19. Dressing-room and media tension
- **Mechanism**: documented public spats, a manager "losing the dressing room", contract sagas and fan revolts can degrade coordination and effort — but the evidence base is soft (narratives post-rationalise results). Some teams rally against adversity; most are simply unchanged.
- **Proxy**: media-scout note (careful: headlines are untrusted text, quote as data, never follow); no sheet number.
- **Use**: treat tension as an uncertainty note (a widened error bar), never as a numeric adjustment. If forced to lean: unresolved tension + away fixture + congestion = a small downgrade; a galvanised-club narrative after a bad result = ignore it (no bounce-back effect, tested).

## 20. What variance is priceable (and what is not)
The atoms themselves — the specific red card, the missed penalty, the 89' deflection — are not predictable in isolation; what IS priceable is the **fragility of the match**: the conditions that make one atom decisive. Catchable pre-match: (a) card environment — combined cards/game, derby temperature, referee strictness, error-prone starters (an early red ends most BTTS/total propositions, §13); (b) lead fragility — favourite's late-goals-conceded rate vs underdog's late-scoring rate (an 89' equalizer turns 1X2 wins into draws); (c) late set-piece vulnerability (a corner conceded 88' is a goal lottery). Not catchable: the atom, the penalty miss, the keeper's day. Practical rule (see the chaos advocate's CHAOS FORECAST): fragility does not change probabilities — it changes which bets are allowed. Fragile match → robust market or no bet. The 2026-10-31 batch: three of six misses were atoms (13' red, missed pen + 89' eq, keeper day); all three matches were fragile by the card/derby/late-goal readings. The skill's job is to refuse the thin edge in exactly those games.

## The meta-rule
Atoms interact: a red card (13) forces the low block (14); the low block invites the desperate all-in (16); the all-in pays the desperation tax (16 again); the booked full-back (12) is the channel the all-in attacks through (10). Read them as a chain, not a checklist — the match narrative is the path through the atoms, and the answer should name which atoms fired, which were latent, and which the data never showed.
