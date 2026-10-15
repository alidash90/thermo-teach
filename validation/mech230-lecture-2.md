# Number trace: courses/MECH230/lectures/Lecture-2/our-work/03_Lecture-Stage (with corrections/)

- Corpus: 92 files from the Çengel 9e digest and the 10e Connect markdown.
- Numbers checked (3+ significant digits): 421; traced to the corpus: 347; untraced: 74.
- Untraced is not an error by itself: computed results rarely appear verbatim. Review the table lookups first.

## Table lookups (check first): 4

| Where | Field | Value | Context |
|---|---|---|---|
| P2 step 3 | tbl | 2.3583 | `001036, v_g = 2.3593 m³/kg, so v_fg = v_g − v_f = 2.3583` |
| P13 step 6 | tbl | 1.6724 | `Pa: v_f = 0.001043, v_g = 1.6734 m³/kg, so v_fg = 1.6724` |
| P13 step 7 | tbl | 151.95 | `A-5 interpolated at 151.95 kPa: v_f ≈ 0.001053, v_g ≈ 1.` |
| P13 step 7 | tbl | 1.1473 | `interpolated at 151.95 kPa: v_f ≈ 0.001053, v_g ≈ 1.1473 m³/kg` |

## Solve steps (mostly computed results): 55

| Where | Field | Value | Context |
|---|---|---|---|
| E3 step 5 | num | 587.1 | `\Delta h=\frac{-81.6}{0.139}-63.0+0.049=-587.1-63.0+0.05` |
| P2 step 3 | num | 2.3583 | `v=0.001036+(0.2)(2.3583)=0.4727\ \text{m}^3/\text{kg}` |
| P2 step 3 | num | 0.4727 | `v=0.001036+(0.2)(2.3583)=0.4727\ \text{m}^3/\text{kg},\qquad ` |
| P2 step 3 | num | 0.4727 | `v=0.001036+(0.2)(2.3583)=0.4727\ \text{m}^3/\text{kg},\qquad ` |
| P2 step 4 | num | 4.72 | `V=0.008+4.72=4.73\ \text{m}^3\;\checkmark` |
| P2 step 4 | note | 99.8 | `Two kg of vapour fill 99.8 % of the tank. That is why x ` |
| P3 step 2 | num | 0.1236 | `0.0007<0.02<0.1236\;\checkmark` |
| P3 step 3 | num | 0.12281 | `0.02-0.0007435}{0.12355-0.0007435}=\frac{0.01926}{0.12281}` |
| P5 step 3 | num | 34.2 | `\frac{T-200}{250-200}=\frac{T-200}{50}=\frac{34.2}{105.2}=0.325` |
| P6 step 1 | res | 1719.3 | `u=1719.3\ \text{kJ/kg}\quad\text{(satu` |
| P6 step 4 | num | 74.3 | `\frac{T-350}{400-350}=\frac{T-350}{50}=\frac{74.3}{82.2}=0.904` |
| P6 step 4 | num | 0.904 | `-350}{400-350}=\frac{T-350}{50}=\frac{74.3}{82.2}=0.904` |
| P7 step 4 | res | 2361.0 | `h_2=2361.0\ \text{kJ/kg}` |
| P7 step 5 | num | 887.4 | `887.4;\qquad \frac{50^2-180^2}{2000` |
| P7 step 5 | res | 887.4 | `w_{\rm out}=887.4-14.95+0.04=872.5\ \text{kJ/kg` |
| P8 step 5 | num | 73.01 | `x_2=\frac{95.48-22.47}{236.99-22.47}=\frac{73.01}{214.52}=0.340,\qquad \Delta ` |
| P9 step 4 | res | 2336.4 | `h_2=2336.4\ \text{kJ/kg}` |
| P9 step 5 | res | 566.9 | `w_{\rm out}=566.9\ \text{kJ/kg}` |
| P9 step 5 | eq | 2336.4 | `w_{\rm out}=h_1-h_2=2903.3-2336.4` |
| P9 step 6 | num | 566.9 | `\dot W_{\rm actual}=(0.80)(10)(566.9)=4535\ \text{kW}` |
| P9 step 6 | num | 4535 | `\dot W_{\rm actual}=(0.80)(10)(566.9)=4535\ \text{kW}` |
| P10 step 4 | res | 2.082 | `\dot m=2.082\ \text{kg/s}` |
| P10 step 5 | eq | 2.082 | `rm out}=\frac{\dot Q_{\rm out}}{\dot m}=\frac{25}{2.082}` |
| P10 step 7 | eq | 2.082 | `\dot{\mathcal V}_2=\dot m\,v_2=(2.082)(1.31623)` |
| P11 step 4 | num | 209.8 | `209.8+2769.1\,\dot m_2=627.95+251.1` |
| P11 step 4 | num | 627.95 | `209.8+2769.1\,\dot m_2=627.95+251.18\,\dot m_2+20;\qquad 25` |
| P11 step 4 | num | 2517.9 | `769.1\,\dot m_2=627.95+251.18\,\dot m_2+20;\qquad 2517.9\,\dot m_2=438.2` |
| P11 step 4 | num | 438.2 | `27.95+251.18\,\dot m_2+20;\qquad 2517.9\,\dot m_2=438.2` |
| P12 step 2 | res | 2676.4 | `h_2=2676.4\ \text{kJ/kg}` |
| P12 step 3 | num | 2676.4 | `2676.4>2583.9\;\checkmark` |
| P12 step 3 | eq | 2676.4 | `h_2=2676.4>h_{g@10\,kPa}\;\Rightarrow\;\` |
| P12 step 4 | eq | 2676.4 | `(\mathrm{kJ/kg}) \\ \hline 50 & 2592.0 \\ T_2=? & 2676.4 \\ 100 & 2687.5 \end{array}` |
| P12 step 5 | num | 84.4 | `\frac{T_2-50}{100-50}=\frac{T_2-50}{50}=\frac{84.4}{95.5}=0.884` |
| P12 step 5 | num | 0.884 | `2-50}{100-50}=\frac{T_2-50}{50}=\frac{84.4}{95.5}=0.884` |
| P12 step 5 | eq | 2676.4 | `\frac{T_2-50}{100-50}=\frac{2676.4-2592.0}{2687.5-2592.0}` |
| P13 step 3 | eq | 151.95 | `}\ (^{\circ}\mathrm{C}) \\ \hline 150 & 111.35 \\ 151.95 & T_2=? \\ 175 & 116.04 \end{` |
| P13 step 3 | t | 151.95 | `(a) T₂ at 151.95 kPa: set up the interpolation` |
| P13 step 4 | num | 4.69 | `frac{T_2-111.35}{116.04-111.35}=\frac{T_2-111.35}{4.69}=\frac{1.95}{25}=0.078` |
| P13 step 4 | eq | 151.95 | `\frac{T_2-111.35}{116.04-111.35}=\frac{151.95-150}{175-150}` |
| P13 step 4 | t | 151.95 | `(a) T₂ at 151.95 kPa: the cross equation (equa` |
| P13 step 5 | eq | 4.69 | `T_2=111.35+4.69\times0.078=111.35+0.37` |
| P13 step 5 | t | 151.95 | `(a) T₂ at 151.95 kPa: solve` |
| P13 step 6 | num | 1.6724 | `v_1=0.001043+(0.5)(1.6724)=0.8372;\qquad m=\frac{0.5}{0` |
| P13 step 6 | num | 0.8372 | `v_1=0.001043+(0.5)(1.6724)=0.8372;\qquad m=\frac{0.5}{0.8372}=0` |
| P13 step 6 | num | 0.8372 | `v_1=0.001043+(0.5)(1.6724)=0.8372;\qquad m=\frac{0.5}{0.8372}=0` |
| P13 step 7 | num | 0.8372 | `x_2=\frac{0.8372-0.001053}{1.1462}=0.729;\qqua` |
| P13 step 7 | num | 1.1462 | `x_2=\frac{0.8372-0.001053}{1.1462}=0.729;\qquad m_{g2}=(0.729)(` |
| P13 step 7 | num | 0.729 | `x_2=\frac{0.8372-0.001053}{1.1462}=0.729;\qquad m_{g2}=(0.729)(0.597)` |
| P13 step 7 | num | 0.729 | `x_2=\frac{0.8372-0.001053}{1.1462}=0.729;\qquad m_{g2}=(0.729)(0.597)` |
| P13 step 7 | note | 0.8372 | `v₂ = v₁ = 0.8372 from Step 5; v_f, v_g interpo` |
| P13 step 7 | note | 151.95 | `v₁ = 0.8372 from Step 5; v_f, v_g interpolated at 151.95 kPa.` |
| P13 step 8 | eq | 0.8372 | `3/\mathrm{kg}) \\ \hline 200 & 0.88578 \\ P_3=? & 0.8372 \\ 225 & 0.79329 \end{array}` |
| P13 step 9 | num | 0.04858 | `\frac{P_3-200}{225-200}=\frac{P_3-200}{25}=\frac{-0.04858}{-0.09249}=0.525` |
| P13 step 9 | num | 0.09249 | `200}{225-200}=\frac{P_3-200}{25}=\frac{-0.04858}{-0.09249}=0.525` |
| P13 step 9 | eq | 0.8372 | `\frac{P_3-200}{225-200}=\frac{0.8372-0.88578}{0.79329-0.88578}` |

## Notes and ask answers: 15

| Where | Field | Value | Context |
|---|---|---|---|
| slide 30 | line 3 | 70.18 | `essure is not a free choice, it must be P_sat = [[70.18 kPa]].` |
| slide 32 | ask 2 | 1.671 | `v_f ≈ 0.001, v_g = 1.672): x? / x = (1.0 − 0.001)/1.671 ≈ 0.60.` |
| slide 37 | line 7 | 99.8 | `Two kg of vapour fill [[99.8]] % of the tank: quality is a` |
| slide 39 | ask 1 | 0.1236 | `e? / v = 0.02 sits between v_f = 0.0007 and v_g = 0.1236 m³/kg.` |
| slide 44 | line 1 | 1719.3 | `AU's worked rows (a) and (b): same 120.21 °C, 1719.3 kJ/kg; 232.23 kPa, x = 0.535.` |
| slide 48 | line 1 | 2361.0 | `s solution of the turbine: same h₁ = 3248.4, h₂ = 2361.0, w = 872.5 kJ/kg, ṁ = 5.73 kg` |
| slide 50 | ask 3 | 566.9 | `Ideal power before the η? / 10 × 566.9 = 5669 kW ≈ 5.7 MW.` |
| slide 50 | ask 3 | 5669 | `Ideal power before the η? / 10 × 566.9 = 5669 kW ≈ 5.7 MW.` |
| slide 51 | line 1 | 2336.4 | `AU's solution: h₁ = 2903.3, h₂ = 2336.4, w = 566.9 kJ/kg, Ẇ ≈ 4.5 MW.` |
| slide 51 | line 1 | 566.9 | `AU's solution: h₁ = 2903.3, h₂ = 2336.4, w = 566.9 kJ/kg, Ẇ ≈ 4.5 MW. Press Next` |
| slide 51 | ask 1 | 4535 | `One sentence: why 4535 kW and not 5669 kW? / Only 80` |
| slide 51 | ask 1 | 5669 | `One sentence: why 4535 kW and not 5669 kW? / Only 80 % of the ideal ` |
| slide 52 | ask 3 | 2.082 | `Exit area if we wanted it? / A₂ = ṁv₂/V₂ = 2.082·1.316/606 ≈ 45 cm²: the nozzl` |
| slide 53 | line 1 | 2.082 | `AU's nozzle solution: same ṁ = 2.082 kg/s, V₂ = 606 m/s, 2.74 m³/s` |
| slide 56 | line 2 | 151.95 | `xture at 101.3 kPa, x = [[0.5]], heated until P = 151.95 kPa; find both temperatures, ` |
