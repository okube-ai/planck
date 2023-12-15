import pytest
import numpy as np

from planck import units


def test_units():
    m = units["m"]
    assert m.symbol == "m"
    assert m.name == "metre"
    assert m.quantity == "length"
    assert m["mm"] == 1000


def test_permutations():
    for k0 in units:
        for k1 in units[k0]:
            assert units[k0][k1] == pytest.approx(1.0 / units[k1][k0], rel=0.0001)


def test_find():
    assert units.find("Pa") == ["MPa", "Pa", "kPa"]
    assert units.find(quantity="velocity") == [
        "fpm",
        "ft/min",
        "ft/s",
        "km/h",
        "kt",
        "m/s",
    ]


def test_convert():
    assert units.convert(1, "m/s", "kt") == pytest.approx(1.94384, rel=0.001)
    assert units.convert(0, "degc", "K") == 273.15
    assert units.convert(0, "degc", "Fahrenheit") == 32
    assert units.convert(np.array([0, 1]), "m", "mm").tolist() == [0, 1000]


if __name__ == "__main__":
    test_units()
    test_permutations()
    test_find()
    test_convert()
