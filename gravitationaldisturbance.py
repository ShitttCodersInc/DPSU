""" Возмущения вызванные несферичностью гравитационного поля Земли
Учитывается только вторая зональная гармоника
"""

from gravitationalmoment import *
from math import sin, cos, fmod, pi
from constants import *
from typing import List


def gravitational_acceleration(r_j2000: List[float], t: float) -> List[float]:
    M = transition_matrix_j2000_to_greenwich(t=t)
    a_j2 = acceleration_greenwich(r_j2000=r_j2000, t=t)
    return list(np.dot(M.transpose(), a_j2).reshape(1, 3))


def acceleration_greenwich(r_j2000: List[float], t: float) -> List[float]:
    if len(r_j2000) != 3:
        raise Exception("r_j2000 len must be equal 3")

    x, y, z = set(r_j2000)
    M = transition_matrix_j2000_to_greenwich(t=t)
    r_j2000 = np.array(r_j2000).reshape(3, 1)
    r = np.dot(M, r_j2000).reshape(1, 3)
    r_mod = np.linalg.norm(r)

    acceleration_j2 = np.array([
        (1 - 5 * (z / r_mod) ** 2) * (x / r_mod),
        (1 - 5 * (z / r_mod) ** 2) * (y / r_mod),
        (3 - 5 * (z / r_mod) ** 2) * (z / r_mod),
    ])

    acceleration_j2 *= EARTH_RADIUS / r_mod
    acceleration_j2 *= EARTH_GRAVITATIONAL_PARAMETER / (r_mod ** 2)
    acceleration_j2 *= -1.5 * J2
    return list(acceleration_j2)


def transition_matrix_j2000_to_greenwich(t: float) -> np.ndarray:
    JD = JD0 + JDD * t
    f = 86400 * fmod(JD, 1.0)
    a = DS2R * ((A + (B + (C + D * t) * t) * t) + f)
    a = fmod(a, 2 * pi)
    a += 2 * pi if a < 0 else 0

    matrix = [
        [cos(a), sin(a), 0],
        [-sin(a), cos(a), 0],
        [0, 0, 1],
    ]

    return np.array(matrix)
