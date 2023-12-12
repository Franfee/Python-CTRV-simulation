# -*- coding: utf-8 -*-
# @Time    : 2021/4/5 11:33
# @Author  : FanAnfei
# @Software: PyCharm
# @python  : Python 3.7.9

import math
import numpy as np


dt = 0.05   # 先设Δt=0.05占一个位置，当实际运行EKF时会计算出前后两次测量的时间差


def TransitionFunction(n):
    """
    计算论文公式3.9中的状态转移矩阵,此时omega不为0,带有转弯
    :param n:状态量(x,y,v,theta,omega)
    :return:转移方程矩阵数据
    """
    return np.vstack((
        n[0] + (n[2] / n[4]) * (np.sin(n[3] + n[4] * dt) - np.sin(n[3])),
        n[1] + (n[2] / n[4]) * (-np.cos(n[3] + n[4] * dt) + np.cos(n[3])),
        n[2],
        n[3] + n[4] * dt,
        n[4]))


def TransitionFunction_1(m):
    """
    计算论文公式3.9中的状态转移矩阵,此时omega为0,直线运动
    :param m:状态量(x,y,v,theta,omega)
    :return:转移方程矩阵数据
    """
    return np.vstack((m[0] + m[2] * np.cos(m[3]) * dt,
                      m[1] + m[2] * np.sin(m[3]) * dt,
                      m[2],
                      m[3] + m[4] * dt,
                      m[4]))


def MeasurementExpression(k):
    """
    数据2 非线性雷达的观测表达式
    :param k:状态量
    :return:观测矩阵数据
    """
    return np.vstack((np.sqrt(k[0] * k[0] + k[1] * k[1]),
                      math.atan2(k[1], k[0]),
                      (k[0] * k[2] * np.cos(k[3]) + k[1] * k[2] * np.sin(k[3])) / np.sqrt(k[0] * k[0] + k[1] * k[1])))
