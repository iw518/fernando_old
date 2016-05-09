#-*-coding:utf-8-*-
#-------------------------------------------------------------------------------
# Name:        main
# Purpose:     gen result txt
#
# Author:      Robot of Fernando
#
# Created:     17-06-2015
# Copyright:   (c) Robot of Fernando 2015
# Licence:     The MIT License
#-------------------------------------------------------------------------------
import os
import struct
import math
import string
import copy
from dataset import *
from GHole import *
from GLayer import *
from GPoint import *
from GFunction import *

BASEDIR  =[ "d:/勘探数据/单孔数据/",
            "d:/勘探数据/静力触探数据/",
            "d:/勘探数据/水位表/",
            "d:/勘探数据/统计/",
            "d:/勘探数据/计算书/",
            "d:/勘探数据/其他/",
            "d:/勘探数据/project/"]
DATABASE ='shmged'
#SILTYS=['砂质粉土','粉砂','细砂','粉细砂','中砂','粗砂','中粗砂','砾砂']

#  若用os.path.dirname(x)来查找上级目录，并创建父目录，有时候查找不到，具体原因不明
#  os.mkdir(x)用来创建一层目录，os.makedirs(x)用来创建多层目录
for x in BASEDIR:
    if not os.path.exists(x):
        os.makedirs(x)
#仔细思考这个函数的写法,非常有用
def autoDate(testDate,MaxNofHole,MaxTotalDep,holelist):
    N0=0
    TotalDep=0
    for i in range(len(holelist)):
        TotalDep=TotalDep+holelist[i].Dep
        if i-N0<MaxNofHole and TotalDep<=MaxTotalDep:
            holelist[i].testDate=AddDate(testDate,0)
        else:
            N0=i
            TotalDep=holelist[N0].Dep
            testDate=AddDate(testDate,1)
            holelist[i].testDate=AddDate(testDate,0)

def CollectBgPoints2Hole(projectNo):
    sql_str=("SELECT soilhole.soil_holeNo, pmbg.bgpoint,(pmbg.startpos+pmbg.endpos)/2, pmbg.n635, grain.k_0005, \
                    'soilType'=(CASE \
                                    WHEN grain.k025_0074>50 THEN '粉砂' \
                                    WHEN grain.k_0005<10 THEN '砂质粉土' \
                                    WHEN grain.k_0005<15 THEN '粘质粉土' \
                                    ELSE '粉质粘土' \
                                END) \
                FROM ((pmbg INNER JOIN base ON pmbg.project_count = base.project_count) \
                    INNER JOIN soilhole \
                            ON (pmbg.hnumber = soilhole.hnumber) AND (base.project_count = soilhole.project_count)) \
                    INNER JOIN (grain RIGHT JOIN main ON grain.tnumber = main.tnumber) \
                            ON (pmbg.startpos = main.stardep) AND (soilhole.soil_hnumber = main.soil_hnumber)\
                WHERE (((base.project_name)='%s')) AND (pmbg.startpos<20) \
                ORDER BY Len(soilhole.soil_holeNo), soilhole.soil_holeNo, Len(pmbg.bgpoint), pmbg.bgpoint"\
                %(projectNo))
    ms = MSSQL(DATABASE)
    sqlList = ms.ExecQuery(sql_str)

    '采集所有的bgpoint'
    BGPOINTList=[]
    for (holeNo,bgPoint,testDep,N635,clayContent,soilType) in sqlList:
        xPoint=BGPOINT()
        xPoint.name=bgPoint.encode('latin-1').decode('gbk')
        xPoint.holeName=holeNo.encode('latin-1').decode('gbk')
        xPoint.testDep=testDep
        xPoint.soilType=soilType.encode('latin-1').decode('gbk')
        xPoint.clayContent=clayContent
        xPoint.N=N635
        BGPOINTList.append(xPoint)

    '将采集的bgpoint加入到hole中'
    holeList=HoleAndLayer(projectNo)
    for xHole in holeList:
        for xPoint in BGPOINTList:
            '注意限制条件'
            if xPoint.holeName==xHole.holeName:
                xHole.AddPoint(xPoint)
    return holeList

