from typing import Dict


# --------------------------------------------------------------------------- #
# Main Class                                                                  #
# --------------------------------------------------------------------------- #

class DimensionalConstant(dict):
    def __init__(
            self,
            symbol: str,
            name: str = None,
            values: Dict[str, float] = None,
    ):

        # Default mutable values
        if values is None:
            values = {}

        super().__init__(values)
        self.symbol = symbol
        self.name = name

    # def __repr__(self, *args, **kwargs):
    #     s = ""
    #     s += "Physical constant - {0:s} ({1:s}) : ".format(self.name, self.symbol)
    #     s += super(PhysicalDimensionalConstant, self).__repr__(*args, **kwargs)
    #     s += "\n"
    #     return s
