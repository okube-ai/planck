import numpy as np
import math
import re

from collections import UserDict


# --------------------------------------------------------------------------- #
# Local Constants                                                             #
# --------------------------------------------------------------------------- #

DEFAULT_PERIOD = "1d"


# Scipy.constants mock
class ScipyConstants:
    def __init__(self):
        self.inch = 0.0254
        self.foot = 12 * self.inch
        self.yard = 3 * self.foot
        self.mile = 1760 * self.yard
        self.nautical_mile = 1852.0

        self.metric_ton = 1e3
        self.grain = 64.79891e-6
        self.pound = 7000 * self.grain  # avoirdupois

        self.g = 9.80665

        self.minute = 60.0
        self.hour = 60 * self.minute
        self.day = 24 * self.hour
        self.week = 7 * self.day
        self.year = 365 * self.day

        self.pi = math.pi
        self.degree = self.pi / 180

        self.bar = 1e5
        self.hp = 550 * self.foot * self.pound * self.g
        self.zero_Celsius = 273.15
        self.R = 8.314462618

    def convert_temperature(self, val, old_scale, new_scale):
        """
        Convert from a temperature scale to another one among Celsius, Kelvin,
        Fahrenheit, and Rankine scales.

        Parameters
        ----------
        val : array_like
            Value(s) of the temperature(s) to be converted expressed in the
            original scale.

        old_scale: str
            Specifies as a string the original scale from which the temperature
            value(s) will be converted. Supported scales are Celsius ('Celsius',
            'celsius', 'C' or 'c'), Kelvin ('Kelvin', 'kelvin', 'K', 'k'),
            Fahrenheit ('Fahrenheit', 'fahrenheit', 'F' or 'f'), and Rankine
            ('Rankine', 'rankine', 'R', 'r').

        new_scale: str
            Specifies as a string the new scale to which the temperature
            value(s) will be converted. Supported scales are Celsius ('Celsius',
            'celsius', 'C' or 'c'), Kelvin ('Kelvin', 'kelvin', 'K', 'k'),
            Fahrenheit ('Fahrenheit', 'fahrenheit', 'F' or 'f'), and Rankine
            ('Rankine', 'rankine', 'R', 'r').

        Returns
        -------
        res : float or array of floats
            Value(s) of the converted temperature(s) expressed in the new scale.

        Notes
        -----
        .. versionadded:: 0.18.0

        Examples
        --------
        >>> from scipy.constants import convert_temperature
        >>> convert_temperature(np.array([-40, 40]), 'Celsius', 'Kelvin')
        array([ 233.15,  313.15])

        """
        # Convert from `old_scale` to Kelvin
        if old_scale.lower() in ['celsius', 'c']:
            tempo = np.asanyarray(val) + self.zero_Celsius
        elif old_scale.lower() in ['kelvin', 'k']:
            tempo = np.asanyarray(val)
        elif old_scale.lower() in ['fahrenheit', 'f']:
            tempo = (np.asanyarray(val) - 32) * 5 / 9 + self.zero_Celsius
        elif old_scale.lower() in ['rankine', 'r']:
            tempo = np.asanyarray(val) * 5 / 9
        else:
            raise NotImplementedError("%s scale is unsupported: supported scales "
                                      "are Celsius, Kelvin, Fahrenheit, and "
                                      "Rankine" % old_scale)
        # and from Kelvin to `new_scale`.
        if new_scale.lower() in ['celsius', 'c']:
            res = tempo - self.zero_Celsius
        elif new_scale.lower() in ['kelvin', 'k']:
            res = tempo
        elif new_scale.lower() in ['fahrenheit', 'f']:
            res = (tempo - self.zero_Celsius) * 9 / 5 + 32
        elif new_scale.lower() in ['rankine', 'r']:
            res = tempo * 9 / 5
        else:
            raise NotImplementedError("'%s' scale is unsupported: supported "
                                      "scales are 'Celsius', 'Kelvin', "
                                      "'Fahrenheit', and 'Rankine'" % new_scale)

        return res



sp_constants = ScipyConstants()


# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #

def _split_symbol(symbol):
    # Input validation
    nd = len(symbol.split("/"))
    nm = len(symbol.split("*"))
    if nd > 1 or nm > 1:
        raise TypeError("Multi-units are not supported.")

    # Get prefix and base
    p0 = ""
    for p in si_prefixes.keys():
        if p != "":
            if re.match(p + r"\D{1}", symbol):
                p0 = p
    base = symbol.replace(p0, "", 1)

    return p0, base


# --------------------------------------------------------------------------- #
# Classes                                                                     #
# --------------------------------------------------------------------------- #

class UnitConstant(UserDict):
    def __init__(self, symbol, name, quantity, *args, **kwargs):
        self.symbol = symbol
        self.name = name
        self.quantity = quantity
        super(UnitConstant, self).__init__(*args, **kwargs)

    def add_metric_prefixes(self, prefixes, order=1):
        for p in prefixes:
            p0, k = _split_symbol(self.symbol)
            self[p + k] = (si_prefixes[p0][0] / si_prefixes[p][0]) ** order

    def __repr__(self, *args, **kwargs):
        s = ""
        s += "Unit of {0:s} - ".format(self.quantity)
        s += "{0:s} [{1:s}]\n".format(self.name, self.symbol)
        s += "Conversions : "
        s += super(UnitConstant, self).__repr__(*args, **kwargs)
        s += "\n"
        return s


class PhysicalDimensionalConstant(UserDict):
    def __init__(self, symbol, name, value, unit):
        self.symbol = symbol
        self.name = name
        self.value = value
        self.unit = unit
        super(PhysicalDimensionalConstant, self).__init__({unit: value})

    def __repr__(self, *args, **kwargs):
        s = ""
        s += "Physical constant - {0:s} ({1:s}) : ".format(self.name, self.symbol)
        s += super(PhysicalDimensionalConstant, self).__repr__(*args, **kwargs)
        s += "\n"
        return s


class PhysicalNonDimensionalConstant(float):
    def __init__(self, symbol, name, value):
        self.symbol = symbol
        self.name = name
        self.value = value
        float.__init__(value)

    def __new__(cls, symbol, name, value):
        return float.__new__(cls, value)

    def __repr__(self, *args, **kwargs):
        s = ""
        s += "{0:s} ({1:s}) : ".format(self.name, self.symbol)
    #     s += str(self)
        s += "\n"
        return s

    @staticmethod
    def keys():
        return ["-"]

    def __getitem__(self, key):
        if key in ["", "-", "none", "None", None]:
            return self
        else:
            raise TypeError("Constant {0:s} has no units".format(self.symbol))


class ConstDict(UserDict):

    def find_unit_constants(self, sub=None, disp=False, quantity=None):
        """
        Return list of unit constants keys containing a given string

        Parameters
        ----------
        sub : str, optional
           Sub-string to search keys for. By default, return all keys.
        disp : bool, optional
           If True, print the keys that are found and return None, Otherwise,
           return the list of keys without printing anything.
        quantity : str, optional
           Specific quantity ["length","mass","volume","pressure",etc.]

        Returns
        ------
        keys: list or None
           If disp is False, the list of keys is returned. Otherwise, None is returned.
        """
        if sub is None:
            sub = ""

        # Get Keys
        keys = []
        for k, v in self.items():
            if sub in k and isinstance(v, UnitConstant):
                if not quantity or v.quantity == quantity:
                    keys += [k]
        keys.sort()

        # Return keys
        if disp:
            print(keys)
            keys = None
        return keys

    def find_physical_constants(self, sub=None, disp=False):
        """
        Return list of unit constants keys containing a given string

        Parameters
        ----------
        sub : str, optional
           Sub-string to search keys for. By default, return all keys.
        disp : bool, optional
           If True, print the keys that are found and return None, Otherwise,
           return the list of keys without printing anything.

        Returns
        ------
        keys: list or None
           If disp is False, the list of keys is returned. Otherwise, None is returned.
        """
        if sub is None:
            sub = ""

        # Get Keys
        keys = []
        for k, v in self.items():
            if sub in k and \
                    (isinstance(v, PhysicalDimensionalConstant) or isinstance(v, PhysicalNonDimensionalConstant)):
                keys += [k]
        keys.sort()

        # Return keys
        if disp:
            print(keys)
            keys = None
        return keys