def ResLiquefaction(projectNo):
    #siltLayers=FindSiltLayers(FindLayers(projectNo))
    holeList=FindLiqueHole(projectNo)
    caculatedHoleCount=len(holeList)
    caculatedPointCount=0
    erroCount=0
    liqueList=[]
    for xHole in holeList:
        for xLayer in xHole.layers:
            '查找该土层是否是砂土或砂质粉土层，若是，则进行判别，否则跳过判别，继续下一个点的计算'
            if True:
                for i in range(len(xLayer.BgPoints)):
                    xPoint=xLayer.BgPoints[i]
                    caculatedPointCount+=1
                    #如果该点是判别层中的第一个点，则代表厚度的上半部分(delta1)的起始位置取判别层的层顶深度
                    if i==0:
                        priorTestDep=xLayer.startDep
                        delta1=xPoint.testDep-priorTestDep
                    #如果该点不是判别层中的第一个点，则代表厚度的上半部分(delta1)的起始位置取其上一点的试验深度
                    else:
                        priorTestDep=xLayer.BgPoints[i-1].testDep
                        delta1=(xPoint.testDep-priorTestDep)/2
                    #如果该点是判别层中的最后一个点，则代表厚度的下半部分(delta2)的结束位置取判别层的层底深度与20m的最小值
                    if i==len(xLayer.BgPoints)-1:
                        nextTestDep=min(xLayer.endDep,20)
                        delta2=(nextTestDep-xPoint.testDep)
                    #如果该点不是判别层中的最后一个点，则代表厚度的下半部分(delta2)的结束位置取其下一点的试验深度
                    else:
                        nextTestDep=xLayer.BgPoints[i+1].testDep
                        delta2=(nextTestDep-xPoint.testDep)/2
                    #midH为代表厚度的中点
                    #print('%s\t%s\t%.2f\t%.2f'%(xHole.holeName,xPoint.name,priorTestDep,nextTestDep))
                    midH=(nextTestDep+priorTestDep)/2
                    xPoint.Di=delta1+delta2
                    xPoint.Wi=CalcWi(midH)
                    '注意python中float小数精度的问题,即使是1.50,float可能显示的也是1.5000062'
                    if round(xPoint.Di,4)>1.5:
                        xPoint.inf='%s%.2f'%('erro',xPoint.Di)
                        erroCount+=1
                    else:
                    	xPoint.inf=''
                    if xPoint.clayContent is None:
                        liqueList.append((xHole.holeName,
                             xLayer.layerNo,
                             '%.2f'%(xPoint.testDep),
                             '',
                             xPoint.N,
                             '否',
                             '-',
                             '-',
                             '%.2f'%(xPoint.Di),
                             '',
                             '',
                             xPoint.inf))
                    else:
                        liqueList.append((xHole.holeName,
                             xLayer.layerNo,
                             '%.2f'%(xPoint.testDep),
                             '%.2f'%(xPoint.clayContent),
                             xPoint.N,
                             ('%.2f'%(xPoint.Ncr) if type(xPoint.Ncr) is float else xPoint.Ncr),
                             xPoint.LiqueFlag,
                             xPoint.FLei,
                             '%.2f'%(xPoint.Di),
                             '%.2f'%(xPoint.Wi),
                             xPoint.ILei,
                             xPoint.inf))
    return liqueList,caculatedHoleCount,caculatedPointCount,erroCount

