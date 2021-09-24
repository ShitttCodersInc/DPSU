import output
import controllaw
from equations import *
from data import *
import gravitationalmoment as grav_moment

r_list = [r]
V_list = [V]
A_list = [[.0] * 3]
t_list = [0.0]
r1 = np.array(r).reshape(3, 1)
V1 = np.array(V).reshape(3, 1)
A1 = np.array([.0] * 3).reshape(3, 1)

quaternion_list = [QUATERNION_0]
angular_velocity_list = [ANGULAR_VELOCITY_0]
OMEGA_list = [[.0] * 3]

quaternion1 = np.array(QUATERNION_0).reshape(4, 1)
angular_velocity1 = np.array(ANGULAR_VELOCITY_0).reshape(3, 1)
OMEGA1 = np.array([.0] * 3).reshape(3, 1)


# best 0.1 4
def euler(time: float = 1400.0, dt: float = .1, Kp: float = .1, Ka: float = 4) -> None:
    global V1, r1, A1, quaternion1, OMEGA1, angular_velocity1
    t = 0
    while t < time:
        t += dt
        print(f'{t / time * 100:.2f}%')

        # орбитальное движение (12)
        # -------------------------------------------------
        V2 = V1 + A1 * dt
        r2 = r1 + V2 * dt
        A2 = R_A(r_j2000=list(r2.reshape(3, )), t=t)
        # -------------------------------------------------

        # Кватернион (11)
        # --------------------------------------------------------------------------------
        quaternion2 = quaternion1 + dt * np.array(R_quat(quaterion=list(quaternion1.reshape(4, )),
                                                         omega=list(angular_velocity1.reshape(3, )))).reshape(4, 1)

        quaternion2 = np.array(qtrn.normalize(quaternion=list(quaternion2.reshape(4, )))).reshape(4, 1)
        # --------------------------------------------------------------------------------

        # Система (8)
        # --------------------------------------------------------------------------------------------
        signal = controllaw.signal(quaternion=list(quaternion1.reshape(4, )),
                                   angular_velocity=list(angular_velocity1.reshape(3, )),
                                   OMEGA=list(OMEGA1.reshape(3, )),
                                   Kp=Kp, Ka=Ka)

        OMEGA2 = OMEGA1 + dt * np.array(R_OMEGA(signal=signal)).reshape(3, 1)

        total_moments = grav_moment.gravity_moment(R=np.linalg.norm(r1),
                                                   quaternion=list(quaternion1.reshape(4, )),
                                                   r_j2000=list(r1.reshape(3, )))

        angular_velocity2 = angular_velocity1 + dt * np.array(R_omega(res_moment=total_moments,
                                                                      omega=list(angular_velocity1.reshape(3, )),
                                                                      OMEGA=list(OMEGA1.reshape(3, )),
                                                                      signal=signal)).reshape(3, 1)
        # --------------------------------------------------------------------------------------------

        r_list.append(list(r2.reshape(1, 3)[0]))
        V_list.append(list(V2.reshape(1, 3)[0]))
        A_list.append(A2)
        t_list.append(t)
        quaternion_list.append(list(quaternion2.reshape(4, )))
        OMEGA_list.append(list(OMEGA2.reshape(3, )))
        angular_velocity_list.append(list(angular_velocity2.reshape(3, )))

        r1 = r2
        V1 = V2
        A1 = A2
        quaternion1 = quaternion2
        OMEGA1 = OMEGA2
        angular_velocity1 = angular_velocity2


def runge_kutta_4(time: float = 200.0, dt: float = .1, Kp: float = .1, Ka: float = 4.5):
    global V1, r1, A1, quaternion1, OMEGA1, angular_velocity1
    t = 0
    while t < time:
        t += dt
        print(f'{t / time * 100}%')

        # орбитальное движение (12)
        # -------------------------------------------------
        V2 = V1 + rungekutta4(f=lambda x, y: R_A(r_j2000=list(r1.reshape(3, )), t=x), h=dt, x=t, y=V1)
        r2 = r1 + rungekutta4(f=lambda x, y: V1, h=dt, x=t, y=r1)
        # -------------------------------------------------

        # Кватернион (11)
        # --------------------------------------------------------------------------------
        quaternion2 = quaternion1 + dt * np.array(R_quat(quaterion=list(quaternion1.reshape(4, )),
                                                         omega=list(angular_velocity1.reshape(3, )))).reshape(4, 1)

        quaternion2 = quaternion1 + rungekutta4(
            f=lambda x, y: np.array(R_quat(quaterion=list(y.reshape(4, )),
                                           omega=list(angular_velocity1.reshape(3, )))).reshape(4, 1),
            h=dt,
            x=t,
            y=quaternion1)

        quaternion2 = np.array(qtrn.normalize(quaternion=list(quaternion2.reshape(4, )))).reshape(4, 1)
        # --------------------------------------------------------------------------------

        # Система (8)
        # --------------------------------------------------------------------------------------------
        signal = controllaw.signal(quaternion=list(quaternion1.reshape(4, )),
                                   angular_velocity=list(angular_velocity1.reshape(3, )),
                                   OMEGA=list(OMEGA1.reshape(3, )),
                                   Kp=Kp, Ka=Ka)

        # OMEGA2 = OMEGA1 + dt * np.array(R_OMEGA(signal=signal)).reshape(3, 1)
        OMEGA2 = OMEGA1 + rungekutta4(f=lambda x, y: np.array(R_OMEGA(signal=signal)).reshape(3, 1), h=dt, x=t,
                                      y=OMEGA1)

        total_moments = grav_moment.gravity_moment(R=np.linalg.norm(r1),
                                                   quaternion=list(quaternion1.reshape(4, )),
                                                   r_j2000=list(r1.reshape(3, )))

        angular_velocity2 = angular_velocity1 + dt * np.array(R_omega(res_moment=total_moments,
                                                                      omega=list(angular_velocity1.reshape(3, )),
                                                                      OMEGA=list(OMEGA1.reshape(3, )),
                                                                      signal=signal)).reshape(3, 1)
        angular_velocity2 = angular_velocity1 + rungekutta4(f=lambda x, y: np.array(R_omega(res_moment=total_moments,
                                                                                            omega=list(y.reshape(3, )),
                                                                                            OMEGA=list(
                                                                                                OMEGA1.reshape(3, )),
                                                                                            signal=signal)).reshape(3,
                                                                                                                    1),
                                                            h=dt,
                                                            x=t,
                                                            y=angular_velocity1)
        # --------------------------------------------------------------------------------------------

        A2 = R_A(r_j2000=list(r1.reshape(3, )), t=t)

        r_list.append(list(r2.reshape(3, )))
        V_list.append(list(V2.reshape(3, )))
        A_list.append(A2)
        t_list.append(t)
        quaternion_list.append(list(quaternion2.reshape(4, )))
        OMEGA_list.append(list(OMEGA2.reshape(3, )))
        angular_velocity_list.append(list(angular_velocity2.reshape(3, )))

        r1 = r2
        V1 = V2
        A1 = A2
        quaternion1 = quaternion2
        OMEGA1 = OMEGA2
        angular_velocity1 = angular_velocity2


def main():
    # euler()
    runge_kutta_4()
    output.quaternion_output(time_list=t_list, quaternion=quaternion_list)
    output.radius_output(time_list=t_list, radius_list=r_list)
    output.omega_output(time_list=t_list, omega=angular_velocity_list)
    output.OMEGA_output(time_list=t_list, OMEGA=OMEGA_list)


if __name__ == '__main__':
    main()
