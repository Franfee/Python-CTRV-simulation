# -*- coding: utf-8 -*-
# @Time    : 2021/5/14 14:50
# @Author  : FanAnfei
# @Software: PyCharm
# @python  : Python 3.7.9

import numpy as np


def GaussianNoise(N, snr, X):
    """
    产生高斯白噪声
    原理:中心极限定理:random(N)*sqrt(sum(Xi.^2)*10.^(-snr/10))或者调用random.gauss(mu,sigma)
    :param N:序列长度
    :param snr:均值
    :param X:方差
    :return:高斯白噪声序列
    """
    noise = np.random.randn(N)
    snr = 10 ** (snr / 10)
    power = np.mean(np.square(X))
    n_power = power / snr
    noise = noise * np.sqrt(n_power)
    return noise


def RMSE(estimatedValue, actualValue):
    """
    输出估计的均方误差（RMSE）
    :param estimatedValue:估计值,np一维向量
    :param actualValue:准确值,np一维向量
    :return: 均方误差
    """
    est = np.ravel(estimatedValue)
    act = np.ravel(actualValue)
    return np.sqrt(np.mean((est - act) ** 2))