# --------------------------------------------------------------------------- #
#                                                                             #
# International System Prefix                                                 #
# ref: https://en.wikipedia.org/wiki/Metric_prefix                            #
#                                                                             #
# --------------------------------------------------------------------------- #

si_prefixes = {
    "y": [10 ** -24, "yocto"],
    "z": [10 ** -21, "zepto"],
    "a": [10 ** -18, "atto"],
    "f": [10 ** -15, "femto"],
    "p": [10 ** -12, "pico"],
    "n": [10 ** -9, "nano"],
    "mu": [10 ** -6, "micro"],
    "m": [10 ** -3, "milli"],
    "c": [10 ** -2, "centi"],
    "d": [10 ** -1, "deci"],
    "": [10 ** 0, ""],
    "da": [10 ** 1, "deca"],
    "h": [10 ** 2, "hecto"],
    "k": [10 ** 3, "kilo"],
    "M": [10 ** 6, "mega"],
    "G": [10 ** 9, "giga"],
    "T": [10 ** 12, "tera"],
    "P": [10 ** 15, "peta"],
    "E": [10 ** 18, "exa"],
    "Z": [10 ** 21, "zetta"],
    "Y": [10 ** 24, "yotta"],
}

# -----------------------------------------------------------------------------#
#                                                                              #
# Official Symbol/Names                                                        #
#                                                                              #
# -----------------------------------------------------------------------------#


# Units with prefixes
units_with_prefixes = {
    "m": "metre",
    "m2": "metre square",
    "m3": "metre cube",
    "g": "gram",
    "g/s": "gram per second",
    "s": "second",
    "W": "watt",
    "J": "joule",
    "N": "newton",
    "Hz": "hertz",
    "m/s": "metre per second",
    "Pa": "pascal",
    "K": "kelvin"
}
for k in list(units_with_prefixes.keys()):
    for p in si_prefixes.keys():
        units_with_prefixes[p + k] = si_prefixes[p][1] + units_with_prefixes[k]

# Other units
unit_without_prefixes = {
    "ft": "feet",
    "in": "inch",
    "mi": "mile",
    "NM": "nautical mile",
    "lb": "pound",
    "slug": "slug",
    "min": "minute",
    "h": "hour",
    "d": "day",
    "week": "week",  # Not symbol in SI system
    "month": "month",  # Not symbol in SI system
    "a": "year",
    "kt": "knot",
    "rad": "radian",
    "rad/s": "radian per second",
    "deg": "degree",
    "hp": "horsepower",
}

all_units = dict(units_with_prefixes, **unit_without_prefixes)

shortcuts = {
    "1/min": "rpm",
    "lb/in2": "psi",
    "lb/ft2": "psf",
    "ft/min": "fpm",
}

# -----------------------------------------------------------------------------#
#                                                                              #
# Base Units                                                                   #
# ref : https://en.wikipedia.org/wiki/SI_base_unit                             #
#                                                                              #
# -----------------------------------------------------------------------------#

const = ConstDict({})

# Length
s = "m"
const[s] = UnitConstant(s, all_units[s], "length", {})
const[s]["in"] = 1. / sp_constants.inch
const[s]["ft"] = 1. / sp_constants.foot
const[s]["mi"] = 1. / sp_constants.mile
const[s]["NM"] = 1. / sp_constants.nautical_mile
const[s].add_metric_prefixes(["m", "c", "", "k"])

# Mass
s = "kg"
const[s] = UnitConstant(s, all_units[s], "mass", {})
const[s]["lb"] = 1. / sp_constants.pound
const[s]["slug"] = 1. / sp_constants.pound / (sp_constants.g * const["m"]["ft"])
const[s].add_metric_prefixes(["m", "", "k"])

# Time
s = "s"
const[s] = UnitConstant(s, all_units[s], "time", {})
const[s]["min"] = 1 / sp_constants.minute
const[s]["h"] = 1 / sp_constants.hour
const[s]["d"] = 1 / sp_constants.day
const[s]["week"] = 1 / int(7*24*3600)
const[s]["month"] = 1 / int(365/12*24*3600)
const[s]["a"] = 1 / sp_constants.year
const[s].add_metric_prefixes(["", "m", "mu", "n"])

