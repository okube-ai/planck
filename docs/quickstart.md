## Units

Explore a given unit
```py
from planck import units

print(units["m"])
"""
metre [m] - unit of length:
{'in': 39.37007874015748, 'ft': 3.280839895013124, 'mi': 0.000621371192237334, 'NM': 0.0005399568034557236, 'mm': 1000.0, 'cm': 100.0, 'm': 1.0, 'km': 0.001}
"""
```

Convert a length from meters to feet.

```py
from planck import units

print(1 * units["m"]["ft"])
#> 3.280839895013124

print(units.convert(1, "m", "ft"))
#> 3.280839895013124

print(units.convert(0, "degc", "K"))
#> 273.15
```

Find all units related to area:
```py
from planck import units

print(units.find(quantity="area"))
"""
[
    'cm2',
    'cm3',
    'ft2',
    'ft3',
    'in2',
    'in3',
    'km2',
    'km3',
    'm2',
    'm3',
    'mi2',
    'mi3',
    'mm2',
    'mm3',
]
"""
```

## Constants


Explore a given constant
```py
from planck import constants

print(constants["g_acc"])
"""
Gravitational acceleration [g_acc]:
{'m/s2': 9.80665, 'ft/s2': 32.17404855643045}
"""
```

Some other constants are non-dimensional and are represented as a float only
```py
from planck import constants

print(constants["gamma_air"])
"""
Ratio of specific heats (cp/cv) for air [gamma_air]:
1.4
"""
```
