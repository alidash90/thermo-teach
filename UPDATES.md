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
Slide 49 (Problem 8) gained a "meet the refrigerant" mini-lesson before the solve, with new Ask-the-class questions. Re-import index.html from the same 03_Lecture-Stage folder.

## 2026-10-14 · From Claude Code (website agent): read before your next edit
Changes made directly in the project folders. Re-read these files before writing them again; earlier rewrites from an older copy undid them twice.
1. Engine `stage_template.html`: jump to any slide. The slide counter in the top bar is now a menu (number and title of every slide), and typing a slide number then Enter jumps there. The saved slide position is keyed per page (`stage_cur:` + path) so lectures on one website do not share it. The presenter-drawer placeholder is "(none)" instead of an em dash. Manual section 9 updated.
2. MECH230 L2 `solves.json` and `study.html`, number fixes checked against Çengel 9e: E3 step 5 enthalpy drop 650 (not 587); P2 step 3 v_fg = 2.3583; P13 v_g − v_f = 1.1462; P13 step 6 back-reference "from Step 5"; P2 to P6 titles cite Ex 3-4, 3-5, 3-8, 3-7, 3-9; em dash removed from P1 step 3.
3. MECH330 L2 `solves.json`, print pack `.tex` and PDF, `corrections.md`: P1 A-6 3.5 MPa/600 °C s = 7.4357; P3 y = 0.1726, 1 − y = 0.8274, q_in = 2923.5, q_out = 1492.4, η = 0.490 unchanged.
4. The website rebuilds index.html from content.json + solves.json with the engine on every publish, so edit those two files, not index.html.
Full log: `validation/DISCREPANCIES.md`.
Live checks passed 2026-10-14 17:40: slide 43 map and zoom, slide 47 schematic with Play, width slider saves, MathJax 0 errors, slide menu and number jump.
