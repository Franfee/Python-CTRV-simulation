# -*- coding: utf-8 -*-
# @Time    : 2021/5/7 14:50
# @Author  : FanAnfei
# @Software: PyCharm
# @python  : Python 3.7.9


import numpy as np
from matplotlib import pyplot as plt

from Util.LoadData import LoadData
from Util.NoiseControler import RMSE

if __name__ == '__main__':
    # 进行矩阵计算的方法:np.matmul(a, b)  和  np.dot(a, b)
    # 载入数据
    Data = np.array(LoadData("Data/ca_data.txt"))

    # Step 1 :初始化
    y = Data[:, 0]  # 迭加有高斯白噪声的采样值
    trueValue = Data[:, 1]  # 真实值

    # 序列长度
    stepLen = len(Data[:, 1])

    # 系统状态转移矩阵
    A = np.array([[1.0, 0.05, 0.00125],
                  [0.0, 1.0, 0.05],
                  [0.0, 0.0, 1.0]])

    # 模型噪声Wk
    q = np.array([[0.25, 0.0, 0.0],
                  [0.0, 0.25, 0.0],
                  [0.0, 0.0, 0.25]])
    # 观测噪音Vk
    r = np.array([[0.25]])
    # 观测矩阵
    h = np.array([[1.0, 0.0, 0.0]])

    # 返回时存放最后时刻的估计误差协方差,存放初值P0,
    p = np.zeros((3, 3))

    # 状态估计向量xk[i,j]    i时刻,j分量的状态估计
    x = np.zeros((stepLen, 3))

    # 最后时刻稳定增益矩阵
    k = np.zeros((3, 1))

    # ################Kalman################

    # Step 2: 计算一步预测误差方差估计: P = APA'
    p = np.matmul(np.matmul(A, p), A.T)

    for stepLenIndex in range(1, stepLen):
        # Step 3:计算滤波增益矩阵:K=PH'(HPH'+R)^-1
        k = np.matmul(np.matmul(p, h.T), np.linalg.inv(np.matmul(np.matmul(h, p), h.T) + r))

        # Step 4: 计算后验状态向量修正:x=x+K(z-Hx)
        x[stepLenIndex] = x[stepLenIndex - 1] + np.matmul(k, (y[stepLenIndex - 1] - np.matmul(h, x[stepLenIndex - 1])))

        # Step 5: 更新估计误差方差阵:P=(I-KH)P
        p = np.eye(3) - np.matmul(np.matmul(k, h), p)

        # Step 6:回到Step2计算预测误差:P= APA'+ Q
        p = np.matmul(np.matmul(A, p), A.T) + q

    # Step 7:结果输出
    print("-------------------------------------------------------------------")
    print("  t时刻\t  s真值\t  y观测值   x(0)滤波值         x(1)            x(2)   ")
    for sequence in range(0, stepLen):
        if (sequence % 5) == 0:
            t = sequence * 0.05  # t为时刻
            print("%6.2f\t%6.2f\t%6.2f\t%e\t%e\t%e" %
                  (t, trueValue[sequence], y[sequence],
                   np.array(x[sequence, 0]).tolist(),
                   np.array(x[sequence, 1]).tolist(),
                   np.array(x[sequence, 2]).tolist()))
    print("-------------------------------------------------------------------")

    # ########## Visualization ##############
    # 画图和分析
    estimatedValue = x[:, 0]
    actualValue = np.array([trueValue])
    print("最大误差:")
    print(np.max(np.abs(estimatedValue-actualValue)))
    print("平均误差:")
    print(np.mean(np.abs(estimatedValue - actualValue)))
    print("估计的均方误差RMSE:")
    print(RMSE(estimatedValue, actualValue))

    # #####
    # 创建画板
    fig = plt.figure()
    # label和title标注的中文支持
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # 显示数据图
    plt.plot(range(0, stepLen), trueValue, 'b.--', label=u"真实值")
    plt.plot(range(0, stepLen), y, 'r.', label=u"测量值")
    plt.plot(range(0, stepLen), x[:, 0], 'g.--', label=u"滤波值")
    plt.xlabel(u"时刻t")
    plt.ylabel(u"位置x")
    plt.title(u"KF滤波仿真分析")
    plt.grid(True, linestyle='-.')
    plt.legend()  # 显示标注
    # 显示画板
    plt.show()

    # 清除画板
    plt.clf()
    # label和title标注的中文支持
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # 显示数据图
    plt.plot(range(0, stepLen), trueValue-x[:, 0], 'r.', label=u"误差值")
    plt.plot(range(0, stepLen), (trueValue - x[:, 0]) / trueValue, 'b.', label=u"误差百分比")
    plt.xlabel(u"时刻t")
    plt.ylabel(u"位置误差x")
    plt.title(u"KF滤波仿真误差分析")
    plt.grid(True, linestyle='-.')
    plt.legend()  # 显示标注
    # 显示画板
    plt.show()

