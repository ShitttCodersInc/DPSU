"""Методы для работы с кватернионом
- Перемножение кватернионов
- Нормировака кватерниона
- Условие необходимости нормировки кватерниона
- Модуль кватерниона
- Сопряженный кватернион
"""
from typing import List
import numpy as np
from math import atan2, asin

QUATERNION_SIZE_ERROR_MSG = 'Quaternion size must be equal 4'


class QuaternionSizeError(Exception):
    pass


def multiply_quaternions(quat1: List[float], quat2: List[float]) -> List[float]:
    if len(quat1) != 4 or len(quat2) != 4:
        raise QuaternionSizeError(QUATERNION_SIZE_ERROR_MSG)

    multiply_result = [
        quat1[0] * quat2[0] - quat1[1] * quat2[1] - quat1[2] * quat2[2] - quat1[3] * quat2[3],
        quat1[0] * quat2[1] + quat1[1] * quat2[0] + quat1[2] * quat2[3] - quat1[3] * quat2[2],
        quat1[0] * quat2[2] + quat1[2] * quat2[0] + quat1[3] * quat2[1] - quat1[1] * quat2[3],
        quat1[0] * quat2[3] + quat1[3] * quat2[0] + quat1[1] * quat2[2] - quat1[2] * quat2[1]
    ]

    return multiply_result


def normalize(quaternion: List[float]) -> List[float]:
    if len(quaternion) != 4:
        raise QuaternionSizeError(QUATERNION_SIZE_ERROR_MSG)

    normalized_quaternion = list(np.array(quaternion) / np.linalg.norm(quaternion))
    return normalized_quaternion


def confugate(quaternion: List[float]) -> List[float]:
    if len(quaternion) != 4:
        raise QuaternionSizeError(QUATERNION_SIZE_ERROR_MSG)
    result = [(quaternion[component] if component == 0 else -quaternion[component])
              for component in range(4)]
    return result


# ! Возращает список на 9 элементов
def convert_qtrn_to_mtrx(qtrn: List[float]) -> List[float]:
    if len(qtrn) != 4:
        raise QuaternionSizeError(QUATERNION_SIZE_ERROR_MSG)

    q01 = qtrn[0] * qtrn[1]
    q02 = qtrn[0] * qtrn[2]
    q03 = qtrn[0] * qtrn[3]
    q12 = qtrn[1] * qtrn[2]
    q13 = qtrn[1] * qtrn[3]
    q23 = qtrn[2] * qtrn[3]
    q1s = qtrn[1] * qtrn[1]
    q2s = qtrn[2] * qtrn[2]
    q3s = qtrn[3] * qtrn[3]
    a = qtrn[0] * qtrn[0] + q1s + q2s + q3s

    matrix = [
        1. - 2. * (q2s + q3s),
        2. * (q12 - q03),
        2. * (q13 + q02),
        2. * (q12 + q03),
        1. - 2. * (q1s + q3s),
        2. * (q23 - q01),
        2. * (q13 - q02),
        2. * (q23 + q01),
        1. - 2. * (q1s + q2s)
    ]
    return matrix


def qtrn_to_euler_angles(qtrn):
    if len(qtrn) != 4:
        raise QuaternionSizeError(QUATERNION_SIZE_ERROR_MSG)

    A = np.array(convert_qtrn_to_mtrx(qtrn=qtrn)).reshape(3, 3)
    # A =
    angles = [
        atan2(-A[1][2], A[1][1]),
        atan2(-A[2][0], A[0][0]),
        asin(A[1][0])
    ]

    return angles
