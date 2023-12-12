# -*- coding: utf-8 -*-
# @Time    : 2021/5/14 14:46
# @Author  : FanAnfei
# @Software: PyCharm
# @python  : Python 3.7.9

import math
import numpy as np


def ControlPsi(psi):
    """
    角度量的数值都应该控制在 [ − π , π ]
    角度加减 2 π不变，所以用如下函数表示函数来调整角度：
    :param psi:角度
    :return:角度
    """
    while psi > np.pi or psi < -np.pi:
        if psi > np.pi:
            psi = psi - 2 * np.pi
        if psi < -np.pi:
            psi = psi + 2 * np.pi
    return psi


def GetRho(locX, locY):
    """
    生成距离ρ
    :param locX:坐标X
    :param locY:坐标Y
    :return: 距离值
    """
    return np.sqrt(locX * locX + locY * locY)


def GetPsi(locX, locY):
    """
    生成距离ψ
    :param locX: 坐标X
    :param locY: 坐标Y
    :return: 角度值
    """
    return math.atan2(locY, locX)


def GetDotRho(vecX, vecY, locX, locY):
    """
    生成距离变化dρ
    :param vecX:速度X
    :param vecY:速度Y
    :param locX:坐标X
    :param locY:坐标Y
    :return:
    """
    return (vecX * GetRho(locX, locY) * np.cos(GetPsi(locX, locY)) +
            vecY * GetRho(locX, locY) * np.sin(GetPsi(locX, locY))) / np.sqrt(locX * locX + locY * locY)
