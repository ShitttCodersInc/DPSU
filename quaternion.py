"""Методы для работы с кватернионом
- Перемножение кватернионов
- Нормировака кватерниона
- Условие необходимости нормировки кватерниона
- Модуль кватерниона
- Сопряженный кватернион
"""
import math
from typing import List
import numpy as np

QUATERNION_SIZE_ERROR_MSG = 'Quaternion size must be equal 4'


class QuaternionSizeError(Exception):
    pass


def multiply_quaternions(quat1: List[float], quat2: List[float]) -> List[float]:
    if len(quat1) != 4 or len(quat2) != 4:
        raise QuaternionSizeError(QUATERNION_SIZE_ERROR_MSG)

    multiply_result = [
        quat1[0] * quat2[0] - quat1[1] * quat2[1] - quat1[2] * quat2[2] - quat1[3] * quat2[3],
        quat1[0] * quat2[1] + quat1[1] * quat2[0] + quat1[3] * quat2[2] - quat1[2] * quat2[3],
        quat1[0] * quat2[2] + quat1[2] * quat2[0] + quat1[1] * quat2[3] - quat1[3] * quat2[1],
        quat1[0] * quat2[3] + quat1[3] * quat2[0] + quat1[2] * quat2[1] - quat1[1] * quat2[2]
    ]

    return multiply_result


def normalize(quaternion: List[float]) -> List[float]:
    if len(quaternion) != 4:
        raise QuaternionSizeError(QUATERNION_SIZE_ERROR_MSG)

    mod = np.linalg.norm(quaternion)
    normalized_quaternion = [component / mod for component in quaternion]
    return normalized_quaternion


def is_need_to_normalized(quaternion: List[float], error: float = 1e-3) -> bool:
    if len(quaternion) != 4:
        raise QuaternionSizeError(QUATERNION_SIZE_ERROR_MSG)

    return math.fabs(1 - np.linalg.norm(quaternion)) >= error


def confugate(quaternion: List[float]) -> List[float]:
    if len(quaternion) != 4:
        raise QuaternionSizeError(QUATERNION_SIZE_ERROR_MSG)
    result = [(quaternion[component] if component == 0 else -quaternion[component])
              for component in range(4)]
    return result
