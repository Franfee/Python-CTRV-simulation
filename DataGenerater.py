# -*- coding: utf-8 -*-
# @Time    : 2021/5/11 02:18
# @Author  : FanAnfei
# @Software: PyCharm
# @python  : Python 3.7.9


import numpy as np
from matplotlib import pyplot as plt

from Util.NoiseControler import GaussianNoise
from Util.NonlinearControler import GetPsi, GetRho, GetDotRho
from Util.TimeManager import TimeToStamp16, StrTimeToDatetime, StampsToStrTime


if __name__ == '__main__':
    # 时间转换测试
    print(StampsToStrTime(1620632443050000))
    print(StampsToStrTime(1620632443000000))
    # 数据保存名
    dataName = "person_data.txt"
    # 数据路径
    dataPath = "Data/" + dataName
    # 数据内容
    dataContent = ""
    # 数据长度
    stepLen = 500

    # 真实运动初始信息
    x = 5.20
    y = 5.20
    vx = 1.70
    vy = 1.70
    vs = np.sqrt(vx * vx + vy * vy)  # 常速度不变
    theta = GetPsi(x, y)

    truePositionX = []
    truePositionY = []
    trueVelocityX = []
    trueVelocityY = []

    dt = 0.05
    NoiseX = GaussianNoise(500, 0, 0.25)
    NoiseY = GaussianNoise(500, 0, 0.25)

    # CTRV 运动数据
    # 恒定转弯,合速度不变
    for i in range(0, stepLen):
        # --------------真实运动-------------------
        # 运动过程
        if i <= (stepLen / 2):
            w = 0.35  # 恒定转弯率
        else:
            w = -0.35  # 恒定转弯率
        theta += w * dt
        vx = vs * np.cos(theta)
        vy = vs * np.sin(theta)
        x += vx * dt
        y += vy * dt

        # ----------------------------------

        # -----------保存数据画图------------
        truePositionX.append(x)
        truePositionY.append(y)
        trueVelocityX.append(vx)
        trueVelocityY.append(vy)
        # ---------------------------------

        # ------------------------
        # 测量噪声
        measureX = x + NoiseX[i]
        measureY = y + NoiseY[i]
        # ------------------------
        # --------------------数据生成----------------------------
        # 当前时间
        nowTime = i * dt
        timeStr = "2021-05-11 15:22:" + str("%.6f" % nowTime)
        # print(timeStr)
        nowDateTime = StrTimeToDatetime(timeStr)
        nowStamps = TimeToStamp16(nowDateTime)
        # print(nowStamps)
        # -------------------------
        if i % 2 == 0:
            title = 'L'
            # 测量数据
            dataContent += title + '\t' + str("%.6f" % measureX) + '\t' + str("%.6f" % measureY)
            dataContent += '\t' + str(nowStamps)
            # 真实数据
            dataContent += '\t' + str("%.6f" % x) + '\t' + str("%.6f" % y)
            dataContent += '\t' + str("%.6f" % vx) + '\t' + str("%.6f" % vy) + '\n'
        else:
            title = 'R'
            measureRho = GetRho(measureX, measureY)
            measurePsi = GetPsi(measureX, measureY)
            measureDotRho = GetDotRho(vx, vy, measureX, measureY)
            # 测量数据
            dataContent += title + '\t' + str("%.6f" % measureRho) + '\t' + str("%.6f" % measurePsi)
            dataContent += '\t' + str("%.6f" % measureDotRho) + '\t' + str(nowStamps)
            # 真实数据
            dataContent += '\t' + str("%.6f" % x) + '\t' + str("%.6f" % y)
            dataContent += '\t' + str("%.6f" % vx) + '\t' + str("%.6f" % vy) + '\n'

    # print(dataContent)
    # -------------数据保存-----------------
    with open(dataPath, 'w') as f:
        f.writelines(dataContent)
    # ------------------------------------
    print("数据保存成功")

    # -------------画图---------------------
    fig = plt.figure(0)  # 生成画板
    # label和title标注的中文支持
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    plt.ion()  # 不暂停绘制
    for i in range(1, stepLen):
        plt.clf()  # 清除画板
        plt.subplot(1, 2, 1)
        plt.plot(truePositionX[0:i], truePositionY[0:i], 'r.--', label=u"真实值")
        plt.xlabel(u"X轴坐标")
        plt.ylabel(u"Y轴坐标")
        plt.title(u"真实位置")
        plt.grid(True, linestyle='-.')  # 网格化
        plt.legend()  # 打开label标记

        plt.subplot(1, 2, 2)
        plt.plot(trueVelocityX[0:i], trueVelocityY[0:i], 'r.--', label=u"真实值")
        plt.xlabel(u"X方向速度")
        plt.ylabel(u"Y方向速度")
        plt.title(u"真实速度")
        plt.grid(True, linestyle='-.')  # 网格化
        plt.legend()  # 打开label标记

        if i < stepLen - 1:
            plt.pause(0.002)
        else:
            plt.pause(5)  # 结果展示5秒
