# -*- coding: utf-8 -*-
# @Time    : 2021/5/11 17:47
# @Author  : FanAnfei
# @Software: PyCharm
# @python  : Python 3.7.9

import datetime
import time


def StrTimeToDatetime(dateStr):
    """
    字符串时间转换为datetime类型
    :param dateStr:字符串时间,要求和%Y-%m-%d %H:%M:%S.%f 转换类型相同;例如"2021-05-11 15:22:18.123456"
    :return: datetime类型时间
    """
    datetimeObj = datetime.datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S.%f")
    return datetimeObj


def StampsToStrTime(stamp):
    """
    使用数字时间戳转化为字符串形式的可读格式时间
    :param stamp: 时间戳    eg:1620723666558161
    :return:时间           eg:2021-05-11 17:01:06.558161
    """
    dataTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(str(stamp)[0:10])))
    if len(str(stamp)[10:]) != 0:
        dataTime = dataTime + '.' + str(stamp)[10:]
    return dataTime


def TimeToStamp16(dateTime):
    """
    使用datetime类型生成16(13)位 高精度时间戳数字
    :param dateTime: 时间     eg:2021-05-11 17:01:06.558161
    :return:时间戳            eg:1620723666558161
    """
    # 10位,时间点相当于从UNIX TIME的纪元时间开始的当年时间编号
    dateStamp = str(int(time.mktime(dateTime.timetuple())))

    # 6位,微秒
    microSecond = str("%06d" % dateTime.microsecond)

    # 3位,微秒
    # microSecond = str("%06d" % datetime_now.microsecond)[0:3]
    dateStamp = dateStamp + microSecond
    return int(dateStamp)


"""
if __name__ == '__main__':

    # -------------------------------------------------------------
    print("-----16位时间转换器------")
    datetime_now = datetime.datetime.now()
    print(datetime_now)

    stamp16 = TimeToStamp16(datetime_now)
    print(type(datetime_now))
    print(type(stamp16))
    print(stamp16)

    decodeTime = StampToTime(stamp16)
    print(type(decodeTime))
    print(decodeTime)

    print("--===============")
    print(StampToTime(1620723666558161))
    print(StampToTime(162072366655816))
    print(StampToTime(16207236665581))
    print(StampToTime(1620723666558))
    print(StampToTime(162072366655))
    print(StampToTime(16207236665))
    print(StampToTime(1620723666))
    print("--===============")

    timeStr = '2021-05-11 15:22:18.12300'
    decodeTime2 = StrTimeToDatetime(timeStr)
    print(type(decodeTime2))
    print(decodeTime2)
    print("-----16位时间转换器------")
    # ---------------------------------------------------------
"""