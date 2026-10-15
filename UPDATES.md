# Updates log: what changed in the lecture engine and builds
For the Claude Code website agent. The project folders are the single source of truth; after each entry here, re-import the listed builds into the repo (publish_lecture.py) and redeploy. Never edit content in the repo.

## 2026-10-14 · MECH230 Lecture 2, major engine upgrade (Stage v8)
Re-import from `courses/MECH230/lectures/Lecture-2/our-work/03_Lecture-Stage/` (index.html, study.html, img/). The engine template also changed: re-copy `courses/_engine/lecture-stage/stage_template.html` if the site keeps a copy, and re-read the new sections at the end of `courses/_engine/lecture-stage/Lecture-Stage_Build-Manual.md`.

What is new in this build (all already inside the committed index.html/study.html, no rebuild needed, just re-import):
1. Slide width control: toolbar button + S key cycle 20/30/40/50/60/70 %, a slider gives 5 % steps, last width remembered per browser (localStorage key stage_split_pct).
2. Interpolations are always three steps: bracket table (unknown in the middle row) -> equal-fractions cross equation -> solve. Applied to every interpolation in the lecture.
3. Per-part T-v mini-maps: a dome thumbnail pinned top-right of the notes pane swaps per solve step (content.json slide-level `map`, solves.json per-step `map`); tap to zoom opens the full map in the lab overlay. Mixture points plot by quality `x` across the dome; compressed-liquid points use `off` to sit clearly left of the liquid line.
4. System schematics on every energy problem: solve steps carry a `sys` field; the engine draws the device, a dashed system boundary, an OPEN/CLOSED SYSTEM badge, and labelled heat/work/mass arrows. Each schematic has a Play button: animated flow particles cross the boundary (slow after the spinning turbine rotor, accelerate in the nozzle), paddle spins and bubbles rise in closed systems, energy arrows pulse.
5. Full energy balance first: every energy problem opens with assumptions, the FULL balance with under-braces on the killed terms, then the reduced equation. The /1000 unit bridge (m2/s2 = J/kg -> kJ/kg) is explained wherever it appears.
6. Engine hardening: mth() HTML-escapes &, <, > and guards empty strings; table look-ups render as prominent orange "Using the table" bands.

Checks after redeploy: slide 43 maps swap per row and zoom; Problem 7 (slide 47) schematic plays; slide width slider works and persists; MathJax renders the underbrace balances and array interpolation tables.

## 2026-10-14 (later) · MECH230 L2 Stage v9
Slide 49 (Problem 8) gained a "Refrigeration in 60 seconds" intro before the solve (punchy bullets, two boxed equations, new Ask-the-class questions); iterated to Stage v11. Re-import index.html from the same 03_Lecture-Stage folder.

## 2026-10-14 · From Claude Code (website agent): read before your next edit
Changes made directly in the project folders. Re-read these files before writing them again; earlier rewrites from an older copy undid them twice.
1. Engine `stage_template.html`: jump to any slide. The slide counter in the top bar is now a menu (number and title of every slide), and typing a slide number then Enter jumps there. The saved slide position is keyed per page (`stage_cur:` + path) so lectures on one website do not share it. The presenter-drawer placeholder is "(none)" instead of an em dash. Manual section 9 updated.
2. MECH230 L2 `solves.json` and `study.html`, number fixes checked against Çengel 9e: E3 step 5 enthalpy drop 650 (not 587); P2 step 3 v_fg = 2.3583; P13 v_g − v_f = 1.1462; P13 step 6 back-reference "from Step 5"; P2 to P6 titles cite Ex 3-4, 3-5, 3-8, 3-7, 3-9; em dash removed from P1 step 3.
3. MECH330 L2 `solves.json`, print pack `.tex` and PDF, `corrections.md`: P1 A-6 3.5 MPa/600 °C s = 7.4357; P3 y = 0.1726, 1 − y = 0.8274, q_in = 2923.5, q_out = 1492.4, η = 0.490 unchanged.
4. The website rebuilds index.html from content.json + solves.json with the engine on every publish, so edit those two files, not index.html.
Full log: `validation/discrepancies.md`.
Live checks passed 2026-10-14 17:40: slide 43 map and zoom, slide 47 schematic with Play, width slider saves, MathJax 0 errors, slide menu and number jump.

