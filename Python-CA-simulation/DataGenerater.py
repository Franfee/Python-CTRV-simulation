# -*- coding: utf-8 -*-
# @Time    : 2021/5/11 02:18
# @Author  : FanAnfei
# @Software: PyCharm
# @python  : Python 3.7.9


from matplotlib import pyplot as plt

from Util.NoiseControler import GaussianNoise

if __name__ == '__main__':
    # 数据保存名
    dataName = "ca_data.txt"
    # 数据路径
    dataPath = "Data/" + dataName
    # 数据内容
    dataContent = ""
    # 数据长度
    stepLen = 200
    # 白噪声数据
    NoiseX = GaussianNoise(stepLen, 0, 0.25)
    # 真实位置
    truePositionX = []
    # 测量数据
    measureX = []
    dt = 0.05

    # CA 运动数据
    for i in range(0, stepLen):
        t = 0.05 * i
        # 运动方程
        moveEqn = 5.0 - 2.0 * t + 3.0 * t * t
        truePositionX.append(moveEqn)
        measureX.append(truePositionX[i] + NoiseX[i])
        dataContent += str("%.6f" % measureX[i]) + '\t' + str("%.6f" % truePositionX[i]) + '\n'

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
        plt.plot(range(0, i), truePositionX[0:i], 'r.--', label=u"真实值")
        plt.xlabel(u"时刻")
        plt.ylabel(u"X轴坐标")
        plt.title(u"真实位置")
        plt.grid(True, linestyle='-.')  # 网格化
        plt.legend()  # 打开label标记

        if i < stepLen - 1:
            plt.pause(0.002)
        else:
            plt.pause(5)  # 结果展示5秒
