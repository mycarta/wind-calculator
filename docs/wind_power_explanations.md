# Offshore Wind Calculator — Explanations and Formulas

> This document explains what the app computes, why some values are called “mean,” what EPF is, and how instantaneous vs. rated power differs. Equations are included for clarity.

---

## At a glance

- Inputs use average wind speeds at hub height. Outputs in the main column are mean values.
- We use an Energy Production Factor (EPF) to adjust the naive v³ scaling to something that better reflects real-world mean power at a site.
- “Mean power” is not the turbine’s nameplate/rated power. Rated power is a cap the machine holds above the rated wind speed.
- Annual energy is computed from mean power, with an optional derating (efficiency) to account for typical losses.

---

## Symbols

- $\rho$ — air density (kg/m³)
- $\bar{v}$ — average wind speed at hub height (m/s)
- $\mathrm{EPF}$ — Energy Production Factor (dimensionless)
- $D$ — rotor diameter (m)
- $A$ — rotor swept area (m²)
- $\overline{P}_A$ — mean power density (W/m²)
- $\overline{P}$ — mean power for a single turbine (W)
- $\eta$ — overall efficiency/derating (0–1)
- $N$ — number of installed turbines on site

---

## Rotor Area

$$
A = \frac{\pi D^2}{4}
$$

---

## Mean power density (EPF-adjusted)

Using average wind speed and EPF:

$$
\overline{P}_A = \tfrac{1}{2}\,\rho\,\mathrm{EPF}\,\bar{v}^{3}\quad [\text{W/m}^2]
$$

- Without EPF, the naive mean of $v^3$ is underestimated if you just use $\bar{v}^3$.
- EPF is an empirical factor that approximates the effect of the true wind-speed distribution.

---

## Mean power for a single turbine

$$
\overline{P} = \overline{P}_A\,A\quad [\text{W}]\quad\Rightarrow\quad \overline{P}_{\text{kW}} = \frac{\overline{P}}{1000}
$$

This is a mean value over time, not an instantaneous snapshot.

---

## Annual energy (non-derated and derated)

Non-derated annual energy:

$$
\mathrm{AEP}_{\text{nd}}\;[\text{MWh/yr}]\;=\;\overline{P}_{\text{kW}}\times 8760\times\frac{1}{1000}
$$

Derated (efficiency applied):

$$
\mathrm{AEP}_{\text{derated}}\;=\;\eta\;\times\;\mathrm{AEP}_{\text{nd}}
$$

- $\eta$ lumps typical losses (availability, electrical, wake, etc.).

---

## Site totals

All site totals multiply the single-turbine mean quantities by the number of turbines $N$ determined from available area and spacing:

- Center-to-center spacing (m): $\;S = D\times F$ where $F$ is the selected spacing factor.
- Turbine count $N$ is computed from site area and spacing layout (see app for the exact logic).

Then, e.g., total mean power (EPF-adjusted):

$$
\overline{P}_{\text{site}} = N\times \overline{P}_{\text{kW}}\quad [\text{kW}]
$$

Total annual energies follow analogously.

---

## Instantaneous vs. rated power (context)

The app’s main outputs are mean values. An instantaneous physics calculation would use a power coefficient and a specific wind speed at a moment in time:

$$
P_{\text{inst}} = \tfrac{1}{2}\,\rho\,A\,C_p\,v^3
$$

Real turbines are capped at their nameplate (rated) power above the rated wind speed. Conceptually:

- For $v < v_{ci}$ (cut-in): $P=0$
- For $v_{ci} \le v < v_{r}$: $P\propto v^3$ (growing)
- For $v_{r} \le v \le v_{co}$: $P= P_{\text{nameplate}}$ (flat/capped)
- For $v > v_{co}$ (cut-out): $P=0$

This “capping” is why rated power differs from mean power computed from average wind speed with EPF.

---

## Units

- Power units: kW, MW, GW — the app scales values for display; the underlying computation uses SI.
- Energy units: MWh/yr, GWh/yr, TWh/yr — derived directly from mean power and hours per year.
- Thousands separators are shown for readability.

---

## Worked example (illustrative)

Suppose at hub height:

- $\rho = 1.225\,\text{kg/m}^3$, $\bar{v} = 4.47\,\text{m/s}$, $\mathrm{EPF}=1.91$, $\eta = 0.20$
- $D = 100\,\text{m}$, so $A = \tfrac{\pi D^2}{4} \approx 7{,}853.98\,\text{m}^2$

Then:

1) Mean power density
$$
\overline{P}_A = 0.5\times 1.225\times 1.91\times 4.47^3 \;\approx\; 104\;\text{W/m}^2
$$

2) Mean power
$$
\overline{P}_{\text{kW}} = \frac{104\times 7{,}853.98}{1000} \;\approx\; 817.8\;\text{kW}
$$

3) Annual energies
$$
\mathrm{AEP}_{\text{nd}} \approx 817.8\times 8760/1000 \;\approx\; 7{,}163\;\text{MWh/yr}
$$
$$
\mathrm{AEP}_{\text{derated}} = 0.20\times 7{,}163 \;\approx\; 1{,}433\;\text{MWh/yr}
$$

The exact numbers will vary with the app’s lookup values and rounding rules but follow these formulas.

---

## Common questions

- Why does my mean power differ from the manufacturer’s rated power?
  - Rated power is a cap at higher winds; mean power is a time average from average winds (with EPF). They answer different questions.
- Can I plug in a different EPF?
  - Yes conceptually; EPF is a proxy for the wind-speed distribution. In the app it’s embedded in the calculation for convenience.
- Where do losses live?
  - We aggregate them in the derating factor $\eta$.

---

## References and further reading

- See the project README references for sources and context.
- Classic topics to search: “Betz limit,” “wind turbine power curve,” “capacity factor vs rated power,” “Rayleigh or Weibull wind distribution.”
