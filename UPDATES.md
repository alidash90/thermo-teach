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
