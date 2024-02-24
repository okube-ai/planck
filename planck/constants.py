import numpy as np

from planck._common import shortcuts
from planck._scipy import sp_constants
from planck.models.dimensionalphysicalconstant import DimensionalPhysicalConstant
from planck.models.nondimensionalphysicalconstant import NonDimensionalPhysicalConstant
from planck.units import units


# --------------------------------------------------------------------------- #
# Main Class                                                                  #
# --------------------------------------------------------------------------- #


class Constants(dict):
    """
    Constants library storing `planck.models.DimensionalPhysicalConstant` and
    `planck.models.NonDimensionalPhysicalConstant` models.
    """
    def find(self, sub: str = None) -> list:
        """
        Return list of constant keys containing a given string

        Parameters
        ----------
        sub:
           Sub-string to search keys for. By default, return all keys.

        Returns
        ------
        keys:
           List of keys
        """
        if sub is None:
            sub = ""

        # Get Keys
        keys = []
        for k, v in self.items():
            if sub in k:
                keys += [k]
        keys.sort()

        # Return keys
        return keys


# --------------------------------------------------------------------------- #
# Build Constants                                                             #
# --------------------------------------------------------------------------- #

d = Constants({})

DC = DimensionalPhysicalConstant
NDC = NonDimensionalPhysicalConstant

# Temperature
d["zero_degc"] = DC(
    symbol="zero_degc",
    name="Zero degree celcius",
    values={
        "K": sp_constants.zero_Celsius,
        "degc": 0.0,
    },
)

# Gravitational acceleration
# ref.: https://en.wikipedia.org/wiki/Gravitational_acceleration
d["g_acc"] = DC(
    symbol="g_acc",
    name="Gravitational acceleration",
    values={
        "m/s2": sp_constants.g,
        "ft/s2": sp_constants.g * units["m"]["ft"],
    },
)


# Earth radius
# ref.: https://en.wikipedia.org/wiki/Earth_radius
d["earth_radius"] = DC(
    "earth_radius",
    "Earth radius",
    {
        "m": 6371000,
        "ft": 6371000 * units["m"]["ft"],
        "km": 6371000 * units["m"]["km"],
    },
)

# Gas Constant
# ref.: https://en.wikipedia.org/wiki/Gas_constant
d["R"] = DC(
    "R",
    "Gas constant for air",
    {
        "kg*m2/mol/K/s2": sp_constants.R,
        "ft2/s2/K": sp_constants.R * units["m2"]["ft2"],
    },
)
d["R_air"] = DC(
    "R_air",
    "Specific gas constant for air",
    {"m2/s2/K": 287.058},
)

# Ideal Gas Model
# ref.: https://en.wikipedia.org/wiki/Ideal_gas
d["gamma_air"] = NDC("gamma_air", "Ratio of specific heats (cp/cv) for air", 1.4)

# ISA Atmospheric Model
# ref.: https://en.wikipedia.org/wiki/International_Standard_Atmosphere
d["isa_T0"] = DC("isa_T0", "ISA temperature at sea level", {"K": 288.15})

d["isa_p0"] = DC(
    "isa_p0",
    "ISA pressure at sea level",
    {
        "Pa": 101325,
        "lb/ft2": 101325 * units["Pa"]["lb/ft2"],
    },
)

d["isa_rho0"] = DC(
    "isa_rho0",
    "ISA density at sea level",
    {
        "kg/m3": 1.2250,
        "slug/ft3": 1.2250 * units["kg"]["slug"] / units["m3"]["ft3"],
    },
)

d["isa_c0"] = DC(
    "isa_c0",
    "ISA speed of sound at sea level",
    {
        "m/s": np.sqrt(d["gamma_air"] * d["isa_p0"]["Pa"] / d["isa_rho0"]["kg/m3"]),
        "ft/s": np.sqrt(d["gamma_air"] * d["isa_p0"]["Pa"] / d["isa_rho0"]["kg/m3"])
        * units["m/s"]["ft/s"],
    },
)

d["isa_lapse_rate"] = DC(
    "isa_lapse_rate",
    "ISA lapse rate",
    {
        "degc/m": -6.5e-3,
        "degc/ft": -6.5e-3 / units["m"]["ft"],
    },
)

d["isa_alt_tropo"] = DC(
    "isa_alt_tropo",
    "ISA altitude AT tropopause",
    {
        "m": 11000,
        "ft": 11000 * units["m"]["ft"],
    },
)

d["isa_T_tropo"] = DC(
    "isa_T_tropo",
    "ISA temperature at tropopause",
    {"K": d["isa_T0"]["K"] + d["isa_lapse_rate"]["degc/m"] * d["isa_alt_tropo"]["m"]},
)

d["isa_Tc_tropo"] = DC(
    "isa_Tc_tropo",
    "ISA temperature constant at tropopause",
    {
        "1/m": d["g_acc"]["m/s2"] / (d["R_air"]["m2/s2/K"] * d["isa_T_tropo"]["K"]),
        "1/ft": d["g_acc"]["m/s2"]
        / (d["R_air"]["m2/s2/K"] * d["isa_T_tropo"]["K"])
        / units["m"]["ft"],
    },
)

d["isa_pc_tropo"] = NDC(
    "isa_pc_tropo",
    "ISA pressure constant at tropopause",
    -d["g_acc"]["m/s2"] / (d["R_air"]["m2/s2/K"] * d["isa_lapse_rate"]["degc/m"]),
)

d["isa_p_tropo"] = DC(
    "isa_p_tropo",
    "ISA pressure at tropopause",
    {
        "Pa": d["isa_p0"]["Pa"]
        * (d["isa_T_tropo"]["K"] / d["isa_T0"]["K"]) ** d["isa_pc_tropo"],
        "lb/ft2": d["isa_p0"]["Pa"]
        * (d["isa_T_tropo"]["K"] / d["isa_T0"]["K"]) ** d["isa_pc_tropo"]
        * units["Pa"]["lb/ft2"],
    },
)


d["planck"] = DC(
    "planck",
    "Planck constant (h)",
    {
        "J*Hz": 6.62607015e-34,
    },
)

# --------------------------------------------------------------------------- #
# Update shortcuts                                                            #
# --------------------------------------------------------------------------- #

for k0 in list(d.keys()):
    for k1 in list(d[k0].keys()):
        if k1 in shortcuts:
            d[k0][shortcuts[k1]] = d[k0][k1]

constants = d
"""Constants Library"""
