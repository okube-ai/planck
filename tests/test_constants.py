import pytest
from planck import constants
# from planck.constants import convert_temperature


def test_constants():
    assert constants["m"]["mm"] == 1000

    for k in ["m", "g_acc", "gamma_air"]:
        assert constants[k].name in constants[k].__repr__()


def test_find_constants():
    assert "kg" in constants.find_unit_constants("kg")
    assert "kg/m3" in constants.find_unit_constants("kg")

    assert "g_acc" in constants.find_physical_constants("g")
    assert "gamma_air" in constants.find_physical_constants("g")


# def test_convert_temperature():
#     assert convert_temperature(0, "degc", "K") == 273.15
#     assert convert_temperature(0, "c", "F") == 32.0


if __name__ == "__main__":
    test_constants()
    test_find_constants()
    # test_convert_temperature()