def ReceiveHoleLayer(projectNo,holeType=-1):
    if holeType==-1:
        sql_str=("SELECT pholeatt.holeno, zp93.dep, zp93.norder \
                FROM (zp93 INNER JOIN base ON zp93.project_count = base.project_count) \
                        INNER JOIN pholeatt ON zp93.hnumber = pholeatt.hnumber \
                WHERE base.project_name ='%s'\
                ORDER BY pholeatt.attribute, \
                            zp93.norder, \
                            LEN(pholeatt.holeno), \
                            pholeatt.holeno"%(projectNo))
    else:
        sql_str=("SELECT pholeatt.holeno, zp93.dep, zp93.norder \
                FROM (zp93 INNER JOIN base ON zp93.project_count = base.project_count) \
                        INNER JOIN pholeatt ON zp93.hnumber = pholeatt.hnumber \
                WHERE base.project_name ='%s' and pholeatt.attribute='%d'\
                ORDER BY zp93.norder,\
                            LEN(pholeatt.holeno), \
                            pholeatt.holeno"%(projectNo,holeType))
    #必须按照norder排序,不能按照zp93.anumber排序
    ms = MSSQL(DATABASE)
    sqlList = ms.ExecQuery(sql_str)
    layers=FindLayers(projectNo)
    holeList=ReceiveHoleBasicInf(projectNo,holeType)
    L1=len(sqlList)
    for j in range(len(holeList)):
        xHole=holeList[j]
        for i in range(0,L1):
            if sqlList[i][0].encode('latin-1').decode('gbk')==xHole.holeName:
                layerOrder=sqlList[i][2]
                xLayer=copy.deepcopy(layers[layerOrder-1])
                xLayer.endDep=sqlList[i][1]
                if layerOrder==1:
                    xLayer.startDep=0.0
                    xLayer.endDep=sqlList[i][1]
                elif xLayer.endDep==0.0:
                    xLayer.startDep=xHole.layers[-1].endDep
                    xLayer.endDep=xHole.layers[-1].endDep
                else:
                    xLayer.startDep=xHole.layers[-1].endDep
                    xLayer.endDep=sqlList[i][1]
                xHole.layers.append(xLayer)
        else:
            xLayer=copy.deepcopy(layers[len(xHole.layers)])
            xLayer.startDep=xHole.layers[-1].endDep
            xLayer.endDep=xHole.Dep
            xHole.layers.append(xLayer)
##    if True:
##    	for xHole in holeList:
##    		print(xHole.holeName)
##    		for xLayer in xHole.layers:
##    			print('%s\t%s\t%.2f\t%.2f'%(xLayer.layerNo,xLayer.layerName,xLayer.startDep,xLayer.endDep))
    return holeList

###查找每个项目所含钻孔及其孔深，返回list[xhole,....],hole主要组成为hole.holeName,hole.Dep
def ReceiveHoleBasicInf(projectNo,holeType=-1):
    if holeType==-1:
        sql_str=("SELECT pholeatt.holeno,pholeatt.height,pholeatt.depth,pholeatt.waterlevel,pholeatt.attribute \
        FROM pholeatt INNER JOIN base ON pholeatt.project_count = base.project_count \
        WHERE (base.project_name='%s') \
        ORDER BY pholeatt.attribute, pholeatt.hole_order, len(pholeatt.holeno), pholeatt.holeno"%(projectNo))
    else:
        sql_str=("SELECT pholeatt.holeno,pholeatt.height,pholeatt.depth,pholeatt.waterlevel,pholeatt.attribute \
        FROM pholeatt INNER JOIN base ON pholeatt.project_count = base.project_count \
        WHERE (base.project_name='%s') AND (pholeatt.attribute='%d')\
        ORDER BY pholeatt.hole_order, len(pholeatt.holeno), pholeatt.holeno"%(projectNo,holeType))
    ms = MSSQL(DATABASE)
    sqlList = ms.ExecQuery(sql_str)
    holeList=[]
    for(holeNo,elevation,holeDepth,waterLevel,holeType) in sqlList:
        xHole=Hole()
        xHole.holeName=holeNo.encode('latin-1').decode('gbk')
        xHole.projectNo=projectNo
        xHole.elevation=elevation
        xHole.Dep=holeDepth
        xHole.waterLevel=waterLevel
        xHole.holeType=holeType
        holeList.append(xHole)
        ##if True:print('%s\t%.2f'%(xHole.holeName,xHole.Dep))
    return holeList


