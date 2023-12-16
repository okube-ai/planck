# --------------------------------------------------------------------------- #
#                                                                             #
# International System Prefix                                                 #
# ref: https://en.wikipedia.org/wiki/Metric_prefix                            #
#                                                                             #
# --------------------------------------------------------------------------- #

si_prefixes = {
    "y": [10**-24, "yocto"],
    "z": [10**-21, "zepto"],
    "a": [10**-18, "atto"],
    "f": [10**-15, "femto"],
    "p": [10**-12, "pico"],
    "n": [10**-9, "nano"],
    "mu": [10**-6, "micro"],
    "m": [10**-3, "milli"],
    "c": [10**-2, "centi"],
    "d": [10**-1, "deci"],
    "": [10**0, ""],
    "da": [10**1, "deca"],
    "h": [10**2, "hecto"],
    "k": [10**3, "kilo"],
    "M": [10**6, "mega"],
    "G": [10**9, "giga"],
    "T": [10**12, "tera"],
    "P": [10**15, "peta"],
    "E": [10**18, "exa"],
    "Z": [10**21, "zetta"],
    "Y": [10**24, "yotta"],
}


# Units with prefixes
units_with_prefixes = {
    "m": "metre",
    "m2": "metre square",
    "m3": "metre cube",
    "g": "gram",
    "g/s": "gram per second",
    "s": "second",
    "W": "watt",
    "J": "joule",
    "N": "newton",
    "Hz": "hertz",
    "m/s": "metre per second",
    "Pa": "pascal",
    "K": "kelvin",
}
for k in list(units_with_prefixes.keys()):
    for p in si_prefixes.keys():
        units_with_prefixes[p + k] = si_prefixes[p][1] + units_with_prefixes[k]

# Other units
unit_without_prefixes = {
    "ft": "feet",
    "in": "inch",
    "mi": "mile",
    "NM": "nautical mile",
    "lb": "pound",
    "slug": "slug",
    "min": "minute",
    "h": "hour",
    "d": "day",
    "week": "week",  # No symbol in SI system
    "month": "month",  # No symbol in SI system
    "a": "year",
    "kt": "knot",
    "rad": "radian",
    "rad/s": "radian per second",
    "deg": "degree",
    "hp": "horsepower",
}

all_units = dict(units_with_prefixes, **unit_without_prefixes)

shortcuts = {
    "1/min": "rpm",
    "lb/in2": "psi",
    "lb/ft2": "psf",
    "ft/min": "fpm",
}
