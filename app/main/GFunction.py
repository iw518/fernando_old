# -*-coding:utf-8-*-
# -------------------------------------------------------------------------------
# Name:        GFunction
# Purpose:     general function
#
# Author:      Robot of Fernando
#
# Created:     17-06-2015
# Copyright:   (c) Administrator 2015
# Licence:     <GPLV3>
# -------------------------------------------------------------------------------


def AddDate(xDate, num=1):
    newDate = xDate.replace('.', '-').replace('/', '-')
    xlist = newDate.split('-')
    if len(xlist) < 3:
        return newDate
    else:
        year = int(xlist[0])
        month = int(xlist[1])
        day = int(xlist[2]) + num
        if month == 2:
            if day > 28:
                day = 1
                month = month + 1
        elif month in [4, 6, 9, 11]:
            if day > 30:
                day = 1
                month = month + 1
        elif month in [1, 3, 5, 7, 8, 12]:
            if day > 31:
                day = 1
                month = month + 1
            if month > 12:
                month = 1
                year = year + 1
        return '{year}-{month}-{day}'.format(year=year, month=month, day=day)


def Convert2dict(objs):
    '''把对象列表转换为字典列表'''

    obj_arr = []
    for o in objs:
        dict = {}
        '''
        for item in dir(o):
            dict[item] = o.item  #错误o没有‘item’
            dict.update(o.__dict__)
        '''
        for item in dir(o):
            dict[item] = getattr(o, item, 0)
        # print(dir(o))
        print(dict)
        obj_arr.append(dict)
    return obj_arr


def FilterZero(x, convert=False):
    try:
        print(float(x))
    except:
        return '-'
    else:
        if x > 0:
            if convert is True:
                return "%.2f" % x
            else:
                return x
        else:
            return '-'


def Matchlist(x, xlist):
    mylist = []
    if x <= xlist[0][0]:
        return xlist[0][1]
    elif x >= xlist[-1][0]:
        return xlist[-1][1]
    else:
        for i in range(len(xlist)):
            if x == xlist[i][0]:
                return xlist[i][1]
            elif x <= xlist[i + 1][0]:
                for j in range(len(xlist[i][1])):
                    x0 = xlist[i][0]
                    x1 = xlist[i + 1][0]
                    y0 = xlist[i][1][j]
                    y1 = xlist[i + 1][1][j]
                    y = (y1 - y0) / (x1 - x0) * (x - x0) + y0
                    mylist.append(y)
                return mylist
