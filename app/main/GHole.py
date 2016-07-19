# -*-coding:utf-8-*-
# -------------------------------------------------------------------------------
# Name:        GHole
# Purpose:     hole class
#
# Author:      Robot of Fernando
#
# Created:     17-06-2015
# Copyright:   (c) Administrator 2015
# Licence:     <GPLV3>
# -------------------------------------------------------------------------------
from .GLayer import Layers
from .GPoint import Points #方便27行isinstance(xPoint,TESTPOINT)引用
DICT_HoleType={
                "取土孔":(1,101),
                "静探孔":(2,201),
                "标贯孔":(3,202),
                "十字板":(4,203),
                "抽水孔":(5,204),
                "降水孔":(6,205),
                "注水孔":(7,206),
                "旁压孔":(8,207),
                "扁铲孔":(9,208),
                "小孔":(10,102),
                "明浜孔":(11,103),
                "轻便触探":(12,209),
                "波速孔":(13,210),
                "重力触探":(14,211)
                }
DICT_SoilTestType = {
                "含水量、密度":(1,501),
                "液、塑限":(2,502),
                "颗粒分析":(3,503),
                "固结快剪":(4,504),
                "固结压缩":(5,505),
                "渗透系数":(6,601),
                "k0":(7,602),
                "qu":(8,603),                
                "UU":(9,604),
                "CU":(10,605),
                "标贯试验":(21,801)
                }


class Hole:
    def __init__(self, holeType=-1):
        '注意类变量和对象变量的区别'
        self.holeName = ''
        self.holeID = 0
        self.holeType = holeType
        self.elevation = -1.00
        self.waterLevel = -1
        self.__Dep = -1.00
        self._layers = Layers()
        self.testPoints = []
        self.projectNo = ''
        self.testDate = 0
        self._points = Points()

    @property
    def Dep(self):
        return self.__Dep

    @Dep.setter
    def Dep(self, value):
        self.__Dep = value

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        self.__points = value

    @property
    def waterElevation(self):
        if float(self.elevation) and float(self.waterLevel):
            return round(self.elevation - self.waterLevel, 2)

    @property
    def layers(self):
        return self._layers


class BoreHole(Hole):
    def __init__(self):
        Hole.__init__(self, 1)


class CPTHole(Hole):
    def __init__(self):
        Hole.__init__(self, 2)

    @property
    def pss(self):
        return ','.join('%.2f' % (xPoint.testValue) for xPoint in self.points)

    @property
    def Dep(self):
        return len(self.points) / 10