###查找每个项目所含钻孔，返回list[xhole,....],hole主要组成为findholeanddep的属性及layers属性,其中layer成分由findlayers明确
def HoleAndLayer(projectNo):
    sql_str=("SELECT soilhole.soil_holeNo, zp93.dep, zp93.norder, zp93.hnumber \
            FROM (zp93 INNER JOIN base ON zp93.project_count = base.project_count) \
                    INNER JOIN soilhole ON zp93.hnumber = soilhole.hnumber \
            WHERE base.project_name ='%s' \
            ORDER BY LEN(soilhole.soil_holeNo), \
                        soilhole.soil_holeNo, \
                        zp93.norder"%(projectNo))
    #必须按照norder排序,不能按照zp93.anumber排序
    ms = MSSQL(DATABASE)
    sqlList = ms.ExecQuery(sql_str)
    layers=FindLayers(projectNo)
    holeList=FindHoleAndDep(projectNo)
    L1=len(sqlList)
    for j in range(len(holeList)):
        xHole=holeList[j]
        for i in range(0,L1):
            if sqlList[i][0].encode('latin-1').decode('gbk')==xHole.holeName:
                layerOrder=sqlList[i][2]
                xLayer=copy.deepcopy(layers[layerOrder-1])
                xLayer.endDep=sqlList[i][1]
                if layerOrder==1:
                    xLayer.startDep=0.0
                    xLayer.endDep=sqlList[i][1]
                elif xLayer.endDep==0.0:
                    xLayer.startDep=xHole.layers[-1].endDep
                    xLayer.endDep=xHole.layers[-1].endDep
                else:
                    xLayer.startDep=xHole.layers[-1].endDep
                    xLayer.endDep=sqlList[i][1]
                xHole.layers.append(xLayer)
        else:
            xLayer=copy.deepcopy(layers[len(xHole.layers)])
            xLayer.startDep=xHole.layers[-1].endDep
            xLayer.endDep=xHole.Dep
            xHole.layers.append(xLayer)
    return holeList

def FindLiqueHole(projectNo):
    holeList=CollectBgPoints2Hole(projectNo)
    for xHole in holeList:
        pointL=len(xHole.bgPoints)
        if pointL==0:
        	continue
        for i in range(0,pointL):
            xPoint=xHole.bgPoints[i]
            #查找标贯点对应的土层
            xLayer=FindLayerOfPoint(xPoint,xHole)
            xLayer.AddBgPoint(xPoint)
    LiqueHoleList=[]
    siltLayers=FindSiltLayers(FindLayers(projectNo))
    for xHole in holeList:
        for xLayer in xHole.layers:
            if (xLayer.layerNo in [item.layerNo for item in siltLayers]) and len(xLayer.BgPoints)>0:
                LiqueHoleList.append(xHole)
                break
    return LiqueHoleList

###查找每个项目所含钻孔及其孔深，返回list[xhole,....],hole主要组成为hole.holeName,hole.Dep
def FindHoleAndDep(projectNo):
    sql_str=("SELECT soilhole.soil_holeNo, Max(main.enddep) \
    FROM (soilhole INNER JOIN main ON soilhole.soil_hnumber = main.soil_hnumber)\
    INNER JOIN base ON soilhole.project_count = base.project_count\
    GROUP BY soilhole.hole_order, soilhole.soil_holeNo, base.project_name\
    HAVING base.project_name='%s'\
    ORDER BY len(soilhole.soil_holeNo), soilhole.soil_holeNo, soilhole.hole_order"%(projectNo))
    ms = MSSQL(DATABASE)
    sqlList = ms.ExecQuery(sql_str)
    holeList=[]
    for(holeNo,holeDepth) in sqlList:
        xHole=BGHOLE()
        xHole.holeName=holeNo.encode('latin-1').decode('gbk')
        xHole.projectNo=projectNo
        xHole.Dep=holeDepth
        holeList.append(xHole)
    return holeList

def FindLayerOfPoint(xPoint,xHole):
	for xLayer in xHole.layers:
		if (xLayer.endDep-xLayer.startDep)>0:
			if (xPoint.testDep>xLayer.startDep) and (xPoint.testDep<xLayer.endDep):
				return xLayer
def FindLayers(projectNo):
    '此处采用right join，为了防止部分地层地质时代为空'
    sql_str=("SELECT pmlayer.layerno, pmlayer.layername, geologic_age.geologic_age \
            FROM geologic_age \
            RIGHT JOIN (pmlayer INNER JOIN base ON pmlayer.project_count = base.project_count) \
            ON geologic_age.anumber = pmlayer.anumber \
            WHERE base.project_name='%s' \
            ORDER BY pmlayer.layerorder"%(projectNo))
    ms = MSSQL(DATABASE)
    sqlList = ms.ExecQuery(sql_str)
    layers=[]
    count=0
    for (layerNo,layerName,layerAge,) in sqlList:
    	count+=1
    	xLayer=Layer()
    	xLayer.layerOrder=count
    	xLayer.layerNo=layerNo.encode('latin-1').decode('gbk')
    	xLayer.layerName=layerName.encode('latin-1').decode('gbk')
    	xLayer.layerAge=layerAge
    	layers.append(xLayer)
    #print("本工程地基土可划分为%d个工程地质层。"%(count))
    return layers

