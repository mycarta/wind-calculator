"""Tests for wind_calculations.

For Windows PowerShell run instructions, see README.md ("Running tests").
"""

import numpy as np
import pytest

from wind_calculations import (
    annual_power_density,
    swept_area,
    power_kw,
    derated_annual_energy_output,
    annual_energy_output,
    possible_turbine_installations,
    air_density_lookup,
    wind_speed_lookup,
)


# --------------------------
# Unit tests: core formulas
# --------------------------

@pytest.mark.parametrize(
    "wind_speed,air_density,epf,expected",
    [
        # Simple sanity: 0.5 * 1.0 * 2.0 * 10^3 = 1000 -> rounds to 1000
        (10.0, 1.0, 2.0, 1000),
        # Defaults in module docstring context: rho=0.99, epf=1.91, v=10
        # 0.5 * 0.99 * 1.91 * 1000 = 945.45 -> rounds to 945
        (10.0, 0.99, 1.91, 945),
        # Zero wind should yield zero power density
        (0.0, 1.225, 1.91, 0),
    ],
)
def test_annual_power_density_known_values(wind_speed, air_density, epf, expected):
    result = int(annual_power_density(wind_speed, air_density, epf))
    assert result == expected


def test_annual_power_density_rounds_wind_speed_to_2dp():
    # Function rounds wind_speed to 2 decimals internally
    v_raw = 5.12345
    v = np.round(v_raw, 2)
    expected = np.rint(0.5 * 1.0 * 2.0 * (v ** 3))
    result = annual_power_density(v_raw, 1.0, 2.0)
    assert result == expected


@pytest.mark.parametrize(
    "diameter,expected",
    [
        (100.0, np.pi * (100.0 / 2) ** 2),
        (0.0, 0.0),
    ],
)
def test_swept_area_values(diameter, expected):
    assert np.isclose(swept_area(diameter), expected, rtol=1e-12, atol=1e-9)


def test_swept_area_negative_diameter_matches_positive():
    # Current implementation will square diameter, so negative yields same area
    assert np.isclose(swept_area(-100.0), swept_area(100.0))


@pytest.mark.parametrize(
    "power_density,diameter,expected",
    [
        # With PD=1000 W/m^2, power_kW equals rotor swept area (in m^2), rounded
        (1000.0, 100.0, int(np.rint(np.pi * (100.0 / 2) ** 2))),
        (0.0, 120.0, 0),
    ],
)
def test_power_kw_values(power_density, diameter, expected):
    assert int(power_kw(power_density, diameter)) == expected


@pytest.mark.parametrize(
    "kw,expected",
    [
        (2308.0, int(np.rint(2308.0 * 8760 / 1000))),  # 20,218.08 -> 20218
        (0.0, 0),
    ],
)
def test_annual_energy_output_values(kw, expected):
    assert int(annual_energy_output(kw)) == expected


@pytest.mark.parametrize(
    "kw,eff,expected",
    [
        # Note: 2308*8760*0.2/1000 = 4043.616 -> rounds to 4044
        (2308.0, 0.2, int(np.rint(2308.0 * 8760 * 0.2 / 1000))),
        (2308.0, 0.0, 0),
        # Efficiency 1 should match non-derated AEP (up to rounding which is identical here)
        (2308.0, 1.0, int(np.rint(2308.0 * 8760 / 1000))),
    ],
)
def test_derated_annual_energy_output_values(kw, eff, expected):
    assert int(derated_annual_energy_output(kw, eff)) == expected


def test_derated_not_exceed_non_derated_for_0_to_1():
    kw = 1500.0
    non_derated = annual_energy_output(kw)
    for eff in np.linspace(0.0, 1.0, 11):
        derated = derated_annual_energy_output(kw, eff)
        assert derated <= non_derated


