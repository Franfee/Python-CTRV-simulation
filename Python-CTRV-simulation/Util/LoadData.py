# -*- coding: utf-8 -*-
# @Time    : 2021/5/14 14:44
# @Author  : FanAnfei
# @Software: PyCharm
# @python  : Python 3.7.9


def LoadData(filePath):
    """
    读取数据,并简单处理
    该数据集包含了追踪目标的LIDAR和RADAR的测量值，以及测量的时间点，同时为了验证我们追踪目标的精度，该数据还包含了追踪目标的真实坐标。

    第0列表示测量数据来自LIDAR还是RADAR
    LIDAR:
        第1,2列表示测量的目标(x,y)
        第3列表示测量的时间戳
        第4,5,6,7表示真实的(x, y, v_x, v_y)
    RADAR:
        测量的前三列(1-3列)是(ρ,ψ,ρ˙),其余列的数据的意义和LIDAR一样
        第4列表示测量的时间戳,第5,6,7,8表示真实的(x, y, v_x, v_y)
    :param filePath: 数据路径
    :return: 全部数据
    """
    dataSet = []
    with open(filePath, 'rb') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip(b'\n').split(b'\t')   # 清除换行符,以制表符分割数据
            rowData = []
            for index, item in enumerate(line):
                if index == 0:
                    if item.decode('utf-8') == 'L':
                        rowData.append(0.0)     # 保证列表中数据类型相同
                    else:
                        rowData.append(1.0)     # 保证列表中数据类型相同
                else:
                    rowData.append(float(item))
            dataSet.append(rowData)
        f.close()
    return dataSet
