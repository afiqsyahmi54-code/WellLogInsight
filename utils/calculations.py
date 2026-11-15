# utils/calculations.py - Petrophysical calculations shared by all analysis screens
"""
Pure data functions (no UI code) so they can be reused by every screen and tested on their own.

Conventions
-----------
* Gamma Ray in gAPI, density in g/cm3, neutron in v/v (or %), resistivity in ohm.m.
* Porosity, Vshale and Sw are returned as fractions (0-1), not percentages.
"""
import numpy as np
import pandas as pd

# Default petrophysical assumptions
RHO_MATRIX = 2.65   # g/cm3, sandstone matrix
RHO_FLUID = 1.0     # g/cm3, fresh water
ARCHIE_A = 0.62     # tortuosity factor
DEFAULT_RW = 0.1    # ohm.m, formation water resistivity


def gr_cutoff(gamma_ray):
    """Midpoint between min and max Gamma Ray. Returns None if there is no valid data."""
    gr = pd.Series(gamma_ray).dropna()
    if gr.empty:
        return None
    return (gr.max() - gr.min()) / 2.0 + gr.min()


def detect_reservoir_intervals(depth, gamma_ray, cutoff):
    """
    Find continuous zones where Gamma Ray is below the cut-off (clean sand).

    A NaN Gamma Ray value ends the current zone.

    Returns a list of (top_depth, bottom_depth, min_gr, max_gr) tuples.
    """
    depth = np.asarray(depth, dtype=float)
    gr = np.asarray(gamma_ray, dtype=float)

    with np.errstate(invalid="ignore"):
        in_zone = gr < cutoff          # NaN compares as False

    if not in_zone.any():
        return []

    # Pad with False so every zone has a rising and a falling edge
    edges = np.diff(np.concatenate(([False], in_zone, [False])).astype(np.int8))
    starts = np.flatnonzero(edges == 1)
    ends = np.flatnonzero(edges == -1) - 1   # last row inside each zone

    return [
        (float(depth[s]), float(depth[e]), float(gr[s:e + 1].min()), float(gr[s:e + 1].max()))
        for s, e in zip(starts, ends)
    ]


def calculate_vshale(gamma_ray):
    """
    Linear Vshale from Gamma Ray.

    GR_clean = 10th percentile, GR_shale = 90th percentile.
    Returns (vshale, gr_clean, gr_shale); vshale is NaN everywhere if the GR curve is flat.
    """
    gr = pd.Series(gamma_ray)
    gr_clean = gr.quantile(0.10)
    gr_shale = gr.quantile(0.90)
    span = gr_shale - gr_clean

    if not span > 0:
        return pd.Series(np.nan, index=gr.index), gr_clean, gr_shale

    vsh = ((gr - gr_clean) / span).clip(0, 1)
    return vsh, gr_clean, gr_shale


def calculate_porosity(density, neutron=None, min_phi=0.0):
    """
    Density porosity, averaged with neutron porosity when a neutron curve is given.

    Neutron values above 1 are assumed to be in % and are divided by 100.
    `min_phi` is the lower clip applied to the density porosity.
    """
    density = pd.Series(density)
    phi_density = ((RHO_MATRIX - density) / (RHO_MATRIX - RHO_FLUID)).clip(min_phi, 1)

    if neutron is None:
        return phi_density

    neutron = pd.Series(neutron)
    if neutron.max() > 1:
        neutron = neutron / 100
    return (phi_density + neutron) / 2


def calculate_water_saturation(porosity, resistivity, m=2.0, n=2.0, rw=DEFAULT_RW, a=ARCHIE_A):
    """
    Archie's equation: Sw = (a * Rw / (phi^m * Rt)) ^ (1/n)

    Porosity is clipped to [0.01, 1] and resistivity to [0.1, 10000] to avoid division
    by zero. Raises ValueError if m or n is not positive.
    """
    if m <= 0 or n <= 0:
        raise ValueError("Archie exponents m and n must be positive")

    phi = pd.Series(porosity).clip(0.01, 1.0)
    rt = pd.Series(resistivity).clip(0.1, 10000)

    sw = (a * rw / (phi ** m * rt)) ** (1 / n)
    return sw.clip(0, 1)
