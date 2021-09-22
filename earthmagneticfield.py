"""Упрощенная модель магнитного поля Земли
- вектор магнитной индукции Земли в Гринвической СК
- вектор магнитной индукции Земли в J2000 СК
"""

from typing import List
import numpy as np
from gravitationaldisturbance import transition_matrix_j2000_to_greenwich


def magnetic_induction_greenwich(r: List[float]) -> List[float]:
    if len(r) != 3:
        raise Exception("r len must be equal 3")

    a = 6371.2
    m = a * np.array([-1501.0, 4797.1, -29442.0])
    r_mod = np.linalg.norm(r)
    r_v = np.array(r)
    magnetic_induction = (3 * np.dot(m, r) * r_v - r_mod ** 2 * m) / r_mod ** 5
    return list(magnetic_induction)


def magnetic_induction_j2000(t: float, r: List[float]) -> List[float]:
    matrix = transition_matrix_j2000_to_greenwich(t=t).transpose()
    B = np.array(magnetic_induction_greenwich(r=r)).reshape(3, 1)
    return list(np.dot(matrix, B).reshape(1, 3))
