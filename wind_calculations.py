import numpy as np


# Lookup tables for air density and wind speed by height (rotor diameter)
# Both tables are derived from von Krauland et al., 2023
air_density_lookup = {
    100: 1.000,
    150: 0.995,
    200: 0.990,
    250: 0.986
}
wind_speed_lookup = {
    100: 9.54,
    150: 9.92,
    200: 10.10,
    250: 10.25
}

def annual_power_density(wind_speed: float, air_density: float = 0.990, energy_pattern_factor: float = 1.91) -> np.float64:
    """
    Calculate the annual average power density of wind.

    Parameters:
    -----------
    wind_speed : float
        Mean wind speed in m/s (rounded to 2 decimal places)
    air_density : float, optional
        Air density in kg/m³, default 0.990 (value at 200 m altitude).
        Other typical values:
            - 0 m (sea level): 1.225
            - 100 m: 1.000
            - 150 m: 0.995
            - 250 m: 0.986

    energy_pattern_factor : float, optional
        Default is 1.91, representing a Rayleigh distribution (k=2)
        This is a measure of the wind speed distribution's effect on available power
        For Weibull distribution with shape parameter k=2 (Rayleigh distribution)

    Returns:
    --------
    np.float64
        Annual average power density in W/m² (rounded to nearest integer)
    """
    wind_speed = np.round(wind_speed, 2)
    power_density = 0.5 * air_density * energy_pattern_factor * (wind_speed ** 3)
    return np.rint(power_density)

def swept_area(diameter: float) -> float:
    """
    Calculate the swept area of a wind turbine rotor.
    
    Parameters:
    -----------
    diameter : float
        Rotor diameter in meters.
    
    Returns:
    --------
    float
        Swept area in square meters (m²).
    """
    return np.pi * (diameter / 2) ** 2

def power_kw(power_density: float, rotor_diameter: float) -> float:
    """
    Calculate the total power output in kW given annual power density (W/m²) and rotor diameter.
    Uses the swept_area function to compute the rotor swept area.

    Parameters:
    -----------
    power_density : float
        Annual power density in W/m².
    rotor_diameter : float
        Rotor diameter in meters.

    Returns:
    --------
    float
        Total power output in kW, rounded to nearest integer.

    """
    area = swept_area(rotor_diameter)
    return np.rint((power_density * area) / 1000)


def derated_annual_energy_output(power_kw: float, efficiency: float = 0.2) -> float:
    """
    Calculate the annual energy output in MWh/year from power (kW) and efficiency factor.

    Parameters:
    -----------
    power_kw : float
        Power output in kW (e.g., from power_kw function).
    efficiency : float, optional
        Efficiency factor (default 0.2 for 20% derating).

    Returns:
    --------
    float
        Annual energy output in MWh/year, rounded to nearest integer.

    Example:
    --------
    >>> annual_energy_output(2308, 0.2)
    4036
    # Annual energy = 2308 kW * 8760 h/year * 0.2 / 1000 = 4035.8 MWh/year
    # Rounded to nearest integer: 4036 MWh/year
    """
    annual_energy_mwh = power_kw * 8760 * efficiency / 1000
    return np.rint(annual_energy_mwh)

def annual_energy_output(power_kw_val):
    """
    Calculate the non-derated annual energy output in MWh/year from power (kW).
    """
    annual_energy_mwh = power_kw_val * 8760 / 1000
    return np.rint(annual_energy_mwh)

def possible_turbine_installations(available_area_km2: float, rotor_diameter_m: float, spacing_factor: float = 5.98) -> int:
    """
    Calculate the number of possible realizable wind turbine installations (Nturb).

    Nturb = Available Area (m²) / Turbine Spacing Density (m²)
    Turbine Spacing Density = (F * Rotor Diameter (m))^2
    Where F is the spacing factor (default 5.98 for offshore wind farms)
    as suggested in United States offshore wind energy atlas, von Krauland et al. (2023)

    Parameters:
    -----------
    available_area_km2 : float
        Total available area in square kilometers (km²).
    rotor_diameter_m : float
        Turbine rotor diameter in meters (m).
    spacing_factor : float, optional
        Spacing factor F (default 5.98 for offshore wind farms).

    Returns:
    --------
    int
        Number of possible wind turbine installations (rounded down to nearest integer).

    Example:
    --------
    >>> possible_turbine_installations(1, 50)
    # Available Area = 1 km² = 1,000,000 m²
    # Turbine Spacing Density = (5.98 * 50)^2 = 89,402 m²
    # Nturb = 1,000,000 / 89,402 = 11.18 -> 11 turbines (rounded down)
    """
    available_area_m2 = available_area_km2 * 1_000_000
    spacing_density = (spacing_factor * rotor_diameter_m) ** 2
    nturb = available_area_m2 // spacing_density
    return int(nturb)
