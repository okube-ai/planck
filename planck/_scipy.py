import math
import numpy as np

DEFAULT_PERIOD = "1d"


# --------------------------------------------------------------------------- #
# Main Class - scipy.constants mock                                           #
# --------------------------------------------------------------------------- #


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
        """
        # Convert from `old_scale` to Kelvin
        if old_scale.lower() in ["celsius", "c"]:
            tempo = np.asanyarray(val) + self.zero_Celsius
        elif old_scale.lower() in ["kelvin", "k"]:
            tempo = np.asanyarray(val)
        elif old_scale.lower() in ["fahrenheit", "f"]:
            tempo = (np.asanyarray(val) - 32) * 5 / 9 + self.zero_Celsius
        elif old_scale.lower() in ["rankine", "r"]:
            tempo = np.asanyarray(val) * 5 / 9
        else:
            raise NotImplementedError(
                "%s scale is unsupported: supported scales "
                "are Celsius, Kelvin, Fahrenheit, and "
                "Rankine" % old_scale
            )
        # and from Kelvin to `new_scale`.
        if new_scale.lower() in ["celsius", "c"]:
            res = tempo - self.zero_Celsius
        elif new_scale.lower() in ["kelvin", "k"]:
            res = tempo
        elif new_scale.lower() in ["fahrenheit", "f"]:
            res = (tempo - self.zero_Celsius) * 9 / 5 + 32
        elif new_scale.lower() in ["rankine", "r"]:
            res = tempo * 9 / 5
        else:
            raise NotImplementedError(
                "'%s' scale is unsupported: supported "
                "scales are 'Celsius', 'Kelvin', "
                "'Fahrenheit', and 'Rankine'" % new_scale
            )

        return res


sp_constants = ScipyConstants()
