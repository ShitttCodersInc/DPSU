""" Возмущения вызванные гравитационным возмействием Солнца
"""

import numpy as np
from constants import *
from math import radians, sin, cos
from typing import List


def sun_acceleration(r_j2000: List[float], t: float) -> List[float]:
    if len(r_j2000) != 3:
        raise Exception("r_j2000 len must be uqual 3")

    rs = radius_earth_sun(t=t)
    rs = np.array(rs)
    rs_mod = np.linalg.norm(rs)
    _r_j2000 = np.array(r_j2000)
    dr = rs - _r_j2000
    dr_mod = np.linalg.norm(dr)
    a_sun = SUN_GRAVITATIONAL_PARAMETER * (dr / dr_mod ** 3 - rs / rs_mod ** 3)

    return list(a_sun)


def radius_earth_sun(t: float) -> List[float]:
    epsilon = radians(23.43929111)
    OMEGA_plus_omega = radians(282.940)
    JD = JD0 + JDD * t
    T = (JD - 2451545.0) / 36525.0
    M = radians(357.5226 + 35999.049 * T)
    _lambda = OMEGA_plus_omega + M + radians(6892 / 3600.0) * sin(M) + radians(72 / 3600.0) * sin(2 * M)
    _r = (149.619 - 2.499 * cos(M) - 0.021 * cos(2 * M)) * 1e6

    r_sun = _r * np.array([cos(_lambda),
                           sin(_lambda) * cos(epsilon),
                           sin(_lambda) * sin(epsilon)
                           ])

    return list(r_sun)