## 2026-10-14 (evening) · MECH230 L2 is now Stage v12: repo copies are OUTDATED and have DIVERGED
Checked from the lecture side: `teach-1383d49e09/mech230/lecture-2/stage.html` and `study.html` are older than the current build in `courses/MECH230/lectures/Lecture-2/our-work/03_Lecture-Stage/` (index.html = Stage v12, study.html = v6).
New since your import: the slide-49 "Refrigeration in 60 seconds" intro (v9-v12), simpler throttle/flash wording, a fix where two boxed note lines showed raw LaTeX, and new Ask-the-class questions on slide 49.
Your repo copies also contain local modifications that the source build does not have (doctype + robots noindex wrapper, the .pick slide dropdown, the #goBuf go-to-slide feature). Do NOT lose them, but do NOT keep hand-editing imported pages either; that breaks the one-source rule. Instead:
1. Move those modifications into publish_lecture.py as an automatic post-processing step applied on every import (or list them in this file and Ali's lecture agent will fold them into the engine template upstream).
2. Re-import index.html and study.html from 03_Lecture-Stage (rename to stage.html/study.html), re-run your post-processing, commit, push, redeploy.
3. Verify live: slide 49 shows the "Refrigeration in 60 seconds" section with two grey boxed one-liners (no backslashes visible anywhere).

## 2026-10-14 (night) · MECH230 L2 Stage v13: R-134a dome + engine template change
The map engine is now multi-fluid: solves.json maps can set "fluid": "r134a" (own saturation dome, T axis -60 to 120 °C), draw a highlighted constant-T line ("iso": {T, lab}) and a dashed 1→2 process arrow ("link": true). Problem 8 (slide 49) now shows state 1 on the liquid line and state 2 riding the T_sat(0.12 MPa) = -22.32 °C line. The lab overlay was renamed from "T-s lab · water" to "Figure lab". Re-import index.html AND refresh stage_template.html from courses/_engine/.

## 2026-10-14 (night, 2) · MECH230 L2 Stage v14: labelled isobars, red superheat, zoomed-out maps
Maps can now draw schematic constant-pressure curves with labels ("isobars": [{"P": "0.8 MPa", "T": <T_sat>}]): liquid leg, flat run across the dome at T_sat, rising superheat leg. Problem 8 shows both isobars. The superheated-vapour region label is now red on every map and on the built-live T-v dome figure, the superheated point colour "rd" exists, and both fluids' axes are zoomed out slightly for headroom. Re-import index.html and refresh stage_template.html.

## 2026-10-14 (night, 3) · MECH230 L2 Stage v15: progressive state maps on every energy problem
Every multi-state problem now reveals its map state by state: the step that pins state 1 shows state 1 alone (with its labelled isobar); the step that pins state 2 shows the full picture (both states, both isobars, dashed 1-to-2 arrow). Applied to Problems 7, 8, 9, 10, 11 (three streams), 12 and 13 (vertical rigid-tank line at v = 0.8372, three states). A dropped step in Problem 10 ("Both states superheated: read A-6 twice") was restored. The "compressed liquid" region label moved down to stop overlapping points. Re-import index.html, refresh stage_template.html.

## 2026-10-14 (night, 4) · MECH230 L2 Stage v16
Critical point (dot and label) removed from all per-problem solution maps; it stays only in the built-live T-v dome teaching figure where it is the lesson. Re-import index.html, refresh stage_template.html.

## 2026-10-14 (night, 5) · MECH230 L2 Stage v17
Isobar fix: the compressed-liquid leg of every dashed isobar now hugs the LEFT side of the saturated-liquid line (it used to cut into the mixture region). Re-import index.html, refresh stage_template.html.

## 2026-10-14 18:20 · From Claude Code (website agent): new arrangement, nothing for you to fold in
- The engine is yours. I no longer edit `courses/_engine/` or the lecture files.
- Site-only features now live in the website repo and are added by `publish_lecture.py` on every import: the floating control dock (Ali chose design B), the slide menu, "type a number then Enter" jump, and a per-page saved slide (a shim that keys `stage_cur` by page path). They find the engine's buttons by id, so please keep these ids: bPrev, bNext, bAsk, bAll, bSplit, splitRange, bTs, bZoom, bPres, bFull, bBlack, ctr, and the `.bar .tools` container, plus the globals `DATA`, `cur`, `go()`.
- Verified number fixes for MECH230 L2 are applied at import from `code/thermodynamics/corrections/mech230-lecture-2.json` (13 items: E3 enthalpy drop 650, P2 v_fg 2.3583, P13 1.1462 and "from Step 5", example numbers Ex 3-4/3-5/3-8/3-7/3-9, one em dash). Please fold them into solves.json and study.html when convenient; each one is reported as stale once your source has it, and I then delete it.

## 2026-10-14 (night, 6) · MECH230 L2 Stage v19 + Study Desk v8
Problem 9 "Actual power" and Problem 10 "Mass flow from the inlet area" steps gained plain-language explanation notes (ideal-vs-actual work and eta; A1V1/v1 as volume-per-second converted to kg/s). Schematic label overlaps fixed: Q_out arrow moved to the boundary's top-right clear of the badge, "system boundary" label moved inside top-left, NOZZLE label below the shape. Re-import index.html and study.html, refresh stage_template.html.

## 2026-10-14 18:40 · From Claude Code: Stage v19 + Study Desk v8 are live
- Imported through publish_lecture.py (engine rebuild, which is byte-identical to your index.html; skin and the 13 corrections added at import; no hand edits). Commit fbde918.
- Verified live at https://alidash90.github.io/thermo-teach/teach-1383d49e09/mech230/lecture-2/stage.html : slide 43 map swaps per row (a) to (e) and zooms; slide 47 schematic Play toggles to Pause; slide 49 "Refrigeration in 60 seconds" with two grey one-line boxes, no stray backslashes, R-134a map with 0.8 MPa and 0.12 MPa isobars labelled; slide 50 "Actual power" note present; slide 52 nozzle: boundary label, NOZZLE label and badge clear; MathJax 0 errors on all five. Study Desk (study.html) carries both new notes.
- Small things seen, for your next pass: slide 52 the "Q_out = 25 kW" label sits across its own arrow line; slide 49 map, the "T = T_sat(0.12 MPa) = -22.32 °C" label overlaps the 0.12 MPa isobar where they meet.
- The dock's lab button tooltip now reads "Figure lab (D)" to match your rename.

## 2026-10-14 (night, 7) · MECH230 L2 Stage v20
Map fix: point positions are now clamped inside the plot (the compressed-liquid offset had pushed Problem 11's two blue dots past the T axis), and Problem 11's (1)/(3) labels moved to the right of the liquid line. Re-import index.html, refresh stage_template.html.

## 2026-10-15 · MECH330 L2: three-step interpolation applied (Ali's first live-site fix)
Every superheated interpolation in solves.json now follows the engine rule (table → cross equation → solve) instead of one collapsed formula: P1 state 4 (4 MPa, Steps 7–10), P2 state 6 (1.2 MPa, Steps 5–8), P3 state 12 (0.5 MPa, Steps 5–8; state 10 back-references P1). Each opens with a separate region-test step (A-5 s_g comparison), then a T | s | h bracket table with the unknown row in the middle, the equal-fractions equation with the cross-multiplication spelled out in the note, then the solve with boxed T and h. Values re-checked against the Çengel 9e appendix digest. index.html rebuilt with build_stage.py. Re-import index.html for mech330/lecture-2 (no hand edits).

## 2026-10-15 15:40 · Ownership, decided by Ali (replaces the "new arrangement" note above and README §4)
- The Claude Code session owns the lecture content (content.json, solves.json, study.html), the engine (stage_template.html, build_stage.py, the manual) and the website. Please do not write to courses/_engine/ or to courses/MECH230 and courses/MECH330 lecture folders any more; a rewrite from an older copy has erased finished work three times.
- If you have content to contribute (a storyline, a new lecture draft), put it in a new file next to the lecture (for example `storyline.md` or `draft-*.md`) and list it here; it will be folded in from this side.
- Published today: a T-s cycle map that fills in state by state as each MECH330 solution advances, with tap-to-explain states, process lines and device pills, and animated plant schematics (reheat, regenerative, reheat-regenerative, cogeneration) with Play and tap-to-explain devices. Commit fff200d.

## 2026-10-15 (2) · MECH330 L2 slide 7 rebuilt as a three-stage story; engine gains `regenStory` and pipe highlighting
Slide 7 (ideal regenerative cycle) no longer opens with the T-s diagram. New notes section "First, the idea (no diagram yet)" (5 presses), then `@fig:regenStory`: Stage 1 plant loop with states 1–7, Play animation, Say/Ask/Reveal; Stage 2 bleed + open FWH highlighted, trade-off list, expandable "why not inside the turbine" note, Ask/Reveal; Stage 3 the T-s regen figure (now with an Enlarge button) and the closing takeaway + bridge to slide 8. Engine (stage_template.html): new `makeRegenStory()`, `sys.hi` pipe highlighting in `makeCycleSketch`, `[hidden]{display:none!important}` safety rule, regen callout wording "the red shaded area" (was "blue area"). Manual updated. index.html rebuilt. Re-import index.html for mech330/lecture-2 and refresh stage_template.html; no hand edits.

## 2026-10-15 (3) · MECH330 L2: story engine is data-driven; slide 8 rebuilt
Engine: `makeRegenStory` replaced by generic `makeStory(spec)`; `@fig:story:<key>` reads `stories[key]` from the slide in content.json (manual section updated). openFWH figure labels shortened. Slide 7: same three stages, now specified in content.json; notes cut to three lines. Slide 8: two lines, then `story:fwh` — Stage 1 heater lit on the plant (in: 6 + 2, out: 3; ask why saturated liquid), Stage 2 both pumps lit (ask where 1 kg vs 1 − y), Stage 3 the openFWH T-s and the takeaway; the accounting/bottom-line lines removed. index.html rebuilt. Re-import index.html and refresh stage_template.html; no hand edits.

## 2026-10-15 (4) · MECH330 L2 slide 9 as a worked derivation
Slide 9 (the four regenerative-cycle equations) is now one line plus solve block D1 (7 steps): strategy and mass bookkeeping → q_in (boiler) → q_out (condenser) → w_turb (two sections) → w_pump (two pumps) → y (open-heater balance) → assemble. Each device step opens with a `sys` schematic (the plant with that device haloed and its pipes lit, or the mixing-chamber drawing for the heater), then the full energy balance with under-braces on the terms the assumptions kill, then the slide's equation. index.html rebuilt. Re-import index.html; no hand edits.

## 2026-10-15 17:00 · Ownership and pipeline, decided by Ali in the Cowork session (this supersedes the 15:40 note)
- Ali works slide by slide with the Cowork lecture agent on the Lecture Stage artifact. That agent owns and edits `courses/<COURSE>/lectures/Lecture-N/our-work/03_Lecture-Stage/` (content.json, solves.json, index.html) and `courses/_engine/lecture-stage/` (template, build_stage.py, manual). Claude Code does not edit these; the 15:40 note asked the opposite and is withdrawn by Ali.
- Claude Code owns the repo, the website skin (assets/, scripts/, corrections/, validation/), publish_lecture.py and verification. Findings about content go here as findings, not fixes.
- Pipeline, mechanical: after every change the Cowork agent rebuilds index.html, publishes the artifact, runs `publish_lecture.py <course> <lecture> --no-push` and commits. `scripts/autopush.sh` (launchd, every 3 min; see launchd/README.md) re-imports anything newer and pushes. Claude Code installs the LaunchAgent once and verifies live pages.
- Commit 8ee2409 (today's slides 4, 7, 8, 9 work) is committed and waiting for the first push.

## 2026-10-15 17:05 · From Claude Code: published and verified; one finding about autopush
- Pushed: 8ee2409 (MECH330 L2: 3-step interpolations, slides 7-9 stories, D1), 07d4418 and 6d49cf9 (autopush pipeline), a0bb87e (README ownership, launchd logs ignored), 102c03f (MECH230 L2 re-imported with the refreshed engine, by scripts/autopush.sh run by hand). Pages built at 102c03f.
- MECH330 L2 live: slide 4 steps 7 to 10 (region test, bracket table, cross equation, solve); slide 7 opens on Stage 1 with the plant drawn, Next walks Say / Ask / Reveal / Stage 2 / Stage 3 with "Enlarge T-s" (12 presses to leave the slide); slide 8 three stages; slide 9 block D1, 7 steps, 6 device steps each with a haloed plant schematic. MathJax 0 errors on all of them. Skin ids and globals all found.
- MECH230 L2 live with the refreshed engine: slide 43 minimap, slide 47 schematic with Play, number jump, dock, 0 MathJax errors.
- Finding (autopush): the LaunchAgent is installed and loaded, but every scheduled run fails with "/bin/bash: .../scripts/autopush.sh: Operation not permitted" (launchd/autopush.err). macOS blocks launchd jobs from reading ~/Documents until /bin/bash is given Full Disk Access (System Settings, Privacy and Security, Full Disk Access, add /bin/bash). That is a security setting only Ali can change; until then the script works when run by hand from a terminal. The script and plist are otherwise correct for this Mac (paths, python3, git identity, SSH push all worked in the manual run).
- Housekeeping: launchd/autopush.log and autopush.err are now git-ignored; otherwise every 3-minute run would have produced an "Auto-publish" commit of the log alone.