# -----------------------------------------------------------------------------#
#                                                                              #
# Derived Units                                                                #
# ref : https://en.wikipedia.org/wiki/SI_derived_unit                          #
#                                                                              #
# -----------------------------------------------------------------------------#

# Area
s = "m2"
const[s] = UnitConstant(s, all_units[s], "area", {})
const[s]["in2"] = const[s[:-1]]["in"] ** 2
const[s]["ft2"] = const[s[:-1]]["ft"] ** 2
const[s]["mi2"] = const[s[:-1]]["mi"] ** 2
const[s].add_metric_prefixes(["m", "c", "", "k"], order=2)

# Volume
s = "m3"
const[s] = UnitConstant(s, all_units[s], "volume", {})
const[s]["in3"] = const[s[:-1]]["in"] ** 3
const[s]["ft3"] = const[s[:-1]]["ft"] ** 3
const[s]["mi3"] = const[s[:-1]]["mi"] ** 3
const[s].add_metric_prefixes(["m", "c", "", "k"], order=3)

# Velocity
s = "m/s"
const[s] = UnitConstant(s, all_units[s], "velocity", {})
const[s]["ft/s"] = const["m"]["ft"]
const[s]["km/h"] = const["m"]["km"] / const["s"]["h"]
const[s]["ft/min"] = const["m"]["ft"] / const["s"]["min"]
const[s]["kt"] = const["m"]["NM"] / const["s"]["h"]

# Angle
s = "rad"
const[s] = UnitConstant(s, all_units[s], "angle", {})
const[s]["deg"] = 1. / sp_constants.degree

# Angular velocity
s = "rad/s"
const[s] = UnitConstant(s, all_units[s], "angular velocity", {})
const[s]["deg/s"] = 1 * const["rad"]["deg"]

# Mass flow rate
s = "kg/s"
const[s] = UnitConstant(s, all_units[s], "mass flow rate", {})
const[s]["kg/h"] = 1 / const["s"]["h"]
const[s]["lb/s"] = const["kg"]["lb"]
const[s]["lb/h"] = const["kg"]["lb"] / const["s"]["h"]


# Frequency
s = "Hz"
const[s] = UnitConstant(s, all_units[s], "frequency", {})
const[s]["1/s"] = 1.
const[s]["1/min"] = 1 / const["s"]["min"]
const[s]["rad/s"] = 2 * np.pi
const[s].add_metric_prefixes(["", "k", "M", ])

# Force
s = "N"
const[s] = UnitConstant(s, all_units[s], "force", {})
const[s]["kg*m/s2"] = 1.
const[s]["lb"] = const["kg"]["lb"] / sp_constants.g
const[s].add_metric_prefixes(["", "k"])

# Pressure
s = "Pa"
const[s] = UnitConstant(s, all_units[s], "pressure", {})
const[s]["N/m2"] = 1.
const[s]["kg/m/s2"] = 1.
const[s]["lb/in2"] = const["kg"]["lb"] / const["m2"]["in2"] / sp_constants.g
const[s]["lb/ft2"] = const["kg"]["lb"] / const["m2"]["ft2"] / sp_constants.g
const[s]["bar"] = 1. / sp_constants.bar
const[s]["mbar"] = 1. / sp_constants.bar * 1000.
const[s]["kPa"] = 1. / 1e3
const[s]["MPa"] = 1. / 1e6

# Torque
s = "N*m"
const[s] = UnitConstant(s, "N*m", "torque", {})
const[s]["J"] = 1.0
const[s]["m2*kg/s2"] = 1.0
const[s]["lb*in"] = const["kg"]["slug"] * const["m"]["ft"] * const["m"]["in"]
const[s]["lb*ft"] = const["kg"]["slug"] * const["m"]["ft"] * const["m"]["ft"]

# Power
s = "W"
const[s] = UnitConstant(s, all_units[s], "power", {})
const[s]["kg*m2/s3"] = 1.
const[s]["J/s"] = 1.
const[s]["hp"] = 1. / sp_constants.hp
const[s]["ft*lb/s"] = const[s]["hp"] * 550
const[s]["ft*lb/min"] = const[s]["ft*lb/s"] * sp_constants.minute
const[s].add_metric_prefixes(["", "k", "M"])

