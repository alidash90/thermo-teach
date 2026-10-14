# Discrepancy log

Numbers checked against the Çengel 9e knowledge base (`courses/MECH330/resources/cengel/digest/appendix.md`, chapter text) and the 10e solutions manual. The automated trace per lecture is in `<course>-lecture-N.md`; this file holds the confirmed findings after a manual recheck (every untraced number recomputed, every `tbl` row grepped).
Fixes are made in the source folder (`courses/<COURSE>/lectures/Lecture-N/our-work/03_Lecture-Stage/`), then the lecture is republished. Status: open until republished.

## MECH230 Lecture 2 (checked 2026-10-14)
- Result: 65 of 67 untraced numbers correct; all 31 `tbl` fields (about 95 values) match A-4, A-5, A-6, A-7, A-12; all final answers match the 9e examples (P1 to P8) or recompute (P9 to P13, AU problems).

| Where (solves.json) | On page | Correct | Reason | Severity | Status |
|---|---|---|---|---|---|
| E3 step 5, note and num | enthalpy drop 587 | 650 | 587 = 81.6/0.139 is Δh + Δke + Δpe; step 4 and slide 10 give Δh ≈ −650 | wrong | open |
| P2 step 3, num | 2.3582 | 2.3583, labelled v_fg | A-4 at 90 °C: v_g − v_f = 2.3593 − 0.001036 = 2.358264 (truncated, not rounded); result 0.4727 unaffected | rounding | open |
| P13 step 4, num | 1.1463 | 1.1462 | interpolated v_g − v_f at 151.95 kPa = 1.14620; x₂ = 0.729 unaffected | rounding | open |
| P13 step 3, num | 1.6724 next to "v_g = 1.6734" | value right, label it v_fg | A-5 at 101.325 kPa | label | open |
| P2 to P6 titles | Ex 3-2, 3-3, 3-4, 3-5, 3-6 | Ex 3-4, 3-5, 3-8, 3-7, 3-9 | 9e example numbers; content.json `book` fields are already right | label | open |
| P1 step 3, tbl (also in study.html) | em dash between "a room of steam" and "wrong column!" | comma or colon | house style: no em dashes | style | open |

## MECH330 Lecture 2 (checked 2026-10-14)
- Result: 68 of 74 untraced numbers correct; 55 of 56 `tbl` values match; final answers match (P1 with the 8e SI Ex 10-4, P2 Ex 10-5, P3 corrected Ex 10-6, P4 Ex 10-8).

| Where (solves.json) | On page | Correct | Reason | Severity | Status |
|---|---|---|---|---|---|
| P1 step 6, tbl (A-6, 3.5 MPa, 600 °C) | s = 7.4337 | 7.4357 | A-6 row 3.50 MPa, 600 °C: 0.11325, 3282.5, 3678.9, 7.4357 (digits transposed); the 4 MPa choice is unaffected | wrong | open |
| P3 step 5 to 7 (and the corrections.md line) | y = 0.1727, 1 − y = 0.8273 | 0.1726, 0.8274 | (1087.4 − 655.94)/(2067.6 + 431.46) = 0.172649 | rounding | open |
| P3 step 7, q_out | 0.6960(2143.9) = 1492.3 | show 0.6961, or print 1492.2 | the printed factor does not multiply out; η = 0.490 unaffected | inconsistent | open |
| P3 | h₄ = 655.94, η = 0.490 vs book 643.92, 0.492 | as on page | Ex 10-6 pump II quirk, already in `assistant/cengel-study/corrections.md` | known book quirk | logged |

## Engine
- 2026-10-14: `stage_template.html` presenter drawer placeholder changed from an em dash to "(none)"; saved slide position now keyed per page (`stage_cur:` + path) so lectures on one domain do not share it. Fixed.