def ExportLayers_Stat(projectNo,d=1.0,wd=0.5):
    '此处采用right join，为了防止部分地层地质时代为空'
    sql_str=("SELECT pmlayer.layerno, pmlayer.layername, \
            '粘聚力'=Sum(Case titemdata.itemCode when 'CON_C' THEN titemdata.iavg ELSE 0 END), \
            '摩擦角'=Sum(Case titemdata.itemCode when 'CON_F' THEN titemdata.iavg ELSE 0 END), \
            'PS值'=Sum(Case titemdata.itemCode when 'PS1' THEN titemdata.iavg ELSE 0 END), \
            '重度'=Sum(Case titemdata.itemCode when 'DENSITY' THEN titemdata.iavg ELSE 0 END) \
            FROM (titemdata INNER JOIN pmlayer ON \
            titemdata.anumber = pmlayer.anumber) INNER JOIN base ON \
            titemdata.project_count = base.project_count \
            WHERE (base.project_name)='%s' \
            GROUP BY pmlayer.layerorder, pmlayer.layerno, pmlayer.layername"%(projectNo))
    ms = MSSQL(DATABASE)
    sqlList = ms.ExecQuery(sql_str)
    layers=[]
    for (layerNo,layerName,CON_C,CON_F,Ps1,DENSITY) in sqlList:
        xLayer=Layer_Stats(d,wd)
        xLayer.layerNo=layerNo.encode('latin-1').decode('gbk')
        xLayer.layerName=layerName.encode('latin-1').decode('gbk')
        xLayer.CON_C=CON_C
        xLayer.CON_F=CON_F
        xLayer.AVG_Ps=round(Ps1,2)
        xLayer.DENSITY=DENSITY
        layers.append(xLayer)
    return layers

def FindSiltLayers(layers):
    siltLayers=[]
    for xLayer in layers:
        #此处采用right join，为了防止部分地层地质时代为空
        if (xLayer.layerAge is None):
            print('地质时代未输入，请补齐')
        elif (xLayer.layerAge.startswith('Q4') and ('砂' in xLayer.layerName.split('夹')[0])):
            siltLayers.append(xLayer)
    return siltLayers

def FindSiltLayers2(projectNo):
    siltLayers=[]
    layers=FindLayers(projectNo)
    for xLayer in layers:
        #此处采用right join，为了防止部分地层地质时代为空
        if (xLayer.layerAge is None):
            print('地质时代未输入，请补齐')
        elif (xLayer.layerAge.startswith('Q4') and ('砂' in xLayer.layerName.split('夹')[0])):
            siltLayers.append(xLayer)
            #print('本工程的砂土层或砂质粉土层为：%s\t%s\t'%(xLayer.layerNo,xLayer.layerName))
    return siltLayers

def CalcWi(midDep):
    if midDep<=5:
        return 10
    elif midDep==20:
        return 0
    else:
        return-2/3*midDep+40/3
def FindCPT(projectNo):
    sql_str=("SELECT pholeatt.holeno, tpfs.qc_fs \
            FROM (tpfs INNER JOIN base \
            ON tpfs.project_count = base.project_count) \
            INNER JOIN pholeatt \
            ON base.project_count = pholeatt.project_count \
            WHERE (base.project_name='%s') \
            AND (pholeatt.hnumber=tpfs.hnumber) \
            AND (pholeatt.attribute=2) \
            ORDER BY LEN(pholeatt.holeno),pholeatt.holeno,pholeatt.hnumber"%(projectNo))
    ms=MSSQL(DATABASE)
    sqlList=ms.ExecQuery(sql_str)
    holeList=[]
    for item in sqlList:
        xHole=CPTHole()
        xHole.holeName=item[0].encode('latin-1').decode('gbk')
        xHole.projectNo=projectNo
        buff=item[1]
        buff_len=len(buff)
        for x in range(0,buff_len,2):
            ps=(struct.unpack('H',buff[x:x+2])[0])/100
            xPoint=PSPOINT()
            xPoint.testDep=round(x/2*0.1+0.1,2)
            xPoint.testValue=round(ps,2)
            xHole.AddPoint(xPoint)
        holeList.append(xHole)
    return holeList
