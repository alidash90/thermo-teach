# thermodynamics: the Thermo teaching website (repo: thermo-teach)

GitHub Pages site for MECH230 Thermodynamics I and MECH330 Thermodynamics II, Australian University Kuwait.

- Live site: https://alidash90.github.io/thermo-teach/
- Instructor home (unlisted, bookmark it): https://alidash90.github.io/thermo-teach/teach-1383d49e09/
- Repo: https://github.com/alidash90/thermo-teach
- Method for lecture content: ../../courses/_engine/lecture-stage/Lecture-Stage_Build-Manual.md
- Original brief: ../../assistant/Thermo-Website_Claude-Code_Prompt.md

## 1. After each new lecture build (one command)
```
cd "~/Documents/Claude/Projects/AU Professorship agent/code/thermodynamics"
python3 scripts/publish_lecture.py mech230 lecture-3
```
- Options: `--title "..."`, `--pdf FILE:Label` (repeatable, kept on republish), `--rebuild` (force an engine rebuild), `--no-push`, `--dry-run`.
- Republishing the same lecture overwrites it in place; URLs never change.

## 2. Layout
```
index.html                         public landing page, two course cards (generated)
mech230/, mech330/                 public course pages: lecture titles only (generated)
teach-1383d49e09/                  unlisted instructor area, every page noindex
  index.html                       instructor home (generated)
  mech230/index.html               course page: Stage, Study Desk, PDFs per lecture (generated)
  mech230/lecture-N/               stage.html, study.html, img/p-NN.jpg, pdf/, lecture.json
assets/site.css                    shared style (AU navy #003C7B, orange #EE7421, dark mode)
site.json                          site title, unlisted folder name, course list, project_root
scripts/publish_lecture.py         copy one build in, check, index, commit, push
scripts/build_site.py              regenerate all index pages from the lecture folders present
scripts/validate_numbers.py        trace every number to the Çengel knowledge base
validation/                        per-lecture trace reports + DISCREPANCIES.md (confirmed findings)
```

## 3. What publish_lecture.py does
1. Reads `courses/<COURSE>/lectures/Lecture-N/our-work/03_Lecture-Stage/` (never writes there).
2. Stage: uses the built `index.html` when it is newer than content.json, solves.json and the engine template; otherwise rebuilds it in a temp folder with `courses/_engine/lecture-stage/build_stage.py`.
3. Study Desk: copies `study.html` if present; the course page shows "not built" otherwise.
4. Images: copies every `img/p-NN.jpg` the pages reference, from `img/`, else the `img/` inside a `*.zip` in the folder, else `Lecture-N/au-slide-images/`. Stops if one is missing.
5. Wraps the Stage fragment in a full UTF-8 document (claude.ai artifacts do this for the engine output) and adds `noindex` to every lecture page.
6. Warns on em dashes and on missing MathJax; writes `validation/<course>-lecture-N.md`.
7. Writes `lecture.json`, regenerates every index, commits and pushes.

## 4. Rules
- The repo is the publishing place, never the editing place. Fix content in `courses/`, engine changes in `courses/_engine/`, then republish.
- Privacy (decided 2026-10-14): public repo, public landing and course pages; Stage and Study Desk only under the unlisted folder. Anyone who browses the repo on github.com can still find them; for real protection use a private repo with GitHub Pro.
- Validate before publishing: read the trace report, recheck untraced table lookups, log confirmed findings in `validation/DISCREPANCIES.md`.

## 5. Ready for later (not built yet)
- Student view: a second engine output without answers, published to the public course pages (`lecture.json` can carry a `student` flag).
- Syllabus weeks to lectures: add a `weeks` map to `site.json` and render it on the public course page.
- Menti twin decks and printable packs: `--pdf FILE:Label` already attaches PDFs per lecture.
