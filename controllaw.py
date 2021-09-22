""" Закон управления ДМ

"""

import quaternion as qtrn
from data import *
from math import copysign, fabs
from typing import List
import numpy as np


def is_OMEGA_correct(OMEGA: List[float]) -> bool:
    if len(OMEGA) != 3:
        raise Exception("OMEGA len must be equal 3")

    for el in OMEGA:
        if fabs(el) >= OMEGA_MAX:
            return False

    return True


def correct_by_OMEGA_limitation(OMEGA: List[float], signal: List[float]) -> List[float]:
    if len(OMEGA) != 3 or len(signal) != 3:
        raise Exception("params len must be equal 3")

    result = [signal[i] if fabs(OMEGA[i]) < OMEGA_MAX else 0 for i in range(len(signal))]
    return result


def correct_by_limitation(Signal: List[float], limit_value: float = L_MAX) -> List[float]:
    if len(Signal) != 3:
        raise Exception("Signal len must be equal 3")

    _signal = [limit_value * copysign(1, Signal[i])
               if fabs(Signal[i]) >= limit_value
               else Signal[i]
               for i in range(len(Signal))]

    return _signal


def signal(quaternion: List[float], angular_velocity: List[float], Kp: float = 0.3, Ka: float = 0.7) -> List[float]:
    if len(quaternion) != 4:
        raise qtrn.QuaternionSizeError(qtrn.QUATERNION_SIZE_ERROR_MSG)
    if len(angular_velocity) != 3:
        raise Exception("angular_velocity len must be equal 3")

    L = -Kp * copysign(1, quaternion[0]) * np.array(quaternion[1:]) - Ka * np.array(angular_velocity)
    L = correct_by_limitation(Signal=L)
    return list(L)
