from planck import constants


def test_constants():
    g = constants["g_acc"]
    assert g.name == "Gravitational acceleration"
    assert g.symbol == "g_acc"
    assert g == {"m/s2": 9.80665, "ft/s2": 32.17404855643045}

    gamma = constants["gamma_air"]
    assert gamma.name == "Ratio of specific heats (cp/cv) for air"
    assert gamma.symbol == "gamma_air"
    assert gamma == 1.4

    planck = constants["planck"]
    assert planck.name.startswith("Planck constant")
    assert planck["J*Hz"] == 6.62607015e-34


def test_find():
    assert constants.find("isa") == [
        "isa_T0",
        "isa_T_tropo",
        "isa_Tc_tropo",
        "isa_alt_tropo",
        "isa_c0",
        "isa_lapse_rate",
        "isa_p0",
        "isa_p_tropo",
        "isa_pc_tropo",
        "isa_rho0",
    ]


if __name__ == "__main__":
    test_constants()
    test_find()
