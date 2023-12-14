
# --------------------------------------------------------------------------- #
# Main Class                                                                  #
# --------------------------------------------------------------------------- #

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

