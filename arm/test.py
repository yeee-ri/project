#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys
    import tty
    import termios

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import *
from ik.ik2 import ik_cal

ADDR_TORQUE_ENABLE        = 64
ADDR_PROFILE_ACCELERATION = 108
ADDR_PROFILE_VELOCITY     = 112
ADDR_GOAL_POSITION        = 116
LEN_GOAL_POSITION         = 4
ADDR_PRESENT_POSITION     = 132
LEN_PRESENT_POSITION      = 4

BAUDRATE = 1000000
PROTOCOL_VERSION = 2.0

DXL0_ID = 12
DXL1_ID = 13
DXL2_ID = 14
DXL3_ID = 15

DEVICENAME = '/dev/ttyUSB1'

TORQUE_ENABLE = 1
TORQUE_DISABLE = 0
DXL_MOVING_STATUS_THRESHOLD = 20

DEG_PER_TICK = 0.087890625

PROFILE_ACCELERATION = 10
PROFILE_VELOCITY = 30

PROFILE_ACCELERATION_gripper = 50
PROFILE_VELOCITY_gripper = 60


def deg_to_tick(deg):
    return int(round(deg / DEG_PER_TICK))

def clamp_goal(goal_0, goal_1, goal_2, goal_3):
    if goal_0 < 740:
        goal_0 = 745
    if goal_0 > 3000:
        goal_0 = 3010

    if goal_1 < 745:
        goal_1 = 745
    if goal_1 > 3345:
        goal_1 = 3350

    if goal_2 < 855:
        goal_2 = 855
    if goal_2 > 3410:
        goal_2 = 3410

    if goal_3 < 3:
        goal_3 = 5
    if goal_3 > 1590:
        goal_3 = 1590

    return goal_0, goal_1, goal_2, goal_3

def write1(packetHandler, portHandler, dxl_id, addr, value):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
        portHandler, dxl_id, addr, value
    )
    if dxl_comm_result != COMM_SUCCESS:
        print(packetHandler.getTxRxResult(dxl_comm_result))
        quit()
    elif dxl_error != 0:
        print(packetHandler.getRxPacketError(dxl_error))
        quit()

def write4(packetHandler, portHandler, dxl_id, addr, value):
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(
        portHandler, dxl_id, addr, value
    )
    if dxl_comm_result != COMM_SUCCESS:
        print(packetHandler.getTxRxResult(dxl_comm_result))
        quit()
    elif dxl_error != 0:
        print(packetHandler.getRxPacketError(dxl_error))
        quit()

