#-*-coding:utf-8-*-
#-------------------------------------------------------------------------------
# Name:        GHole
# Purpose:
#
# Author:      Robot of Fernando
#
# Created:     17-06-2015
# Copyright:   (c) Administrator 2015
# Licence:     <GPLV3>
#-------------------------------------------------------------------------------
import math
from GPoint import TESTPOINT #方便27行isinstance(xPoint,TESTPOINT)引用
class Hole:
    def __init__(self,holeType=-1):
        '注意类变量和对象变量的区别'
        self.holeName=''
        self.holeID=0
        self.holeType=holeType
        self.elevation=-1.00
        self.waterLevel=-1
        self.__Dep=-1.00
        self.layers=[]
        self.testPoints=[]
        self.projectNo=''
        self.testDate=0
    @property
    def Dep(self):
        return self.__Dep
    @Dep.setter
    def Dep(self,value):
        self.__Dep=value
    @property
    def waterElevation(self):
        return self.elevation-self.waterLevel
    def AddPoint(self,xPoint):
        '判断子类对象是否属于父类用isinstance,'
        if isinstance(xPoint,TESTPOINT):
            self.testPoints.append(xPoint)

class BoreHole(Hole):
    def __init__(self):
        Hole.__init__(self,1)
        self.soilPoints=[]
        self.bgPoints=[]
    def AddPoint(self,xPoint):
        if type(xPoint) is SoilPoint:
            self.soilPoints.append(xPoint)
        elif type(xPoint) is BgPoint:
            self.bgPoints.append(xPoint)

class BGHOLE(Hole):
    '注意类变量和对象变量的区别'
    def __init__(self):
        Hole.__init__(self,1)
        self.bgPoints=[]
    def AddPoint(self,bgPoint):
        self.bgPoints.append(bgPoint)
class CPTHole(Hole):
    def __init__(self):
        Hole.__init__(self,2)
    @property
    def pss(self):
        return ','.join('%.2f'%(xPoint.testValue) for xPoint in self.testPoints)
    @property
    def Dep(self):
        return len(self.testPoints)/10
