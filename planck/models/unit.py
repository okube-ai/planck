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
            Unit symbol (e.g. "m")
        quantity:
            Unit quantity (e.g. "length")
        name:
            Unit name (e.g. "meter")
        si_prefixes:
            List of supported international system prefixes (e.g. "k", "micro")
        order:
            Order of the quantity
        values:
            Values expressed in other units
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
