from planck._scipy import sp_constants
from _common import si_prefixes
from _common import all_units
from unitconstant import _split_symbol
from unitconstant import UnitConstant
from collections import defaultdict

d = defaultdict(lambda: {})


def add_si_prefixes(d, key, prefixes, order=1):
    for p in prefixes:
        p0, k = _split_symbol(key)
        d[p + k] = (si_prefixes[p0][0] / si_prefixes[p][0]) ** order
    return d

# Length
s = "m"
d[s]["in"] = 1. / sp_constants.inch
d[s]["ft"] = 1. / sp_constants.foot
d[s]["mi"] = 1. / sp_constants.mile
d[s]["NM"] = 1. / sp_constants.nautical_mile
add_si_prefixes(d[s], key=s, prefixes=["m", "c", "", "k"])

# Mass
s = "kg"
d[s]["lb"] = 1. / sp_constants.pound
d[s]["slug"] = 1. / sp_constants.pound / (sp_constants.g * d["m"]["ft"])
add_si_prefixes(d[s], key=s, prefixes=["m", "", "k"])

# Time
s = "s"
d[s] = UnitConstant(s, all_units[s], "time", {})
d[s]["min"] = 1 / sp_constants.minute
d[s]["h"] = 1 / sp_constants.hour
d[s]["d"] = 1 / sp_constants.day
d[s]["week"] = 1 / int(7*24*3600)
d[s]["month"] = 1 / int(365/12*24*3600)
d[s]["a"] = 1 / sp_constants.year
add_si_prefixes(d, key=s, prefixes=["", "m", "mu", "n"])


# Volume
s = "m3"
d[s]["in3"] = d[s[:-1]]["in"] ** 3
d[s]["ft3"] = d[s[:-1]]["ft"] ** 3
d[s]["mi3"] = d[s[:-1]]["mi"] ** 3
add_si_prefixes(d[s], key=s, prefixes=["m", "c", "", "k"], order=3)


# -----------------------------------------------------------------------------#
# Create all permutations                                                      #
# -----------------------------------------------------------------------------#

# Permutations of output units
for k0 in list(d.keys()):
    k1s = list(d[k0].keys())
    for k1 in k1s:
        for k2 in k1s:
            if k2 not in d[k1].keys():
                d[k1][k2] = d[k0][k2] / d[k0][k1]

print(len(d))

# Inverse relationships
for k0 in list(d.keys()):
    for k1 in list(d[k0].keys()):
        if k0 not in d[k1].keys():
            print("got one!")
            d[k1][k0] = 1. / d[k0][k1]

print(len(d))


d = dict(d)

print(d["m"])
