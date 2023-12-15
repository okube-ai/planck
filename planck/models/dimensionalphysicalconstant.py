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
        """
        Dimensional physical constant

        Parameters
        ----------
        symbol:
            Constant symbol
        name:
            Constant name
        values:
            Constant values expressed in different units

        Examples
        --------
        ```py
        from planck import models
        from planck import units
        from planck import sp_constants

        const = models.DimensionalPhysicalConstant(
            symbol="g_acc",
            name="Gravitational acceleration",
            values={
                "m/s2": sp_constants.g,
                "ft/s2": sp_constants.g * units["m"]["ft"],
            },
        )
        print(const)
        '''
        Gravitational acceleration [g_acc]:
        {'m/s2': 9.80665, 'ft/s2': 32.17404855643045}
        '''
        ```
        """
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