def enable_torque(packetHandler, portHandler, dxl_id):
    write1(packetHandler, portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    print("Dynamixel#%d has been successfully connected" % dxl_id)

def disable_torque(packetHandler, portHandler, dxl_id):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(
        portHandler, dxl_id, ADDR_TORQUE_ENABLE, TORQUE_DISABLE
    )
    if dxl_comm_result != COMM_SUCCESS:
        print(packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print(packetHandler.getRxPacketError(dxl_error))

def set_profile(packetHandler, portHandler, dxl_id, accel, velocity):
    write4(packetHandler, portHandler, dxl_id, ADDR_PROFILE_ACCELERATION, accel)
    write4(packetHandler, portHandler, dxl_id, ADDR_PROFILE_VELOCITY, velocity)

def set_profile_gripper(packetHandler, portHandler, dxl_id, accel, velocity):
    write4(packetHandler, portHandler, dxl_id, ADDR_PROFILE_ACCELERATION, accel)
    write4(packetHandler, portHandler, dxl_id, ADDR_PROFILE_VELOCITY, velocity)

def read_present_positions(groupSyncRead):
    dxl_comm_result = groupSyncRead.txRxPacket()
    if dxl_comm_result != COMM_SUCCESS:
        print(packetHandler.getTxRxResult(dxl_comm_result))
        return None

    if not groupSyncRead.isAvailable(DXL0_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION):
        print("[ID:%03d] groupSyncRead getdata failed" % DXL0_ID)
        return None
    if not groupSyncRead.isAvailable(DXL1_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION):
        print("[ID:%03d] groupSyncRead getdata failed" % DXL1_ID)
        return None
    if not groupSyncRead.isAvailable(DXL2_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION):
        print("[ID:%03d] groupSyncRead getdata failed" % DXL2_ID)
        return None
    if not groupSyncRead.isAvailable(DXL3_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION):
        print("[ID:%03d] groupSyncRead getdata failed" % DXL3_ID)
        return None

    goal_0 = groupSyncRead.getData(DXL0_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
    goal_1 = groupSyncRead.getData(DXL1_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
    goal_2 = groupSyncRead.getData(DXL2_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
    goal_3 = groupSyncRead.getData(DXL3_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)

    return goal_0, goal_1, goal_2, goal_3

def send_goal(groupSyncWrite, goal_0, goal_1, goal_2, goal_3):
    goal_0, goal_1, goal_2, goal_3 = clamp_goal(goal_0, goal_1, goal_2, goal_3)

    param_goal_position_0 = list(goal_0.to_bytes(4, byteorder="little", signed=False))
    param_goal_position_1 = list(goal_1.to_bytes(4, byteorder="little", signed=False))
    param_goal_position_2 = list(goal_2.to_bytes(4, byteorder="little", signed=False))
    param_goal_position_3 = list(goal_3.to_bytes(4, byteorder="little", signed=False))

    if not groupSyncWrite.addParam(DXL0_ID, param_goal_position_0):
        print("[ID:%03d] groupSyncWrite addparam failed" % DXL0_ID)
        quit()
    if not groupSyncWrite.addParam(DXL1_ID, param_goal_position_1):
        print("[ID:%03d] groupSyncWrite addparam failed" % DXL1_ID)
        quit()
    if not groupSyncWrite.addParam(DXL2_ID, param_goal_position_2):
        print("[ID:%03d] groupSyncWrite addparam failed" % DXL2_ID)
        quit()
    if not groupSyncWrite.addParam(DXL3_ID, param_goal_position_3):
        print("[ID:%03d] groupSyncWrite addparam failed" % DXL3_ID)
        quit()

    dxl_comm_result = groupSyncWrite.txPacket()
    if dxl_comm_result != COMM_SUCCESS:
        print(packetHandler.getTxRxResult(dxl_comm_result))

    groupSyncWrite.clearParam()

    return goal_0, goal_1, goal_2, goal_3

def wait_until_arrived(groupSyncRead, goal_0, goal_1, goal_2, goal_3, ignore_gripper_goal=False):
    prev_dxl3 = None

    while True:
        positions = read_present_positions(groupSyncRead)
        if positions is None:
            continue

        dxl0_present_position, dxl1_present_position, dxl2_present_position, dxl3_present_position = positions

        print(
            "[ID:%03d] Goal:%d Pres:%d\t[ID:%03d] Goal:%d Pres:%d\t[ID:%03d] Goal:%d Pres:%d\t[ID:%03d] Goal:%d Pres:%d"
            % (
                DXL0_ID, goal_0, dxl0_present_position,
                DXL1_ID, goal_1, dxl1_present_position,
                DXL2_ID, goal_2, dxl2_present_position,
                DXL3_ID, goal_3, dxl3_present_position
            )
        )

        arm_arrived = (
            abs(goal_0 - dxl0_present_position) <= DXL_MOVING_STATUS_THRESHOLD and
            abs(goal_1 - dxl1_present_position) <= DXL_MOVING_STATUS_THRESHOLD and
            abs(goal_2 - dxl2_present_position) <= DXL_MOVING_STATUS_THRESHOLD
        )

        if ignore_gripper_goal:
            grip_arrived = True
            if prev_dxl3 is not None and abs(dxl3_present_position - prev_dxl3) < 3:
                grip_arrived = True
        else:
            grip_arrived = abs(goal_3 - dxl3_present_position) <= DXL_MOVING_STATUS_THRESHOLD

        prev_dxl3 = dxl3_present_position

        if arm_arrived and grip_arrived:
            break

portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

groupSyncWrite = GroupSyncWrite(
    portHandler, packetHandler, ADDR_GOAL_POSITION, LEN_GOAL_POSITION
)
groupSyncRead = GroupSyncRead(
    portHandler, packetHandler, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION
)

if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    getch()
    quit()

if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    getch()
    quit()

set_profile(packetHandler, portHandler, DXL0_ID, PROFILE_ACCELERATION, PROFILE_VELOCITY)
set_profile(packetHandler, portHandler, DXL1_ID, PROFILE_ACCELERATION, PROFILE_VELOCITY)
set_profile(packetHandler, portHandler, DXL2_ID, PROFILE_ACCELERATION, PROFILE_VELOCITY)
set_profile_gripper(packetHandler, portHandler, DXL3_ID, PROFILE_ACCELERATION_gripper, PROFILE_VELOCITY_gripper)

enable_torque(packetHandler, portHandler, DXL0_ID)
enable_torque(packetHandler, portHandler, DXL1_ID)
enable_torque(packetHandler, portHandler, DXL2_ID)
enable_torque(packetHandler, portHandler, DXL3_ID)

if not groupSyncRead.addParam(DXL0_ID):
    print("[ID:%03d] groupSyncRead addparam failed" % DXL0_ID)
    quit()
if not groupSyncRead.addParam(DXL1_ID):
    print("[ID:%03d] groupSyncRead addparam failed" % DXL1_ID)
    quit()
if not groupSyncRead.addParam(DXL2_ID):
    print("[ID:%03d] groupSyncRead addparam failed" % DXL2_ID)
    quit()
if not groupSyncRead.addParam(DXL3_ID):
    print("[ID:%03d] groupSyncRead addparam failed" % DXL3_ID)
    quit()

while True:
    print("q: close, w: open, m: move, ESC: quit")
    ch = getch()

    if ch == chr(0x1b):
        break

    if ch == 'q' or ch == 'w':
        positions = read_present_positions(groupSyncRead)
        if positions is None:
            continue

        goal_0, goal_1, goal_2, goal_3 = positions

        if ch == 'q':
            goal_3 = deg_to_tick(0)
            print("Gripper Close")
        else:
            goal_3 = deg_to_tick(140)
            print("Gripper Open")

        goal_0, goal_1, goal_2, goal_3 = send_goal(groupSyncWrite, goal_0, goal_1, goal_2, goal_3)
        wait_until_arrived(groupSyncRead, goal_0, goal_1, goal_2, goal_3, ignore_gripper_goal=True)
        continue

    if ch == 'm':
        try:
            x, y = input("Enter input x, y: ").split()
            d = int(x)
            h = int(y)
        except ValueError:
            print("Again")
            continue

        deg_0, deg_1, deg_2 = ik_cal(d, h)

        if deg_0 is None or deg_1 is None or deg_2 is None:
            print("Calculation Error")
            continue

        positions = read_present_positions(groupSyncRead)
        if positions is None:
            continue

        _, _, _, goal_3 = positions

        goal_0 = deg_to_tick(deg_0)
        goal_1 = deg_to_tick(deg_1)
        goal_2 = deg_to_tick(deg_2)

        goal_0, goal_1, goal_2, goal_3 = send_goal(groupSyncWrite, goal_0, goal_1, goal_2, goal_3)
        wait_until_arrived(groupSyncRead, goal_0, goal_1, goal_2, goal_3, ignore_gripper_goal=False)
        continue

disable_torque(packetHandler, portHandler, DXL0_ID)
disable_torque(packetHandler, portHandler, DXL1_ID)
disable_torque(packetHandler, portHandler, DXL2_ID)
disable_torque(packetHandler, portHandler, DXL3_ID)

groupSyncRead.clearParam()
portHandler.closePort()