# Density
s = "g/m3"
const[s] = UnitConstant(s, "g/m3", "density", {})
const[s]["slug/ft3"] = const["kg"]["slug"] / const["m3"]["ft3"]
const[s]["kg/m3"] = 1. / 1000.

# -----------------------------------------------------------------------------#
#                                                                              #
# Create shortcuts                                                             #
#                                                                              #
# -----------------------------------------------------------------------------#

for k0 in list(const.keys()):
    for k1 in list(const[k0].keys()):
        if k1 in shortcuts:
            const[k0][shortcuts[k1]] = const[k0][k1]

# -----------------------------------------------------------------------------#
#                                                                              #
# Create all permutations                                                      #
#                                                                              #
# -----------------------------------------------------------------------------#

# Permutations of output units
for k0 in list(const.keys()):
    k1s = list(const[k0].keys())
    for k1 in k1s:
        for k2 in k1s:
            if k1 not in const.keys():
                name = all_units.get(k1, k1)
                const[k1] = UnitConstant(k1, name, const[k0].quantity, {})
            if k2 not in const[k1].keys():
                const[k1][k2] = const[k0][k2] / const[k0][k1]
                pass

# Inverse relationships
for k0 in list(const.keys()):
    for k1 in list(const[k0].keys()):
        if k1 not in const.keys():
            name = all_units.get(k1, k1)
            const[k1] = UnitConstant(k1, name, const[k0].quantity, {})
        if k0 not in const[k1].keys():
            const[k1][k0] = 1. / const[k0][k1]

# -----------------------------------------------------------------------------#
#                                                                              #
# Constants                                                                    #
#                                                                              #
# -----------------------------------------------------------------------------#

DC = PhysicalDimensionalConstant
NDC = PhysicalNonDimensionalConstant

# Temperature
const["zero_degc"] = DC("zero_degc", "Zero degree celcius",
                        sp_constants.zero_Celsius, "K")

# Gravitational acceleration
# ref.: https://en.wikipedia.org/wiki/Gravitational_acceleration
const["g_acc"] = DC("g", "Gravitational acceleration",
                    sp_constants.g, "m/s2")

# Earth radius
# ref.: https://en.wikipedia.org/wiki/Earth_radius
const["earth_radius"] = DC("earth_radius", "Earth radius",
                           6371000, "m")

# Gas Constant
# ref.: https://en.wikipedia.org/wiki/Gas_constant
const["R"] = DC("R", "Gas constant for air",
                sp_constants.R, "kg*m2/mol/K/s2")
const["R_air"] = DC("R_air", "Specific gas constant for air",
                    287.058, "m2/s2/K")

# Ideal Gas Model
# ref.: https://en.wikipedia.org/wiki/Ideal_gas
const["gamma_air"] = NDC("gamma_air", "Ratio of specific heats (cp/cv) for air", 1.4)

# ISA Atmospheric Model
# ref.: https://en.wikipedia.org/wiki/International_Standard_Atmosphere

const["isa_T0"] = DC("isa_T0", "ISA temperature at sea level", 288.15, "K")

const["isa_p0"] = DC("isa_p0", "ISA pressure at sea level", 101325, "Pa")

const["isa_rho0"] = DC("isa_rho0", "ISA density at sea level", 1.2250, "kg/m3")

const["isa_c0"] = DC("isa_c0", "ISA speed of sound at sea level",
                     np.sqrt(const["gamma_air"] * const["isa_p0"]["Pa"] / const["isa_rho0"]["kg/m3"]), "m/s")

const["isa_lapse_rate"] = DC("isa_lapse_rate", "ISA lapse rate", -6.5e-3, "degc/m")

const["isa_alt_tropo"] = DC("isa_alt_tropo", "ISA altitude AT tropopause", 11000, "m")

const["isa_T_tropo"] = DC("isa_T_tropo", "ISA temperature at tropopause",
                          const["isa_T0"]["K"] + const["isa_lapse_rate"]["degc/m"] * const["isa_alt_tropo"]["m"], "K")

const["isa_Tc_tropo"] = DC("isa_Tc_tropo", "ISA temperature constant at tropopause",
                           const["g_acc"]["m/s2"] / (const["R_air"]["m2/s2/K"] * const["isa_T_tropo"]["K"]), "1/m")

