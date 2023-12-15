from typing import Union
from typing import List

from planck._scipy import sp_constants


__all__ = [
    "convert_temperature",
]


def convert_temperature(
    value: Union[float, List[float]],
    source: str,
    target: str,
):
    """
    Convert from a temperature scale to another one among Celsius, Kelvin, Fahrenheit and Rankine scales.

    Parameters
    ----------
        value:
            Value(s) of the temperature(s) to be converted expressed in the original scale.
        source:
            Specifies as a string the original scale from which the temperature value(s) will be converted.
            Supported scales are Celsius (‘Celsius’, ‘celsius’, ‘C’ or ‘c’), Kelvin (‘Kelvin’, ‘kelvin’, ‘K’, ‘k’),
            Fahrenheit (‘Fahrenheit’, ‘fahrenheit’, ‘F’ or ‘f’) and Rankine (‘Rankine’, ‘rankine’, ‘R’, ‘r’).
        target:
            Specifies as a string the new scale to which the temperature value(s) will be converted. Supported scales
            are Celsius (‘Celsius’, ‘celsius’, ‘C’ or ‘c’), Kelvin (‘Kelvin’, ‘kelvin’, ‘K’, ‘k’), Fahrenheit
            (‘Fahrenheit’, ‘fahrenheit’, ‘F’ or ‘f’) and Rankine (‘Rankine’, ‘rankine’, ‘R’, ‘r’).

    Returns
    -------
        output : float or array of floats
            Value(s) of the converted temperature(s) expressed in the new scale.
    """
    if source == "degc":
        source = "c"
    if target == "degc":
        target = "c"
    return sp_constants.convert_temperature(value, source, target)
