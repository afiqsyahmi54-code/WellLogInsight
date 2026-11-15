import numpy as np
import pandas as pd
import pytest

from utils.calculations import (
    calculate_porosity,
    calculate_vshale,
    calculate_water_saturation,
    detect_reservoir_intervals,
    gr_cutoff,
)


def loop_intervals(depth, gr_values, cutoff):
    """The original row-by-row logic used in the screens, kept as a reference."""
    intervals, in_zone, start, prev = [], False, None, None
    min_gr = max_gr = None
    for d, gr in zip(depth, gr_values):
        if pd.isna(gr):
            if in_zone:
                intervals.append((start, prev, min_gr, max_gr))
                in_zone = False
            continue
        if gr < cutoff:
            if not in_zone:
                in_zone, start, min_gr, max_gr = True, d, gr, gr
            else:
                min_gr, max_gr = min(min_gr, gr), max(max_gr, gr)
        elif in_zone:
            intervals.append((start, prev, min_gr, max_gr))
            in_zone = False
        prev = d
    if in_zone:
        intervals.append((start, prev, min_gr, max_gr))
    return intervals


# ---------- gr_cutoff ----------

def test_gr_cutoff_is_midpoint():
    assert gr_cutoff([20, 60, 100]) == 60


def test_gr_cutoff_ignores_nan():
    assert gr_cutoff([np.nan, 20, 100]) == 60


def test_gr_cutoff_empty_returns_none():
    assert gr_cutoff([np.nan, np.nan]) is None


# ---------- detect_reservoir_intervals ----------

def test_intervals_simple_zone():
    depth = [1, 2, 3, 4, 5, 6]
    gr = [90, 30, 40, 90, 20, 90]
    assert detect_reservoir_intervals(depth, gr, 50) == [
        (2.0, 3.0, 30.0, 40.0),
        (5.0, 5.0, 20.0, 20.0),
    ]


def test_intervals_none_found():
    assert detect_reservoir_intervals([1, 2, 3], [90, 95, 100], 50) == []


def test_intervals_zone_at_end_of_log():
    assert detect_reservoir_intervals([1, 2, 3], [90, 30, 20], 50) == [(2.0, 3.0, 20.0, 30.0)]


def test_nan_ends_a_zone():
    depth = [1, 2, 3, 4]
    gr = [30, 30, np.nan, 30]
    assert detect_reservoir_intervals(depth, gr, 50) == [
        (1.0, 2.0, 30.0, 30.0),
        (4.0, 4.0, 30.0, 30.0),
    ]


def test_intervals_match_original_loop_on_random_data():
    rng = np.random.default_rng(0)
    for _ in range(25):
        depth = np.arange(500) * 0.5 + 1000
        gr = rng.uniform(10, 150, 500)
        gr[rng.random(500) < 0.05] = np.nan
        cutoff = gr_cutoff(gr)
        expected = loop_intervals(depth, gr, cutoff)
        actual = detect_reservoir_intervals(depth, gr, cutoff)
        assert len(actual) == len(expected)
        assert np.allclose(np.array(actual), np.array(expected, dtype=float))


# ---------- calculate_vshale ----------

def test_vshale_bounds_and_ordering():
    gr = pd.Series(np.linspace(20, 120, 101))
    vsh, gr_clean, gr_shale = calculate_vshale(gr)
    assert vsh.min() == 0 and vsh.max() == 1
    assert gr_clean == pytest.approx(30)
    assert gr_shale == pytest.approx(110)
    assert vsh.is_monotonic_increasing


def test_vshale_flat_curve_is_nan_not_inf():
    vsh, _, _ = calculate_vshale(pd.Series([50.0] * 10))
    assert vsh.isna().all()


# ---------- calculate_porosity ----------

def test_porosity_density_only():
    # (2.65 - 2.325) / 1.65 = 0.1969...
    phi = calculate_porosity(pd.Series([2.325]))
    assert phi.iloc[0] == pytest.approx(0.325 / 1.65)


def test_porosity_clipped_to_zero_and_one():
    phi = calculate_porosity(pd.Series([3.2, 0.5]))
    assert list(phi) == [0.0, 1.0]


def test_porosity_averages_with_neutron():
    phi = calculate_porosity(pd.Series([2.65]), pd.Series([0.20]))
    assert phi.iloc[0] == pytest.approx(0.10)


def test_neutron_in_percent_is_converted():
    as_fraction = calculate_porosity(pd.Series([2.3]), pd.Series([0.25]))
    as_percent = calculate_porosity(pd.Series([2.3]), pd.Series([25.0]))
    assert as_percent.iloc[0] == pytest.approx(as_fraction.iloc[0])


# ---------- calculate_water_saturation ----------

def test_archie_known_value():
    # phi=0.25, Rt=20, Rw=0.1, a=0.62, m=n=2 -> sqrt(0.062 / (0.0625 * 20)) = 0.2227
    sw = calculate_water_saturation(pd.Series([0.25]), pd.Series([20.0]))
    assert sw.iloc[0] == pytest.approx(np.sqrt(0.062 / 1.25))


def test_sw_higher_resistivity_means_lower_sw():
    sw = calculate_water_saturation(pd.Series([0.2, 0.2]), pd.Series([5.0, 50.0]))
    assert sw.iloc[1] < sw.iloc[0]


def test_sw_is_clipped_between_zero_and_one():
    sw = calculate_water_saturation(pd.Series([0.0, 0.3]), pd.Series([0.1, 100000.0]))
    assert sw.between(0, 1).all()


@pytest.mark.parametrize("m, n", [(0, 2), (2, 0), (-1, 2)])
def test_sw_rejects_non_positive_exponents(m, n):
    with pytest.raises(ValueError):
        calculate_water_saturation(pd.Series([0.2]), pd.Series([10.0]), m=m, n=n)
