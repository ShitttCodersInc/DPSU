"""Правые части основных уравнений необходимых для вычислений
- 8
- 11
- 12

* Универсальный метод рунге кутта
"""
import numpy as np
from data import *
import quaternion as qtrn
from constants import *
import gravitationaldisturbance as grav
import sundisturbance as sun


# Система (8)
# --------------------------------------------------------------------------------------------------------------------
def R_omega(res_moment: List[float], omega: List[float], OMEGA: List[float], signal: List[float]) -> List[float]:
    if len(res_moment) != 3 or len(omega) != 3 or len(OMEGA) != 3 or len(signal) != 3:
        raise Exception("arguments len must be uqual 3")

    J_matr = np.array(J)
    J_matr_inv = np.linalg.inv(J_matr)
    J_ef_matr = np.array(J_ef)
    _res_moment = np.array(res_moment).reshape(3, 1)
    _omega = np.array(omega).reshape(3, 1)
    _OMEGA = np.array(OMEGA).reshape(3, 1)
    _signal = np.array(signal).reshape(3, 1)

    # Вычисляю поэтапно, раскрывая скобки
    result = J_matr.dot(_omega) + J_ef_matr.dot(_OMEGA)
    result = _res_moment - np.cross(_omega.reshape(3, ), result.reshape(3, )).reshape(3, 1) + _signal
    result = J_matr_inv.dot(result.reshape(3, 1))
    result = result.reshape(3, )
    return list(result)


def R_OMEGA(signal: List[float]) -> List[float]:
    if len(signal) != 3:
        raise Exception("signal len must be equal 3")

    J_ef_matr_inv = np.linalg.inv(np.array(J_ef))
    _signal = np.array(signal).reshape(3, 1)
    result = np.dot(J_ef_matr_inv, _signal).reshape(3, )
    return list(result)


# --------------------------------------------------------------------------------------------------------------------

# Уравнение (11)
# -----------------------------------------------------------------------------
def R_quat(quaterion: List[float], omega: List[float]) -> List[float]:
    if len(quaterion) != 4:
        raise qtrn.QuaternionSizeError(qtrn.QUATERNION_SIZE_ERROR_MSG)

    result = qtrn.multiply_quaternions(quat1=quaterion, quat2=[.0] + omega)
    result = [0.5 * el for el in result]

    return result


# -----------------------------------------------------------------------------


# Уравнение (12)
# -----------------------------------------------------------------------------
def R_A(r_j2000: List[float], t: float) -> List[float]:
    if len(r_j2000) != 3:
        raise Exception("r_j2000 len must be equal 3")

    _r_j2000 = np.array(r_j2000).reshape(3, 1)
    _r_j2000_mod = np.linalg.norm(_r_j2000)
    A = (- EARTH_GRAVITATIONAL_PARAMETER / (_r_j2000_mod ** 3)) * _r_j2000

    A_grav = grav.gravitational_acceleration(r_j2000=r_j2000, t=t)
    A_sun = sun.sun_acceleration(r_j2000=r_j2000, t=t)

    A_grav = np.array(A_grav).reshape(3, 1)
    A_sun = np.array(A_sun).reshape(3, 1)

    A += A_grav
    A += A_sun

    return A


# -----------------------------------------------------------------------------


def rungekutta4(f, h, x, y):
    k1 = f(x=x, y=y)
    k2 = f(x=x + 0.5 * h, y=y + 0.5 * h * k1)
    k3 = f(x=x + 0.5 * h, y=y + 0.5 * h * k2)
    k4 = f(x=x + h, y=y + h * k3)
    dy = (h / 6.) * (k1 + 2 * k2 + 2 * k3 + k4)
    return dy
