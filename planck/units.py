from typing import Union
from typing import List
import numpy as np

from planck._scipy import sp_constants
from planck.models.unit import Unit
from planck._common import shortcuts


TEMPERATURE_UNITS = [
    "degc",
    "c",
    "celcius",
    "k",
    "kelvin",
    "fahrenheit",
    "f",
    "rankine",
    "r",
]


# --------------------------------------------------------------------------- #
# Main Class                                                                  #
# --------------------------------------------------------------------------- #


class Units(dict):
    """
    Units library storing `planck.models.Unit` models.
    """
    def convert(
        self, value: Union[float, np.array], input_unit: str, output_unit: str
    ) -> Union[float, np.array]:
        """
        Convert a `value` from `input_unit` to `output_unit`

        Parameters
        ----------
        value:
            Value to convert
        input_unit:
            Source unit
        output_unit:
            Target unit

        Returns
        -------
        :
            Value expressed as `output_unit`

        Examples
        --------
        ```py
        from planck import units

        print(units.convert(1.0, "m", "ft"))
        #> 3.280839895013124

        print(units.convert(0.0, "C", "K"))
        #> 273.15
        ```
        """

        # Temperature
        if input_unit.lower() in TEMPERATURE_UNITS:
            if input_unit == "degc":
                input_unit = "c"
            if output_unit == "degc":
                output_unit = "c"
            return sp_constants.convert_temperature(value, input_unit, output_unit)

        return value * self[input_unit][output_unit]

    def find(self, sub: str = None, quantity: str = None) -> list:
        """
        Return unit keys containing a given string

        Parameters
        ----------
        sub:
           Sub-string to search keys for. By default, return all keys.
        quantity:
           Specific quantity ["length", "mass", "volume", "pressure", etc.]

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
                if not quantity or v.quantity == quantity.lower():
                    keys += [k]
        keys.sort()

        # Return keys
        return keys


# --------------------------------------------------------------------------- #
# Build Constants                                                             #
# --------------------------------------------------------------------------- #

d = Units({})

# --------------------------------------------------------------------------- #
# Base Units                                                                  #
# ref : https://en.wikipedia.org/wiki/SI_base_unit                            #
# --------------------------------------------------------------------------- #

# Length
s = "m"
d[s] = Unit(
    symbol=s,
    quantity="length",
    values={
        "in": 1.0 / sp_constants.inch,
        "ft": 1.0 / sp_constants.foot,
        "mi": 1.0 / sp_constants.mile,
        "NM": 1.0 / sp_constants.nautical_mile,
    },
    si_prefixes=["m", "c", "", "k"],
)

# Mass
s = "kg"
d[s] = Unit(
    symbol=s,
    quantity="mass",
    values={
        "lb": 1.0 / sp_constants.pound,
        "slug": 1.0 / sp_constants.pound / (sp_constants.g * d["m"]["ft"]),
    },
    si_prefixes=["m", "", "k"],
)

# Time
s = "s"
d[s] = Unit(
    symbol=s,
    quantity="time",
    values={
        "min": 1 / sp_constants.minute,
        "h": 1 / sp_constants.hour,
        "d": 1 / sp_constants.day,
        "week": 1 / int(7 * 24 * 3600),
        "month": 1 / int(365 / 12 * 24 * 3600),
        "a": 1 / sp_constants.year,
    },
    si_prefixes=["", "m", "mu", "n"],
)


# --------------------------------------------------------------------------- #
# Derived Units                                                               #
# ref : https://en.wikipedia.org/wiki/SI_derived_unit                         #
# --------------------------------------------------------------------------- #

# Area
s = "m2"
d[s] = Unit(
    symbol=s,
    quantity="area",
    values={
        "in2": d[s[:-1]]["in"] ** 2,
        "ft2": d[s[:-1]]["ft"] ** 2,
        "mi2": d[s[:-1]]["mi"] ** 2,
    },
    si_prefixes=["m", "c", "", "k"],
    order=2,
)

# Volume
s = "m3"
d[s] = Unit(
    symbol=s,
    quantity="area",
    values={
        "in3": d[s[:-1]]["in"] ** 3,
        "ft3": d[s[:-1]]["ft"] ** 3,
        "mi3": d[s[:-1]]["mi"] ** 3,
    },
    si_prefixes=["m", "c", "", "k"],
    order=3,
)

# Velocity
s = "m/s"
d[s] = Unit(
    symbol=s,
    quantity="velocity",
    values={
        "ft/s": d["m"]["ft"],
        "km/h": d["m"]["km"] / d["s"]["h"],
        "ft/min": d["m"]["ft"] / d["s"]["min"],
        "kt": d["m"]["NM"] / d["s"]["h"],
    },
)

# Angle
s = "rad"
d[s] = Unit(
    symbol=s,
    quantity="angle",
    values={
        "deg": 1.0 / sp_constants.degree,
    },
)

# Angular velocity
s = "rad/s"
d[s] = Unit(
    symbol=s,
    quantity="angular velocity",
    values={
        "deg/s": 1 * d["rad"]["deg"],
    },
)

# Mass flow rate
s = "kg/s"
d[s] = Unit(
    symbol=s,
    quantity="mass flow rate",
    values={
        "kg/h": 1 / d["s"]["h"],
        "lb/s": d["kg"]["lb"],
        "lb/h": d["kg"]["lb"] / d["s"]["h"],
    },
)

# Frequency
s = "Hz"
d[s] = Unit(
    symbol=s,
    quantity="frequency",
    values={
        "1/s": 1.0,
        "1/min": 1 / d["s"]["min"],
        "rad/s": 2 * np.pi,
    },
    si_prefixes=["", "k", "M"],
)

# Force
s = "N"
d[s] = Unit(
    symbol=s,
    quantity="force",
    values={
        "kg*m/s2": 1.0,
        "lb": d["kg"]["lb"] / sp_constants.g,
    },
    si_prefixes=["", "k"],
)

# Pressure
s = "Pa"
d[s] = Unit(
    symbol=s,
    quantity="pressure",
    values={
        "N/m2": 1.0,
        "kg/m/s2": 1.0,
        "lb/in2": d["kg"]["lb"] / d["m2"]["in2"] / sp_constants.g,
        "lb/ft2": d["kg"]["lb"] / d["m2"]["ft2"] / sp_constants.g,
        "bar": 1.0 / sp_constants.bar,
        "mbar": 1.0 / sp_constants.bar * 1000.0,
        "kPa": 1.0 / 1e3,
        "MPa": 1.0 / 1e6,
    },
)

# Torque
s = "N*m"
d[s] = Unit(
    symbol=s,
    quantity="torque",
    values={
        "J": 1.0,
        "m2*kg/s2": 1.0,
        "lb*in": d["kg"]["slug"] * d["m"]["ft"] * d["m"]["in"],
        "lb*ft": d["kg"]["slug"] * d["m"]["ft"] * d["m"]["ft"],
    },
)


# Power
s = "W"
d[s] = Unit(
    symbol=s,
    quantity="power",
    values={
        "kg*m2/s3": 1.0,
        "J/s": 1.0,
        "hp": 1.0 / sp_constants.hp,
        "ft*lb/s": 1.0 / sp_constants.hp * 550,
        "ft*lb/min": 1.0 / sp_constants.hp * 550 * sp_constants.minute,
    },
    si_prefixes=["", "k", "M"],
)

# Density
s = "g/m3"
d[s] = Unit(
    symbol=s,
    quantity="density",
    values={
        "slug/ft3": d["kg"]["slug"] / d["m3"]["ft3"],
        "kg/m3": 1.0 / 1000.0,
    },
)

# --------------------------------------------------------------------------- #
# Create shortcuts                                                            #
# --------------------------------------------------------------------------- #

for k0 in list(d.keys()):
    for k1 in list(d[k0].keys()):
        if k1 in shortcuts:
            d[k0][shortcuts[k1]] = d[k0][k1]


# --------------------------------------------------------------------------- #
# Create all permutations                                                     #
# --------------------------------------------------------------------------- #

# Permutations of output units
for k0 in list(d.keys()):
    k1s = list(d[k0].keys())
    for k1 in k1s:
        for k2 in k1s:
            if k1 not in d.keys():
                d[k1] = Unit(symbol=k1, quantity=d[k0].quantity)
            if k2 not in d[k1].keys():
                d[k1][k2] = d[k0][k2] / d[k0][k1]

# Inverse relationships
for k0 in list(d.keys()):
    for k1 in list(d[k0].keys()):
        if k1 not in d.keys():
            d[k1] = Unit(symbol=k1, quantity=d[k0].quantity)
        if k0 not in d[k1].keys():
            d[k1][k0] = 1.0 / d[k0][k1]

units = d
"""Units Library"""
