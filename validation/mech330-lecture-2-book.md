# Book check: MECH330 Lecture 2

Against the Cengel 9e knowledge base (`courses/MECH330/resources/cengel/`, manifest + tables/A-*.csv). Made by `scripts/check_book.py`.

- Table values: 45 matched to the printed digits, 1 not matched.
- Citations: 14 resolved in the manifest, 1 found only in the book text (index gap), 0 missing.
- Example fit: 2 of 4 solve blocks find most of their results in the cited example.

## Table values not matched

| Where | Value | Finding |
|---|---|---|
| P1 step 7 note | 6.6796 | A-6 nearest: s_kJ_per_kgK = 7.3706 at P_MPa=4.0, T_C=600 |

## Citations

| Kind | Id | Book | Status | Used in |
|---|---|---|---|---|
| equation | 8-5 | in the book text p. 418; not indexed in manifest.json | ok-text | 1 place(s) |
| equation | 10-1 | (q_in − q_out) + (w_in − w_out) = h_e − h_i  (kJ/kg)** stead | ok | 1 place(s) |
| equation | 10-8 | eta_th = w_net/q_in = 1 − q_out/q_in**, where w_net = q_in − | ok | 1 place(s) |
| equation | 10-12 | q_in = q_primary + q_reheat = (h_3 − h_2) + (h_5 − h_4) | ok | 2 place(s) |
| equation | 10-13 | w_turb,out = w_turb,I + w_turb,II = (h_3 − h_4) + (h_5 − h_6 | ok | 1 place(s) |
| equation | 10-14 | q_in = h_5 − h_4 | ok | 1 place(s) |
| equation | 10-23 | epsilon_u = (Net power output + Process heat delivered)/Tota | ok | 1 place(s) |
| example | 10-3 | Effect of Boiler Pressure and Temperature on Efficiency (pp. 553-555) | ok | 4 place(s) |
| example | 10-4 | The Ideal Reheat Rankine Cycle (pp. 557-559) | ok | 1 place(s) |
| example | 10-5 | The Ideal Regenerative Rankine Cycle (pp. 562-564) | ok | 5 place(s) |
| example | 10-6 | The Ideal Reheat-Regenerative Rankine Cycle (pp. 565-567) | ok | 3 place(s) |
| example | 10-8 | An Ideal Cogeneration Plant (pp. 572-574) | ok | 4 place(s) |
| section | 10-5 | THE IDEAL REHEAT RANKINE CYCLE (pp. 555-556) | ok | 1 place(s) |
| section | 10-6 | THE IDEAL REGENERATIVE RANKINE CYCLE (pp. 559-562) | ok | 1 place(s) |
| section | 10-8 | COGENERATION (pp. 569-572) | ok | 1 place(s) |

## Example fit (results found in the cited example text)

| Block | Cites | Book title | Pages | Found |
|---|---|---|---|---|
| P1 | Ex 10-4 | The Ideal Reheat Rankine Cycle | 557-559 | 1 of 31 (check the citation) |
| P2 | Ex 10-5 | The Ideal Regenerative Rankine Cycle | 562-564 | 23 of 38 |
| P3 | Ex 10-6 | The Ideal Reheat-Regenerative Rankine Cycle | 565-567 | 14 of 43 (check the citation) |
| P4 | Ex 10-8 | An Ideal Cogeneration Plant | 572-574 | 18 of 26 |

## Table values matched

| Where | Value | Book cell |
|---|---|---|
| P1 step 5 tbl | 0.6492 | A-5 sf_kJ_per_kgK = 0.6492 |
| P1 step 5 tbl | 7.4996 | A-5 sfg_kJ_per_kgK = 7.4996 |
| P1 step 5 tbl | 191.81 | A-5 hf_kJ_per_kg = 191.81 |
| P1 step 5 tbl | 2392.1 | A-5 hfg_kJ_per_kg = 2392.1 |
| P1 step 6 tbl | 7.4357 | A-6 s_kJ_per_kgK = 7.4357 |
| P1 step 6 tbl | 7.3706 | A-6 s_kJ_per_kgK = 7.3706 |
| P1 step 6 tbl | 7.3127 | A-6 s_kJ_per_kgK = 7.3127 |
| P1 step 7 tbl | 2.7966 | A-5 sf_kJ_per_kgK = 2.7966 |
| P1 step 7 tbl | 6.0696 | A-5 sg_kJ_per_kgK = 6.0696 |
| P1 step 8 tbl | 6.5843 | A-6 s_kJ_per_kgK = 6.5843 |
| P1 step 8 tbl | 3093.3 | A-6 h_kJ_per_kg = 3093.3 |
| P1 step 8 tbl | 6.7714 | A-6 s_kJ_per_kgK = 6.7714 |
| P1 step 8 tbl | 3214.5 | A-6 h_kJ_per_kg = 3214.5 |
| P2 step 5 tbl | 6.5217 | A-5 sg_kJ_per_kgK = 6.5217 |
| P2 step 6 tbl | 6.5909 | A-6 s_kJ_per_kgK = 6.5909 |
| P2 step 6 tbl | 2816.1 | A-6 h_kJ_per_kg = 2816.1 |
| P2 step 6 tbl | 6.8313 | A-6 s_kJ_per_kgK = 6.8313 |
| P2 step 6 tbl | 2935.6 | A-6 h_kJ_per_kg = 2935.6 |
| P2 step 9 tbl | 0.6492 | A-5 sf_kJ_per_kgK = 0.6492 |
| P2 step 9 tbl | 8.1488 | A-5 sg_kJ_per_kgK = 8.1488 |
| P3 step 2 tbl | 191.81 | A-5 hf_kJ_per_kg = 191.81 |
| P3 step 2 tbl | 0.00101 | A-5 vf_m3_per_kg = 0.001010 |
| P3 step 2 tbl | 640.09 | A-5 hf_kJ_per_kg = 640.09 |
| P3 step 2 tbl | 0.001093 | A-5 vf_m3_per_kg = 0.001093 |
| P3 step 3 tbl | 1087.4 | A-5 hf_kJ_per_kg = 1087.4 |
| P3 step 3 tbl | 0.001252 | A-5 vf_m3_per_kg = 0.001252 |
| P3 step 3 tbl | 2.7966 | A-5 sf_kJ_per_kgK = 2.7966 |
| P3 step 4 tbl | 3583.1 | A-6 h_kJ_per_kg = 3583.1 |
| P3 step 4 tbl | 6.6796 | A-6 s_kJ_per_kgK = 6.6796 |
| P3 step 4 tbl | 3674.9 | A-6 h_kJ_per_kg = 3674.9 |
| P3 step 4 tbl | 7.3706 | A-6 s_kJ_per_kgK = 7.3706 |
| P3 step 5 tbl | 6.8207 | A-5 sg_kJ_per_kgK = 6.8207 |
| P3 step 6 tbl | 7.2725 | A-6 s_kJ_per_kgK = 7.2725 |
| P3 step 6 tbl | 2961.0 | A-6 h_kJ_per_kg = 2961.0 |
| P3 step 6 tbl | 7.4614 | A-6 s_kJ_per_kgK = 7.4614 |
| P3 step 6 tbl | 3064.6 | A-6 h_kJ_per_kg = 3064.6 |
| P4 step 2 tbl | 6.8207 | A-5 sg_kJ_per_kgK = 6.8207 |
| P4 step 2 tbl | 1.8604 | A-5 sf_kJ_per_kgK = 1.8604 |
| P4 step 2 tbl | 4.9603 | A-5 sfg_kJ_per_kgK = 4.9603 |
| P4 step 2 tbl | 640.09 | A-5 hf_kJ_per_kg = 640.09 |
| P4 step 2 tbl | 2108.0 | A-5 hfg_kJ_per_kg = 2108.0 |
| P4 step 2 tbl | 0.4762 | A-5 sf_kJ_per_kgK = 0.4762 |
| P4 step 2 tbl | 7.9176 | A-5 sfg_kJ_per_kgK = 7.9176 |
| P4 step 2 tbl | 137.75 | A-5 uf_kJ_per_kg = 137.75 |
| P4 step 2 tbl | 2423.0 | A-5 hfg_kJ_per_kg = 2423.0 |
