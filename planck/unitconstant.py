import re

from planck._common import si_prefixes


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
# Main Class                                                                  #
# --------------------------------------------------------------------------- #

class UnitConstant(dict):
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
