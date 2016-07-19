# -*-coding:utf-8-*-
# -------------------------------------------------------------------------------
# Name:        GPoint
# Purpose:
#
# Author:      Robot of Fernando
#
# Created:     17-06-2015
# Copyright:   (c) Administrator 2015
# Licence:     <GPLV3>
# -------------------------------------------------------------------------------
import math


class TESTPOINT():
    def __init__(self):
        self.pointID = 0
        self.testDep = 0.0
        self.testValue = 0.0
        self.holeName = ""
        self.soilType = ""
        self.clayContent = -1.0


class PSPOINT(TESTPOINT):
    def __init__(self):
        TESTPOINT.__init__(self)


class BGPOINT(TESTPOINT):

    '注意类变量和对象变量的区别'

    def __init__(self):
        TESTPOINT.__init__(self)
        # startDep=0
        # endDep=0
        # midDep=(startDep+endDep)/2
        self.N = -1.0
        self.testValue = self.N
        self.Wi = -1.0
        self.Di = -1.0
        self.inf = ''

    @property
    def Ncr(self):
        N0 = 7
        BETA = 0.80
        DW = 0.50
        Ncr = -1.0
        ds = self.testDep
        cc = self.clayContent
        if cc >= 10:
            return '-'
        elif cc <= 3:
            Ncr = N0*BETA*(math.log(0.6*ds+1.5)-0.1*DW)
            return round(Ncr, 2)
        else:
            Ncr = N0*BETA*(math.log(0.6*ds+1.5)-0.1*DW)*math.sqrt(3/cc)
            return round(Ncr, 2)

    @property
    def FLei(self):
        if self.Ncr == '-':
            return '-'
        elif self.Ncr <= self.N:
            return '-'
        elif self.Ncr > self.N:
            return round(self.N / self.Ncr, 2)

    @property
    def ILei(self):
        if self.FLei == '-':
            return '-'
        else:
            return round((1 - self.FLei) * self.Di * self.Wi, 2)

    @property
    def LiqueFlag(self):
        if self.Ncr == '-':
            return '否'
        elif self.Ncr <= self.N:
            return '否'
        elif self.Ncr > self.N:
            return '是'


class Points(list):
    def __init__(self):
        list.__init__(self)

    def append(self, item):
        if isinstance(item, TESTPOINT):
            list.append(self, item)

    def filter(self, pointType):
        xList = []
        for xPoint in self:
            if isinstance(xPoint, pointType):
                xList.append(xPoint)
        return xList
