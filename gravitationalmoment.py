""" Внешний возмущающий гравитационный момент
Методы для расчёта момента
"""
import quaternion as qtrn
from data import *
from constants import *
import numpy as np
from typing import List


def gravity_moment(R: float, quaternion: List[float], r_j2000: List[float]) -> List[float]:
    if len(quaternion) != 4:
        raise qtrn.QuaternionSizeError(qtrn.QUATERNION_SIZE_ERROR_MSG)
    if len(r_j2000) != 3:
        raise Exception("r_j2000 len must be uqual 3")

    unit_vector = unit_vector_SSK(quaternion=quaternion, r_j2000=r_j2000)

    product_J_on_unit_vect = np.array([
        Jx * unit_vector[0],
        Jy * unit_vector[1],
        Jz * unit_vector[2],
    ])

    moment = np.cross(np.array(unit_vector), product_J_on_unit_vect)
    moment *= (3 * EARTH_GRAVITATIONAL_PARAMETER) / (2 * (R ** 3))

    return list(moment)


def unit_vector_SSK(quaternion: List[float], r_j2000: List[float]) -> List[float]:
    if len(quaternion) != 4:
        raise qtrn.QuaternionSizeError(qtrn.QUATERNION_SIZE_ERROR_MSG)
    if len(r_j2000) != 3:
        raise Exception('r_j2000 len must be equal 3')

    normalized_r_j2000 = list(np.array(r_j2000) / np.linalg.norm(r_j2000))

    conf_quaternion = qtrn.confugate(quaternion=quaternion)
    result = qtrn.multiply_quaternions(quat1=conf_quaternion, quat2=[.0] + normalized_r_j2000)
    result = qtrn.multiply_quaternions(quat1=result, quat2=quaternion)

    return result[1:]
