# -*- coding: utf-8 -*-
# @Time    : 2021/5/8 21:52
# @Author  : FanAnfei
# @Software: PyCharm
# @python  : Python 3.7.9


import numpy as np
import numdifftools as nd

from matplotlib import pyplot as plt


from Util.MyFun import TransitionFunction, TransitionFunction_1, MeasurementExpression

from Util.LoadData import LoadData
from Util.NoiseControler import RMSE
from Util.NonlinearControler import ControlPsi

if __name__ == '__main__':
    # ===================Step1========================
    # 读取数据
    measureData = LoadData('Data/person_data.txt')
    # measureData = LoadData('Data/test_data.txt')
    # 步数
    stepLen = len(measureData)
    # 预定义数据空间
    statusSpace = np.zeros([5, 1])  # 状态空间(x,y,ρ,ψ,ρ˙)
    statusSpaceList = np.zeros([5, stepLen])  # 状态空间的序列,用于保存每一步的数据
    # 真实的(x, y, v_x, v_y)
    truePositionX = []
    truePositionY = []
    trueVelocityX = []
    trueVelocityY = []
    # 测量数据融合(非线性数据会融合到x,y)
    measurePositionX = []
    measurePositionY = []
    # 滤波得到的数据(通过状态空间得到)
    EKFPositionX = []
    EKFPositionY = []
    EKFVelocityX = []
    EKFVelocityY = []

    # 初始化P(对角矩阵)
    P = np.diag([1.0, 1.0, 1.0, 1.0, 1.0])
    # 激光雷达的测量矩阵(线性),
    H_lidar = np.array([[1., 0., 0., 0., 0.],
                        [0., 1., 0., 0., 0.]])

    # 测量噪声R,处理噪声的中直线加速度项的标准差 σa ，转角加速度项的标准差σω˙
    R_lidar = np.array([[0.0225, 0.], [0., 0.0225]])
    R_radar = np.array([[0.09, 0., 0.], [0., 0.0009, 0.], [0., 0., 0.09]])
    # 过程噪声标准偏差(均值为0)
    noiseQ = 2.0
    # 偏航加速度的过程噪声标准偏差(均值为0)
    noiseYaw = 0.3
    # 定义状态转移函数和测量函数，使用numdifftools.Jacobian来计算其对应的雅可比矩阵
    JA_FUN = nd.Jacobian(TransitionFunction)  # 论文公式3.9,omega!=0
    JA_FUN_1 = nd.Jacobian(TransitionFunction_1)  # 论文公式3.9,omega=0
    JH_FUN = nd.Jacobian(MeasurementExpression)  # 论文P18测量矩阵计算

    # 初始化测量
    initMeasure = measureData[0]
    currentStepTime = 0.0
    # 使用测量数据初始化状态
    if initMeasure[0] == 0.0:
        """
        对于激光雷达数据，可以直接将测量到的目标的(x,y) 坐标作为初始(x,y) 其余状态项为0
        """
        print(u"LIDAR初始化!")
        currentStepTime = initMeasure[3]
        statusSpace[0] = initMeasure[1]
        statusSpace[1] = initMeasure[2]
    else:
        """
        对于雷达数据，测量的 ρ , ψ , ρ˙得到目标的坐标(x,y)
        x=ρ*cos (ψ)
        y=ρ*sin (ψ)
        """
        print(u"RADAR初始化!")
        currentStepTime = initMeasure[4]
        statusSpace[0] = initMeasure[1] * np.cos(ControlPsi(initMeasure[2]))
        statusSpace[1] = initMeasure[1] * np.sin(ControlPsi(initMeasure[2]))
    # ======================================================

    # =======================Step10==========================
    for step in range(0, stepLen):
        # ================未结束跟踪序列======================
        if step % 100 == 0:
            print("第" + str(step) + "步EKF跟踪...")
        stepMeasureData = measureData[step]  # 本次测量的数据

        # ===================Step2========================
        if stepMeasureData[0] == 0.0:  # 雷达类型L
            measureX = stepMeasureData[1]
            measureY = stepMeasureData[2]
            z = np.array([[measureX], [measureY]])  # 观测矩阵
            dt = (stepMeasureData[3] - currentStepTime) / 1000000.0  # 时间差
            currentStepTime = stepMeasureData[3]  # 更新当前时间
            # 保存测量值(融合数据)
            measurePositionX.append(measureX)
            measurePositionY.append(measureY)
            # 保存真实值
            truePositionX.append(stepMeasureData[4])
            truePositionY.append(stepMeasureData[5])
            trueVelocityX.append(stepMeasureData[6])
            trueVelocityY.append(stepMeasureData[7])
        else:  # 雷达类型R
            measureRho = stepMeasureData[1]
            measurePsi = stepMeasureData[2]
            measureDotRho = stepMeasureData[3]
            z = np.array([[measureRho], [measurePsi], [measureDotRho]])  # 观测矩阵
            dt = (stepMeasureData[4] - currentStepTime) / 1000000.0  # 时间差
            currentStepTime = stepMeasureData[4]  # 更新当前时间
            # 保存测量值(融合数据)
            measurePositionX.append(measureRho * np.cos(measurePsi))
            measurePositionY.append(measureRho * np.sin(measurePsi))
            # 保存真实值
            truePositionX.append(stepMeasureData[5])
            truePositionY.append(stepMeasureData[6])
            trueVelocityX.append(stepMeasureData[7])
            trueVelocityY.append(stepMeasureData[8])

        # ======================Step3========================
        # 计算当前情况的转移矩阵
        if np.abs(statusSpace[4]) < 0.0001:
            # omega = 0 直线运动
            # ndarray的ravel()向量展平,tolist()转列表
            statusSpace = TransitionFunction_1(statusSpace.ravel().tolist())
            statusSpace[3] = ControlPsi(statusSpace[3])
            JA = JA_FUN_1(statusSpace.ravel().tolist())
        else:
            # omega != 0 转弯运动
            statusSpace = TransitionFunction(statusSpace.ravel().tolist())
            statusSpace[3] = ControlPsi(statusSpace[3])
            JA = JA_FUN(statusSpace.ravel().tolist())
        # ===================================================

        # ===================Step4===========================
        # 计算传递的噪音公式（3.12）~（3.15）
        G = np.zeros([5, 2])
        G[0, 0] = 0.5 * dt * dt * np.cos(statusSpace[3])
        G[1, 0] = 0.5 * dt * dt * np.sin(statusSpace[3])
        G[2, 0] = dt
        G[3, 1] = 0.5 * dt * dt
        G[4, 1] = dt
        Q_v = np.diag([noiseQ * noiseQ, noiseYaw * noiseYaw])
        Q = np.matmul(np.matmul(G, Q_v), G.T)
        # ===================================================

        # ===================Step5===========================
        # 计算一步预测误差方差估计P = APA' + Q
        P = np.matmul(np.matmul(JA, P), JA.T) + Q
        # ===================================================

        # -------------------------------------------------------
        if stepMeasureData[0] == 0.0:
            # Lidar
            # ===================Step6===========================
            # 计算滤波增益矩阵
            K = np.matmul(np.matmul(P, H_lidar.T), np.linalg.inv(np.matmul(np.matmul(H_lidar, P), H_lidar.T) + R_lidar))
            # ===================================================

            # ===================Step7===========================
            # 计算后验状态向量修正
            y = z - np.matmul(H_lidar, statusSpace)
            y[1, 0] = ControlPsi(y[1, 0])  # 角度范围控制
            statusSpace = statusSpace + np.matmul(K, y)
            statusSpace[3] = ControlPsi(statusSpace[3])  # 角度范围控制
            # ===================================================

            # ===================Step8===========================
            # 更新估计误差方差阵
            P = np.matmul((np.eye(5) - np.matmul(K, H_lidar)), P)
            # ===================================================
        else:
            # Radar
            JH = JH_FUN(statusSpace.ravel().tolist())
            # ===================Step6===========================
            # 计算滤波增益矩阵
            K = np.matmul(np.matmul(P, JH.T), np.linalg.inv(np.matmul(np.matmul(JH, P), JH.T) + R_radar))
            # ===================================================

            # ===================Step7===========================
            # 计算后验状态向量修正
            pred = MeasurementExpression(statusSpace.ravel().tolist())
            if np.abs(pred[0, 0]) < 0.0001:  # if rho is 0
                pred[2, 0] = 0
            y = z - pred
            y[1, 0] = ControlPsi(y[1, 0])  # 角度范围控制
            statusSpace = statusSpace + np.matmul(K, y)
            statusSpace[3] = ControlPsi(statusSpace[3])  # 角度范围控制
            # ===================Step8===========================
            # 更新估计误差方差阵
            P = np.matmul((np.eye(5) - np.matmul(K, JH)), P)
            # ===================================================

        # ===================Step9===========================
        # 保存本次滤波数据
        statusSpaceList[:, step] = statusSpace.ravel().tolist()
        EKFPositionX.append(statusSpace[0])
        EKFPositionY.append(statusSpace[1])
        EKFVelocityX.append(np.cos(statusSpace[3]) * statusSpace[2])
        EKFVelocityY.append(np.sin(statusSpace[3]) * statusSpace[2])
    # ===================================================

    # ===================Step11===========================
    # 输出
    print("------------------------------------------------------")
    print("横坐标\t纵坐标\t速度\t偏航角方向\t偏航角速度:")
    for index in range(0, stepLen):
        outData = np.ravel(statusSpaceList[:, index]).tolist()
        print("%e\t%e\t%e\t%e\t%e" % (outData[0], outData[1], outData[2], outData[3], outData[4]))
    print("------------------------------------------------------")

    print("------------------------------------------------------")
    print("位置数据:真实x,滤波x,真实y,滤波y")
    for index in range(0, stepLen):
        print("%e\t%e\t%e\t%e" % (np.ravel(truePositionX).tolist()[index],
                                  np.ravel(EKFPositionX).tolist()[index],
                                  np.ravel(truePositionY).tolist()[index],
                                  np.ravel(EKFPositionY).tolist()[index]))
    print("------------------------------------------------------")

    print("------------------------------------------------------")
    print("速度数据:真实vx,滤波vx,真实vy,滤波vy")
    for index in range(0, stepLen):
        print("%e\t%e\t%e\t%e" % (np.ravel(trueVelocityX).tolist()[index],
                                  np.ravel(EKFVelocityX).tolist()[index],
                                  np.ravel(trueVelocityY).tolist()[index],
                                  np.ravel(EKFVelocityY).tolist()[index]))
    print("------------------------------------------------------")
    # 分析
    print("RMSE:(x,y,vx,vy)")
    print(RMSE(np.array(EKFPositionX), np.array(truePositionX)),
          RMSE(np.array(EKFPositionY), np.array(truePositionY)),
          RMSE(np.array(EKFVelocityX), np.array(trueVelocityX)),
          RMSE(np.array(EKFVelocityY), np.array(trueVelocityY)))
    print("最大误差:(x,y,vx,vy)")
    print(np.max(np.abs(np.array(EKFPositionX).ravel() - np.array(truePositionX).ravel())),
          np.max(np.abs(np.array(EKFPositionY).ravel() - np.array(truePositionY).ravel())),
          np.max(np.abs(np.array(EKFVelocityX).ravel() - np.array(trueVelocityX).ravel())),
          np.max(np.abs(np.array(EKFVelocityY).ravel() - np.array(trueVelocityY).ravel())))
    print("最小误差:(x,y,vx,vy)")
    print(np.min(np.abs(np.array(EKFPositionX).ravel() - np.array(truePositionX).ravel())),
          np.min(np.abs(np.array(EKFPositionY).ravel() - np.array(truePositionY).ravel())),
          np.min(np.abs(np.array(EKFVelocityX).ravel() - np.array(trueVelocityX).ravel())),
          np.min(np.abs(np.array(EKFVelocityY).ravel() - np.array(trueVelocityY).ravel())))
    print("平均误差:(x,y,vx,vy)")
    print(np.mean(np.abs(np.array(EKFPositionX).ravel() - np.array(truePositionX).ravel())),
          np.mean(np.abs(np.array(EKFPositionY).ravel() - np.array(truePositionY).ravel())),
          np.mean(np.abs(np.array(EKFVelocityX).ravel() - np.array(trueVelocityX).ravel())),
          np.mean(np.abs(np.array(EKFVelocityY).ravel() - np.array(trueVelocityY)).ravel()))

    # 画图
    fig = plt.figure(0)     # 生成画板

    # label和title标注的中文支持
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    plt.ion()   # 不暂停绘制
    for i in range(1, stepLen):
        plt.clf()   # 清除画板
        plt.subplot(1, 2, 1)
        plt.plot(EKFPositionX[0:i], EKFPositionY[0:i], 'g.', label=u"滤波值")
        plt.plot(truePositionX[0:i], truePositionY[0:i], 'r.--', label=u"真实值")
        plt.plot(measurePositionX[0:i], measurePositionY[0:i], 'b.', label=u"测量值")
        plt.xlabel(u"X轴坐标")
        plt.ylabel(u"Y轴坐标")
        plt.title(u"位置滤波分析")
        plt.grid(True, linestyle='-.')  # 网格化
        plt.legend()        # 打开label标记

        plt.subplot(1, 2, 2)
        plt.plot(trueVelocityX[0:i], trueVelocityY[0:i], 'r.--', label=u"真实值")
        plt.plot(EKFVelocityX[0:i], EKFVelocityY[0:i], 'g.', label=u"滤波值")
        plt.xlabel(u"X方向速度")
        plt.ylabel(u"Y方向速度")
        plt.title(u"速度滤波分析")
        plt.grid(True, linestyle='-.')  # 网格化
        plt.legend()    # 打开label标记

        if i < stepLen-1:
            plt.pause(0.002)
        else:
            plt.pause(10)    # 结果展示5秒
