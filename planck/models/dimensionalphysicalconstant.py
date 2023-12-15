from typing import Dict


# --------------------------------------------------------------------------- #
# Main Class                                                                  #
# --------------------------------------------------------------------------- #


class DimensionalPhysicalConstant(dict):
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

    def __repr__(self, *args, **kwargs):
        s = ""
        s += f"{self.name} [{self.symbol}]:\n"
        s += super().__repr__(*args, **kwargs)
        return s
