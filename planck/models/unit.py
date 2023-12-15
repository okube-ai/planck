import re
from typing import Dict

from planck._common import si_prefixes
from planck._common import all_units


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
# Main Class                                                                  #
# --------------------------------------------------------------------------- #


class Unit(dict):
    def __init__(
        self,
        symbol: str,
        quantity: str,
        name: str = None,
        si_prefixes: list = None,
        order: int = 1,
        values: Dict[str, float] = None,
    ):
        """
        Unit model

        Parameters
        ----------
        symbol:
            Unit symbol
        quantity:
            Unit quantity
        name:
            Unit name
        si_prefixes:
            List of supported international system prefixes
        order:
            Order of the quantity
        values:
            Values expressed in other units

        Examples
        --------
        ```py
        from planck import models
        from planck import sp_constants

        unit = models.Unit(
            symbol="m",
            quantity="length",
            values={
                "in": 1.0 / sp_constants.inch,
                "ft": 1.0 / sp_constants.foot,
                "mi": 1.0 / sp_constants.mile,
                "NM": 1.0 / sp_constants.nautical_mile,
            },
            si_prefixes=["m", "c", "", "k"],
        )
        print(unit)
        '''
        metre [m] - unit of length:
        {'in': 39.37007874015748, 'ft': 3.280839895013124, 'mi': 0.000621371192237334, 'NM': 0.0005399568034557236, 'mm': 1000.0, 'cm': 100.0, 'm': 1.0, 'km': 0.001}
        '''
        ```
        """
        # Default mutable values
        if values is None:
            values = {}
        if si_prefixes is None:
            si_prefixes = []
        if name is None:
            name = all_units.get(symbol)

        super().__init__(values)

        self.symbol = symbol
        self.quantity = quantity
        self.name = name
        self.si_prefixes = si_prefixes
        self.order = order

        self.add_si_prefixes()

    def add_si_prefixes(self) -> None:
        for p in self.si_prefixes:
            p0, k = _split_symbol(self.symbol)
            self[p + k] = (si_prefixes[p0][0] / si_prefixes[p][0]) ** self.order

    def __repr__(self, *args, **kwargs):
        s = ""
        s += f"{self.name} [{self.symbol}] - unit of {self.quantity}:\n"
        s += super().__repr__(*args, **kwargs)
        return s
