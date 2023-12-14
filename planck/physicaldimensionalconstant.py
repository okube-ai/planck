
# --------------------------------------------------------------------------- #
# Main Class                                                                  #
# --------------------------------------------------------------------------- #

class PhysicalDimensionalConstant(dict):
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
