"""Методы для вывода данных
- графики
- лог файл <?csv>
"""
import datetime
import os
from typing import List

import matplotlib.pyplot as plt
import numpy as np

now = datetime.datetime.now()

FOLDER = 'data'
SUBFOLDER = '{:02}{:02}{:02}{:02}{:02}{:02}'.format(now.hour, now.minute, now.second, now.day, now.month, now.year)
DATAPATH = f'{FOLDER}/{SUBFOLDER}'
CSV_SPLITTER = ';'


def output_all(time_list: List[float], radius_list: List[List[float]], omega: List[List[float]],
               OMEGA: List[List[float]], quaternion: List[List[float]]):
    radius_output(time_list=time_list, radius_list=radius_list)
    omega_output(time_list=time_list, omega=omega)
    OMEGA_output(time_list=time_list, OMEGA=OMEGA)
    quaternion_output(time_list=time_list, quaternion=quaternion)


def radius_output(time_list: List[float], radius_list: List[List[float]]) -> None:
    if len(time_list) != len(radius_list):
        raise Exception("time_list and radius list len must be equaled")

    if not os.path.exists(FOLDER):
        os.mkdir(FOLDER)
    if not os.path.exists(DATAPATH):
        os.mkdir(DATAPATH)

    x = [r[0] for r in radius_list]
    y = [r[1] for r in radius_list]
    z = [r[2] for r in radius_list]
    radius_module = [np.linalg.norm(r) for r in radius_list]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x, y, z, label='parametric curve')
    ax.scatter([x[0]], [y[0]], [z[0]], 'b.')
    ax.scatter([x[-1]], [y[-1]], [z[-1]], 'r.')
    plt.savefig(f'{DATAPATH}/3d.png')
    plt.show()

    plt.grid()
    plt.xlabel("Время, сек")
    plt.ylabel("Расстояние, км")
    plt.plot(time_list, x, label='x(t)')
    plt.plot(time_list, y, label='y(t)')
    plt.plot(time_list, z, label='z(t)')
    plt.legend()
    plt.savefig(f'{DATAPATH}/xyz.png')
    plt.show()

    plt.grid()
    plt.xlabel("Время, сек")
    plt.ylabel("Расстояние, км")
    plt.plot(time_list, radius_module, label='|r(t)|')
    plt.legend()
    plt.savefig(f'{DATAPATH}/r_module.png')
    plt.show()

    with open(f"{DATAPATH}/radius_log.csv", "w") as csv:
        csv.write('time;rx;ry;rz;rmod;\n')

        for i in range(len(time_list)):
            csv.write(f'{time_list[i]};{x[i]};{y[i]};{z[i]};{radius_module[i]};\n')


def omega_output(time_list: List[float], omega: List[List[float]]) -> None:
    if len(time_list) != len(omega):
        raise Exception("time_list and omega list len must be equaled")

    if not os.path.exists(FOLDER):
        os.mkdir(FOLDER)
    if not os.path.exists(DATAPATH):
        os.mkdir(DATAPATH)

    x = [r[0] for r in omega]
    y = [r[1] for r in omega]
    z = [r[2] for r in omega]
    omega_module = [np.linalg.norm(r) for r in omega]

    plt.grid()
    plt.xlabel("Время, сек")
    plt.ylabel("Угловая скорость, рад/с")
    plt.plot(time_list, x, label='ω_x(t)')
    plt.plot(time_list, y, label='ω_y(t)')
    plt.plot(time_list, z, label='ω_z(t)')
    plt.legend()
    plt.savefig(f'{DATAPATH}/omega_xyz.png')
    plt.show()

    plt.grid()
    plt.xlabel("Время, сек")
    plt.ylabel("Угловая скорость, км")
    plt.plot(time_list, omega_module, label='|ω(t)|')
    plt.legend()
    plt.savefig(f'{DATAPATH}/omega_module.png')
    plt.show()

    with open(f"{DATAPATH}/omega_log.csv", "w") as csv:
        csv.write('time;omega_x;omega_y;omega_z;omega_mod;\n')

        for i in range(len(time_list)):
            csv.write(f'{time_list[i]};{x[i]};{y[i]};{z[i]};{omega_module[i]};\n')


def OMEGA_output(time_list: List[float], OMEGA: List[List[float]]) -> None:
    if len(time_list) != len(OMEGA):
        raise Exception("time_list and omega list len must be equaled")

    if not os.path.exists(FOLDER):
        os.mkdir(FOLDER)
    if not os.path.exists(DATAPATH):
        os.mkdir(DATAPATH)

    x = [r[0] for r in OMEGA]
    y = [r[1] for r in OMEGA]
    z = [r[2] for r in OMEGA]
    OMEGA_module = [np.linalg.norm(r) for r in OMEGA]

    plt.grid()
    plt.xlabel("Время, сек")
    plt.ylabel("Угловая скорость, рад/с")
    plt.plot(time_list, x, label='Ω_x(t)')
    plt.plot(time_list, y, label='Ω_y(t)')
    plt.plot(time_list, z, label='Ω_z(t)')
    plt.legend()
    plt.savefig(f'{DATAPATH}/_OMEGA_xyz.png')
    plt.show()

    plt.grid()
    plt.xlabel("Время, сек")
    plt.ylabel("Угловая скорость, рад/с")
    plt.plot(time_list, OMEGA_module, label='|Ω(t)|')
    plt.legend()
    plt.savefig(f'{DATAPATH}/_OMEGA_module.png')
    plt.show()

    with open(f"{DATAPATH}/BIG_OMEGA_log.csv", "w") as csv:
        csv.write('time;OMEGA_x;OMEGA_y;OMEGA_z;OMEGA_mod;\n')

        for i in range(len(time_list)):
            csv.write(f'{time_list[i]};{x[i]};{y[i]};{z[i]};{OMEGA_module[i]};\n')


def quaternion_output(time_list: List[float], quaternion: List[List[float]]) -> None:
    if len(time_list) != len(quaternion):
        raise Exception("time_list and omega list len must be equaled")

    if not os.path.exists(FOLDER):
        os.mkdir(FOLDER)
    if not os.path.exists(DATAPATH):
        os.mkdir(DATAPATH)

    qtrn0 = [qtrn[0] for qtrn in quaternion]
    qtrn1 = [qtrn[1] for qtrn in quaternion]
    qtrn2 = [qtrn[2] for qtrn in quaternion]
    qtrn3 = [qtrn[3] for qtrn in quaternion]
    qtrn_mod = [np.linalg.norm(qtrn) for qtrn in quaternion]

    with open(f"{DATAPATH}/quaternion_log.csv", "w") as csv:
        csv.write('time;qtrn[0];qtrn[1];qtrn[2];qtrn[3];qtrn_mod;\n')

        for i in range(len(time_list)):
            csv.write(f'{time_list[i]};{qtrn0[i]};{qtrn1[i]};{qtrn2[i]};{qtrn3[i]};{qtrn_mod[i]};\n')
