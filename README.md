## Offshore wind calculator
 
### Quick description 
The notebook in this repo allows quick interactive wind power calculations using Panel. Users can estimate a wind turbine's output on rotor diameter and wind speed, and also site-wide energy production based on available area in squared kilometers, and a turbine density factor.

### Assumptions
I made a number of educated assumptions, based on published engineering formulas, and literature research. They are summarized below:

- **Lookup Tables:** Air density and wind speed values are derived from published sources (von Krauland et al., 2023, and references therein) and are indexed by rotor diameter, representing typical offshore conditions at various hub heights. For simplicity the rotor diameter and hub height (for wind speed choice) are set to equal.

- **Default Parameters:**
  - Air density defaults to 0.990 kg/m³ (200 m altitude) unless otherwise specified. Assuming Installation of Vestas' V236 15.0MW, or similar turbines.
  - Energy pattern factor is set to 1.91, corresponding to a Rayleigh wind speed distribution (Weibull k=2).
  - Efficiency factor for derating annual energy output is fixed at 0.2 (20%). This is a coservative value, well below the Betz Limit, lumping efficiency, partial wake, total wake effects.
  - Turbine spacing factor is set to 5.98, following once again work cited in von Krauland et al.


These assumptions are intended to provide representative, but not site-specific, estimates.

## References
    - Harness It, by Michael Ginsberg, 2019, Business Expert Press
    - von Krauland et al., 2023, [United States offshore wind energy atlas](https://doi.org/10.1016/j.ecmx.2023.100410)
	
	
Click the button to launch app 
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mycarta/wind-calculator/HEAD?urlpath=%2Fdoc%2Ftree%2FPanel_app_pkg.ppynb)