def test_worked_example_reference_case():
    """
    Reference worked example:
    - rotor diameter = 50 m
    - wind speed = 4.47 m/s
    - energy pattern factor (EPF) = 1.91
    - air density ~ sea level = 1.225 kg/m^3
    - efficiency = 20%

    Expected derated annual energy output ≈ 357 MWh/year.
    We also validate key intermediates to guard against formula regressions.

    Source: "Harness It" (Michael Ginsberg, 2019), see README References.
    """
    v = 4.47
    rho = 1.225
    epf = 1.91
    d = 50.0
    eff = 0.20

    apd = annual_power_density(v, rho, epf)            # W/m^2 (rounded integer float)
    assert int(apd) == 104

    pkw = power_kw(apd, d)                              # kW (rounded integer float)
    assert int(pkw) == 204

    aep = annual_energy_output(pkw)                     # MWh/year (rounded integer float)
    assert int(aep) == 1787

    derated = derated_annual_energy_output(pkw, eff)    # MWh/year (rounded integer float)
    assert int(derated) == 357


@pytest.mark.parametrize(
    "area_km2,diameter,spacing,expected",
    [
        (1.0, 50.0, 6.0, 11),  # Example from docstring
        (0.0, 50.0, 6.0, 0),   # No area -> 0 turbines
        (2.0, 100.0, 10.0, 2), # 2e6 / (1000^2) = 2 -> 2 turbines
    ],
)
def test_possible_turbine_installations_values(area_km2, diameter, spacing, expected):
    assert possible_turbine_installations(area_km2, diameter, spacing) == expected


def test_possible_turbine_installations_zero_division_cases():
    # spacing_factor = 0 or rotor_diameter = 0 leads to division by zero in current implementation
    with pytest.raises(ZeroDivisionError):
        possible_turbine_installations(1.0, 0.0, 6.0)
    with pytest.raises(ZeroDivisionError):
        possible_turbine_installations(1.0, 50.0, 0.0)


# --------------------------
# Light property checks
# --------------------------
try:
    from hypothesis import given, strategies as st  # type: ignore
except Exception:  # pragma: no cover
    # Fallback shim: if Hypothesis isn't installed, bind 'given' to a decorator
    # that marks tests as skipped, and provide a stub 'st' with compatible API.
    import pytest as _pytest  # type: ignore

    def given(*_args, **_kwargs):  # type: ignore
        def _decorator(fn):
            return _pytest.mark.skip(reason="hypothesis not installed")(fn)
        return _decorator

    class _St:  # minimal strategy stub
        def floats(self, *args, **kwargs):  # type: ignore
            return None

    st = _St()  # type: ignore


@given(
    st.floats(min_value=0.0, max_value=60.0),
    st.floats(min_value=0.0, max_value=60.0),
)
def test_apd_monotonic_in_wind_speed(v1, v2):
    # Non-decreasing with wind speed for non-negative speeds
    apd1 = annual_power_density(v1)
    apd2 = annual_power_density(v2)
    # If v2 >= v1 then apd2 >= apd1 (ties possible due to rounding)
    if v2 >= v1:
        assert apd2 >= apd1
    else:
        assert apd1 >= apd2


@given(
    st.floats(min_value=0.1, max_value=200.0),
    st.floats(min_value=0.1, max_value=10.0),
)
def test_possible_turbines_monotonic_in_area(area_km2, delta):
    # Increasing area should not decrease turbine count
    nt1 = possible_turbine_installations(area_km2, 80.0, 6.0)
    nt2 = possible_turbine_installations(area_km2 + delta, 80.0, 6.0)
    assert nt2 >= nt1


# --------------------------
# Lookup table sanity checks
# --------------------------

def test_lookup_tables_have_expected_keys():
    assert set(air_density_lookup.keys()) == {100, 150, 200, 250}
    assert set(wind_speed_lookup.keys()) == {100, 150, 200, 250}


def test_lookup_values_are_positive():
    assert all(v > 0 for v in air_density_lookup.values())
    assert all(v > 0 for v in wind_speed_lookup.values())
