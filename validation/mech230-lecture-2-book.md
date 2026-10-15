# Book check: MECH230 Lecture 2

Against the Cengel 9e knowledge base (`courses/MECH330/resources/cengel/`, manifest + tables/A-*.csv). Made by `scripts/check_book.py`.

- Table values: 53 matched to the printed digits, 0 not matched.
- Citations: 26 resolved in the manifest, 2 found only in the book text (index gap), 0 missing.
- Example fit: 6 of 6 solve blocks find most of their results in the cited example.

## Table values not matched

None.

## Citations

| Kind | Id | Book | Status | Used in |
|---|---|---|---|---|
| equation | 2-32 | delta E_system = E_final - E_initial = E_2 - E_1. Energy is  | ok | 1 place(s) |
| equation | 2-33 | in the book text p. 72; not indexed in manifest.json | ok-text | 1 place(s) |
| equation | 2-41 | Efficiency = Desired output / Required input. Efficiency is  | ok | 1 place(s) |
| equation | 2-43 | eta_overall = eta_comb.equip. eta_thermal eta_generator = W_ | ok | 1 place(s) |
| equation | 3-1 | in the book text p. 122; not indexed in manifest.json | ok-text | 1 place(s) |
| equation | 3-3 | quality x = m_vapor / m_total, with m_total = m_liquid + m_v | ok | 1 place(s) |
| equation | 3-4 | v_avg = v_f + x v_fg (m^3/kg). **Eq. 3-5** x = (v_avg - v_f) | ok | 1 place(s) |
| equation | 3-8 | y ~ y_f @ T (y = v, u, h) (approximation; h is the most sens | ok | 1 place(s) |
| example | 2-10 | Cooling of a Hot Fluid in a Tank (pp. 74-75) | ok | 1 place(s) |
| example | 2-11 | Acceleration of Air by a Fan (pp. 75-76) | ok | 1 place(s) |
| example | 2-16 | Cost Savings Associated with High-Efficiency Motors (pp. 84-85) | ok | 1 place(s) |
| example | 3-1 | Pressure of Saturated Liquid in a Tank (pp. 123) | ok | 2 place(s) |
| example | 3-4 | Pressure and Volume of a Saturated Mixture (pp. 126-127) | ok | 2 place(s) |
| example | 3-5 | Properties of Saturated Liquid–Vapor Mixture (pp. 127-128) | ok | 3 place(s) |
| example | 3-7 | Temperature of Superheated Vapor (pp. 129) | ok | 2 place(s) |
| example | 3-8 | Approximating Compressed Liquid as Saturated Liquid (pp. 130) | ok | 2 place(s) |
| example | 3-9 | The Use of Steam Tables to Determine Properties (pp. 131-132) | ok | 5 place(s) |
| section | 2-6 | The First Law of Thermodynamics (pp. 70-77) | ok | 5 place(s) |
| section | 2-7 | Energy Conversion Efficiencies (pp. 78-85) | ok | 7 place(s) |
| section | 3-1 | Pure Substance (pp. 110) | ok | 2 place(s) |
| section | 3-2 | Phases of a Pure Substance (pp. 110-111) | ok | 2 place(s) |
| section | 3-3 | Phase-Change Processes of Pure Substances (pp. 111-116) | ok | 9 place(s) |
| section | 3-4 | Property Diagrams for Phase-Change Processes (pp. 116-122) | ok | 4 place(s) |
| section | 3-5 | Property Tables (pp. 122-132) | ok | 14 place(s) |
| section | 5-1 | Conservation of Mass (pp. 212-217) | ok | 1 place(s) |
| section | 5-2 | Flow Work and the Energy of a Flowing Fluid (pp. 219-221) | ok | 1 place(s) |
| section | 5-3 | Energy Analysis of Steady-Flow Systems (pp. 222-225) | ok | 2 place(s) |
| section | 5-4 | Some Steady-Flow Engineering Devices (pp. 225-238) | ok | 10 place(s) |

## Example fit (results found in the cited example text)

| Block | Cites | Book title | Pages | Found |
|---|---|---|---|---|
| P1 | Ex 3-1 | Pressure of Saturated Liquid in a Tank | 123 | 3 of 3 |
| P2 | Ex 3-4 | Pressure and Volume of a Saturated Mixture | 126-127 | 3 of 6 |
| P3 | Ex 3-5 | Properties of Saturated Liquid–Vapor Mixture | 127-128 | 10 of 13 |
| P4 | Ex 3-8 | Approximating Compressed Liquid as Saturated Liquid | 130 | 1 of 1 |
| P5 | Ex 3-7 | Temperature of Superheated Vapor | 129 | 3 of 6 |
| P6 | Ex 3-9 | The Use of Steam Tables to Determine Properties | 131-132 | 11 of 15 |

## Table values matched

| Where | Value | Book cell |
|---|---|---|
| P1 step 3 tbl | 0.001036 | A-4 vf_m3_per_kg = 0.001036 |
| P1 step 3 tbl | 2.3593 | A-4 vg_m3_per_kg = 2.3593 |
| P2 step 3 tbl | 0.001036 | A-4 vf_m3_per_kg = 0.001036 |
| P2 step 3 tbl | 2.3593 | A-4 vg_m3_per_kg = 2.3593 |
| P2 step 3 tbl | 2.3583 | A-4 vg_m3_per_kg - vf_m3_per_kg = 2.3593 - 0.001036 = 2.358264 |
| P2 step 3 tbl | 2.3583 | A-4 vg_m3_per_kg - vf_m3_per_kg = 2.3593 - 0.001036 = 2.358264 |
| P3 step 2 tbl | 0.0007435 | A-12 vf_m3_per_kg = 0.0007435 |
| P3 step 2 tbl | 0.12355 | A-12 vg_m3_per_kg = 0.12355 |
| P3 step 4 tbl | 31.18 | A-12 hf_kJ_per_kg = 31.18 |
| P3 step 4 tbl | 209.96 | A-12 hfg_kJ_per_kg = 209.96 |
| P4 step 3 tbl | 334.97 | A-4 uf_kJ_per_kg = 334.97 |
| P5 step 1 tbl | 2748.1 | A-5 hg_kJ_per_kg = 2748.1 |
| P5 step 2 tbl | 2855.8 | A-6 h_kJ_per_kg = 2855.8 |
| P5 step 2 tbl | 2961.0 | A-6 h_kJ_per_kg = 2961.0 |
| P6 step 1 tbl | 504.50 | A-5 uf_kJ_per_kg = 504.50 |
| P6 step 1 tbl | 2024.6 | A-5 ufg_kJ_per_kg = 2024.6 |
| P6 step 2 tbl | 524.83 | A-4 uf_kJ_per_kg = 524.83 |
| P6 step 2 tbl | 2534.3 | A-4 ug_kJ_per_kg = 2534.3 |
| P6 step 2 tbl | 2009.5 | A-4 ufg_kJ_per_kg = 2009.5 |
| P6 step 3 tbl | 2875.7 | A-6 u_kJ_per_kg = 2875.7 |
| P6 step 3 tbl | 2957.9 | A-6 u_kJ_per_kg = 2957.9 |
| P6 step 6 tbl | 313.99 | A-4 uf_kJ_per_kg = 313.99 |
| P6 step 7 tbl | 731.00 | A-5 uf_kJ_per_kg = 731.00 |
| P7 step 3 tbl | 3248.4 | A-6 h_kJ_per_kg = 3248.4 |
| P7 step 4 tbl | 225.94 | A-5 hf_kJ_per_kg = 225.94 |
| P7 step 4 tbl | 2372.3 | A-5 hfg_kJ_per_kg = 2372.3 |
| P8 step 3 tbl | 95.48 | A-12 hf_kJ_per_kg = 95.48 |
| P8 step 4 tbl | 22.47 | A-12 hf_kJ_per_kg = 22.47 |
| P8 step 4 tbl | 236.99 | A-12 hg_kJ_per_kg = 236.99 |
| P9 step 3 tbl | 2903.3 | A-6 h_kJ_per_kg = 2903.3 |
| P9 step 4 tbl | 417.51 | A-5 hf_kJ_per_kg = 417.51 |
| P9 step 4 tbl | 2675.0 | A-5 hg_kJ_per_kg = 2675.0 |
| P10 step 3 tbl | 3267.7 | A-6 h_kJ_per_kg = 3267.7 |
| P10 step 3 tbl | 0.38429 | A-6 v_m3_per_kg = 0.38429 |
| P10 step 3 tbl | 3072.1 | A-6 h_kJ_per_kg = 3072.1 |
| P10 step 3 tbl | 1.31623 | A-6 v_m3_per_kg = 1.31623 |
| P11 step 3 tbl | 83.915 | A-4 hf_kJ_per_kg = 83.915 |
| P11 step 3 tbl | 251.18 | A-4 hf_kJ_per_kg = 251.18 |
| P11 step 3 tbl | 2769.1 | A-6 h_kJ_per_kg = 2769.1 |
| P12 step 2 tbl | 762.51 | A-5 hf_kJ_per_kg = 762.51 |
| P12 step 2 tbl | 2014.6 | A-5 hfg_kJ_per_kg = 2014.6 |
| P12 step 3 tbl | 191.81 | A-5 hf_kJ_per_kg = 191.81 |
| P12 step 3 tbl | 2583.9 | A-5 hg_kJ_per_kg = 2583.9 |
| P12 step 4 tbl | 2592.0 | A-6 h_kJ_per_kg = 2592.0 |
| P12 step 4 tbl | 2687.5 | A-6 h_kJ_per_kg = 2687.5 |
| P13 step 6 tbl | 0.001043 | A-5 vf_m3_per_kg = 0.001043 |
| P13 step 6 tbl | 1.6734 | A-5 vg_m3_per_kg = 1.6734 |
| P13 step 6 tbl | 1.6724 | A-5 vg_m3_per_kg - vf_m3_per_kg = 1.6734 - 0.001043 = 1.672357 |
| P13 step 6 tbl | 1.6724 | A-5 vg_m3_per_kg - vf_m3_per_kg = 1.6734 - 0.001043 = 1.672357 |
| P13 step 7 tbl | 0.001053 | A-5 vf_m3_per_kg at P_kPa=151.95: 0.00105331 |
| P13 step 7 tbl | 1.1473 | A-5 vg_m3_per_kg at P_kPa=151.95: 1.14726 |
| P13 step 8 tbl | 0.88578 | A-5 vg_m3_per_kg = 0.88578 |
| P13 step 8 tbl | 0.79329 | A-5 vg_m3_per_kg = 0.79329 |