const["isa_pc_tropo"] = NDC("isa_pc_tropo", "ISA pressure constant at tropopause",
                            -const["g_acc"]["m/s2"] / (const["R_air"]["m2/s2/K"] * const["isa_lapse_rate"]["degc/m"]))

const["isa_p_tropo"] = DC("isa_p_tropo", "ISA pressure at tropopause",
                          const["isa_p0"]["Pa"] * (const["isa_T_tropo"]["K"] / const["isa_T0"]["K"]) ** const[
                              "isa_pc_tropo"], "Pa")

# -----------------------------------------------------------------------------#
# Convert constants to other units                                             #
# -----------------------------------------------------------------------------#

const["zero_degc"]["degc"] = 0.0

const["g_acc"]["ft/s2"] = const["g_acc"]["m/s2"] * const["m"]["ft"]

const["earth_radius"]["ft"] = const["earth_radius"]["m"] * const["m"]["ft"]
const["earth_radius"]["km"] = const["earth_radius"]["m"] * const["m"]["km"]

const["R_air"]["ft2/s2/K"] = const["R_air"]["m2/s2/K"] * const["m2"]["ft2"]

const["isa_rho0"]["slug/ft3"] = const["isa_rho0"]["kg/m3"] * const["kg"]["slug"] / const["m3"]["ft3"]

const["isa_p0"]["lb/ft2"] = const["isa_p0"]["Pa"] * const["Pa"]["lb/ft2"]

const["isa_c0"]["ft/s"] = const["isa_c0"]["m/s"] * const["m/s"]["ft/s"]

const["isa_lapse_rate"]["degc/ft"] = const["isa_lapse_rate"]["degc/m"] / const["m"]["ft"]

const["isa_alt_tropo"]["ft"] = const["isa_alt_tropo"]["m"] * const["m"]["ft"]

const["isa_Tc_tropo"]["1/ft"] = const["isa_Tc_tropo"]["1/m"] / const["m"]["ft"]

const["isa_p_tropo"]["lb/ft2"] = const["isa_p_tropo"]["Pa"] * const["Pa"]["lb/ft2"]

# -----------------------------------------------------------------------------#
# Create shortcuts                                                             #
# -----------------------------------------------------------------------------#

for k0 in list(const.keys()):
    for k1 in list(const[k0].keys()):
        if k1 in shortcuts:
            const[k0][shortcuts[k1]] = const[k0][k1]


# -----------------------------------------------------------------------------#
# Functions                                                                    #
# -----------------------------------------------------------------------------#

def convert_temperature(val, old_scale, new_scale):
    """
    Convert from a temperature scale to another one among Celsius, Kelvin, Fahrenheit and Rankine scales.

    Parameters
    ----------
        val : array_like
            Value(s) of the temperature(s) to be converted expressed in the original scale.
        old_scale: str
            Specifies as a string the original scale from which the temperature value(s) will be converted. Supported scales are Celsius (‘Celsius’, ‘celsius’, ‘C’ or ‘c’), Kelvin (‘Kelvin’, ‘kelvin’, ‘K’, ‘k’), Fahrenheit (‘Fahrenheit’, ‘fahrenheit’, ‘F’ or ‘f’) and Rankine (‘Rankine’, ‘rankine’, ‘R’, ‘r’).
        new_scale: str
            Specifies as a string the new scale to which the temperature value(s) will be converted. Supported scales are Celsius (‘Celsius’, ‘celsius’, ‘C’ or ‘c’), Kelvin (‘Kelvin’, ‘kelvin’, ‘K’, ‘k’), Fahrenheit (‘Fahrenheit’, ‘fahrenheit’, ‘F’ or ‘f’) and Rankine (‘Rankine’, ‘rankine’, ‘R’, ‘r’).

    Returns
    -------
        output : float or array of floats
            Value(s) of the converted temperature(s) expressed in the new scale.
    """
    if old_scale == "degc":
        old_scale = "c"
    if new_scale == "degc":
        new_scale = "c"
    return sp_constants.convert_temperature(val, old_scale, new_scale)


# -----------------------------------------------------------------------------#
# List of valid units                                                          #
# -----------------------------------------------------------------------------#

valid_units = list(const.keys())
valid_units += [None]
valid_units += ["dot"]
valid_units += ["%"]
valid_units += ["degc", "K"]
