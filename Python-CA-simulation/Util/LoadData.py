# -*- coding: utf-8 -*-
# @Time    : 2021/5/14 14:44
# @Author  : FanAnfei
# @Software: PyCharm
# @python  : Python 3.7.9


def LoadData(filePath):
    """
    读取数据,并简单处理
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
                rowData.append(float(item))
            dataSet.append(rowData)
        f.close()
    return dataSet