#====================================================#
def ExportPs(projectNo):
    sql_str=("SELECT pholeatt.holeno, tpfs.qc_fs \
            FROM (tpfs INNER JOIN base \
            ON tpfs.project_count = base.project_count) \
            INNER JOIN pholeatt \
            ON base.project_count = pholeatt.project_count \
            WHERE (base.project_name='%s') \
            AND (pholeatt.hnumber=tpfs.hnumber) \
            AND (pholeatt.attribute=2) \
            ORDER BY pholeatt.hnumber"%(projectNo))

    ms=MSSQL(DATABASE)
    sqlList=ms.ExecQuery(sql_str)

    # cur.fetchone()是tuple格式，因为pymssql默认查询多个字段
    # print(type(cur.fetchone()))
    # buff=cur.fetchone()[1]
    for y in sqlList:
        buff=y[1]
        buff_len=len(buff)
        str1=''
        for x in range(0,buff_len,2):
            ps=(struct.unpack('H',buff[x:x+2])[0])/100
            ps="%.2f\n"%(ps)
            str1+=ps
        file_dir= os.path.join(BASEDIR[1],projectNo+'--'+y[0]+".txt")
        f=open(file_dir,'w')
        print(str1,file=f)
        f.close()

def ResWater(projectNo):
    sql_str=("SELECT pholeatt.holeno as 孔号, \
    pholeatt.height as 标高, pholeatt.waterlevel as 水位 \
    FROM pholeatt INNER JOIN base ON pholeatt.project_count = base.project_count \
    WHERE (base.project_name='%s') AND (pholeatt.attribute=1) ORDER BY pholeatt.hole_order"%(projectNo))

    ms = MSSQL(DATABASE)
    sqlList = ms.ExecQuery(sql_str)
    holeList=[]
    for (holeNo,height,waterLevel) in sqlList:
        xHole=BoreHole()
        xHole.holeName=holeNo.encode('latin-1').decode('gbk')
        xHole.projectNo=projectNo
        xHole.elevation=height
        xHole.waterLevel=waterLevel
        if (type(height) is float) and (type(waterLevel) is float):holeList.append(xHole)
##    str1=''##
##    '计算书说明'
##    str1+='<hr />'
##    str1+='<P />'
##    str1+='<P>'+'&nbsp;'*35+'地下水位计算书'+'&nbsp;'*35+'</P>'
##    str1+='<P />'
##    str1+='<hr />'
##    str1+='<P>'+'工程编号:'+'%s'%(projectNo)+'</P>'
##    cnt=len(holeList)
##    factor=GroupTotal(cnt)[0]
##    rank=GroupTotal(cnt)[1]
##    for x in range(rank):
##        start=x*factor
##        if ((x+1)*factor)<=cnt:
##            end=(x+1)*factor
##        else:
##            end=cnt
##        '设置字符宽度为5,此处sep用四个空格来代替\t，估计是一旦字符宽度大于4，则\t会小于4'
##        str1+='<P>'+' '.join('%5s'%(xHole.holeName) for xHole in holeList[start:end])+'</P>'
##        str1+='<P>'+' '.join('%5.2f'%(xHole.waterLevel) for xHole in holeList[start:end])+'</P>'
##        str1+='<P>'+' '.join('%+5.2f'%(xHole.waterElevation) for xHole in holeList[start:end])+'</P>'
##    str1+='<P>'+'工程审核人：'+'\t'*3+'工程负责人：'+'\t'*3+'计算人： Robot of fernando'+'</P>'
##    return str1
    return holeList

## 转置分列
'默认每张水位表最大可容纳8列'
'  1,2,3,.......................1factor'
'  .............................2factor'
'  ....................................'
'  ....................................'
'  (rank-1)factor+1,..........rank*factor'
def GroupTotal(total,factor=8):
    rank=math.floor(total/factor)
    remainder=total%factor
    if remainder==0:
        rank=rank
    else:
        rank=rank+1
        factor=math.ceil(total/rank)
    return (factor,rank)