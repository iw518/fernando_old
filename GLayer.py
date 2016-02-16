#-*-coding:utf-8-*-
#-------------------------------------------------------------------------------
# Name:        GLayer
# Purpose:
#
# Author:      Robot of Fernando
#
# Created:     17-06-2015
# Copyright:   (c) Administrator 2015
# Licence:     <GPLV3>
#-------------------------------------------------------------------------------
import math,GFunction
DICT_FK_PS={'粘土':(68,0.135,1.5,1.1,0),
            '淤泥质':(58,0.125,0.8,1.0,0),
            '粉土':(72,0.090,2.5,1.3,0.3),
            '素填土':(54,0.108,1.5,1.1,0),
            '冲填土':(40,0.080,1.0,1.0,0),
            '吹填土':(40,0.080,1.0,1.0,0),
            '砂':(72,0.090,2.5,1.3,0.3)
            }
F_FACTOR=[(16,(0.90,)),(18,(1.03,)),(20,(1.17,)),(22,(1.30,)),(23,(1.37,)),(24,(1.44,)),(25,(1.50,))]
FD_FACTOR=[(0,(0.00,2.00,5.14)),
       (1,(0.01,2.00,5.38)),
       (2,(0.01,2.00,5.63)),
       (3,(0.02,2.00,5.90)),
       (4,(0.05,2.00,6.19)),
       (5,(0.07,2.00,6.49)),
       (6,(0.11,2.00,6.81)),
       (7,(0.16,2.00,7.16)),
       (8,(0.22,2.00,7.53)),
       (9,(0.30,2.00,7.92)),
       (10,(0.39,2.00,8.35)),
       (11,(0.50,2.07,8.80)),
       (12,(0.63,2.09,9.28)),
       (13,(0.78,2.12,9.81)),
       (14,(0.97,2.15,10.37)),
       (15,(1.18,2.18,10.98)),
       (16,(1.43,2.22,11.63)),
       (17,(1.73,2.26,12.34)),
       (18,(2.08,2.30,13.10)),
       (19,(2.48,2.35,13.93)),
       (20,(2.95,2.40,14.83)),
       (21,(3.50,2.46,15.82)),
       (22,(4.13,2.52,16.88)),
       (23,(4.88,2.58,18.05)),
       (24,(5.74,2.65,19.32)),
       (25,(6.76,2.72,20.72))
]

class Layer:
    def __init__(self):
        self.layerNo=''
        self.layerName=''
        self.layerOrder=-1
        self.startDep=-1.0
        self.endDep=-1.0
        self.holeName=''
        self.BgPoints=[]
        self.SoilPoints=[]
    def AddBgPoint(self,xPoint):
        self.BgPoints.append(xPoint)
    def AddSoilPoint(self,xPoint):
        self.SoilPoints.append(xPoint)

class Layer_Stats(Layer):
    def __init__(self):
        Layer.__init__(self)
        self.CON_C=0.0
        #self.CON_Ck=0.0
        self.CON_F=0.0
        #self.CON_Fk=0.0
        self.__AVG_Ps=0.0
        self.DENSITY=0.0
    @property
    def AVG_Ps(self):
        if self.__AVG_Ps<=0:
            return '-'
        else:
            return round(self.__AVG_Ps,2)
    @AVG_Ps.setter
    def AVG_Ps(self,value):
        self.__AVG_Ps=value

    @property
    def CON_F_toStr(self):
        if self.CON_F<=0:
            return '-'
        else:
            F100=int(self.CON_F*100)%10 #百分位
            F10=int(self.CON_F*10)%10  #十分位
            F=int(self.CON_F)
            if (self.CON_F-F)<0.25:
                return '%.1f'%(F)
            elif (self.CON_F-F)>=0.25 and (self.CON_F-F)<0.75:
                return '%.1f'%(F+0.5)
            else:
                return '%.1f'%(F+1)
    @property
    def CON_C_toStr(self):
        if self.CON_C<=0:
            return '-'
        else:
            C10=int(self.CON_C*10)%10
            C0=int(self.CON_C)%10
            C=int(self.CON_C)
            if (self.CON_C-C)<0.5:
                return '%.0f'%(C)
            else:
                return '%.0f'%(C+1)

    @property
    def Ps_Fak(self):
        if self.AVG_Ps=='-':
            return '-'
        else:
            return round(self.CalcPsBearingCapacity(),2)
    @property
    def Soil_Fak(self):
        if self.DENSITY=='-':
            return '-'
        else:
            return round(self.CalcSoilBearingCapacity(),2)


    def Avg2Std(AVG,cv,n):
        rs=1-(1.704/math.sqrt(n)+4.678/n/n)*cv
        return AVG*rs

    def CalcPsBearingCapacity(self):
        fd=0
        D=1.0
        B=3.0
        for (k,v) in DICT_FK_PS.items():
            if k in self.layerName.split('夹')[0]:
                fk=v[0]+v[1]*min(self.AVG_Ps,v[2])*1000
                fd=0.5*fk+v[3]*13*(D-0.5)+v[4]*8*(B-3)
                break
        return fd

    def CalcSoilBearingCapacity(self):

        d=1.0
        b=1.5
        Tr=1.0
        Tc=1.0
        Tq=1.0

        # 勘察软件水的重度取10,此处为取9.8
        r=(self.DENSITY-1)*9.8
        r0=self.DENSITY*0.5*9.8+r*0.5

        LAMD=0.8
        rc=2.7
        rf=1.2
        #地基基础设计规范5.2.3条，剪切指标标准值取固快峰值强度平均值
        CON_Ck=self.CON_C
        CON_Fk=self.CON_F

        CON_Cd=LAMD*CON_Ck/rc
        CON_Fd=LAMD*CON_Fk/rf
        f=GFunction.Matchlist(CON_Fd,F_FACTOR)[0]
        Nr=(GFunction.Matchlist(CON_Fd,FD_FACTOR))[0]
        Nq=(GFunction.Matchlist(CON_Fd,FD_FACTOR))[1]
        Nc=(GFunction.Matchlist(CON_Fd,FD_FACTOR))[2]
        fd=0.5*f*Nr*Tr*r*b+f*Nc*Tc*CON_Cd+Nq*Tq*r0*d
        return fd

    @property
    def Fak(self):
        if self.AVG_Ps=='-' and self.DENSITY<=0:
            return '-'
        elif self.AVG_Ps=='-' and self.DENSITY>0:
            return (self.Soil_Fak/5)*5
        elif self.AVG_Ps!='-' and self.DENSITY<=0:
            return (self.Ps_Fak/5)*5
        else:
            if ('粉土' in self.layerName.split('夹')[0]) or ('砂' in self.layerName.split('夹')[0]):
                return (int((self.Ps_Fak+self.Soil_Fak)/2/5))*5
            else:
                return (int((min(self.Ps_Fak,self.Soil_Fak)*0.75+max(self.Ps_Fak,self.Soil_Fak)*0.25)/5))*5