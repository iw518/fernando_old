# -*-coding:utf-8-*-
# -------------------------------------------------------------------------
# Name:        statisticsxapp
# Purpose:     start web
#
# Author:      Robot of Fernando
#
# Created:     29-05-2016
# Copyright:   (c) Robot of Fernando 2015
# Licence:     The MIT License
# -------------------------------------------------------------------------

from flask import Blueprint, render_template, request, url_for, jsonify
from maingui import *
from auth import *

analysis = Blueprint('analysis', __name__)

@analysis.route('/cptAnalysis', methods=['POST', 'GET'])
def cptAnalysis():
    projectNo = request.args.get('projectNo')
    holeDict = FindCPT(projectNo)
    holelist=[]
    holelist2=[]
    for holeName, xHole in holeDict.items():
        holelist.append(xHole)
    holeDict = ReceiveHoleLayer(projectNo, 2)
    for holeName, xHole in holeDict.items():
        holelist2.append(xHole)
    if request.method == 'GET':
        layer_hole_ps_list = []
        for i in range(0, len(FindLayers(projectNo))):
            hole_ps_list = []
            for xHole in holelist2:
                for yHole in holelist:
                    SumPs = 0
                    if xHole.holeName == yHole.holeName:
                        if i >= len(xHole.layers):
                            hole_ps_list.append((xHole.holeName, 0))
                        else:
                            xLayer = xHole.layers[i]
                            for testPoint in yHole.points:
                                if testPoint.testDep > round(xLayer.startDep, 2) and testPoint.testDep <= round(xLayer.endDep, 2):  # 注意小数位数不等也可能导致不相等，情况允许时，应该调整layer函数的位数
                                    SumPs = SumPs + testPoint.testValue
                            if xLayer.endDep - xLayer.startDep == 0:
                                hole_ps_list.append([xHole.holeName, 0])
                            else:
                                hole_ps_list.append([xHole.holeName,
                                                     round(SumPs / (xLayer.endDep - xLayer.startDep) / 10, 2)
                                                     ]
                                                    )
            layer_hole_ps_list.append([FindLayers(projectNo)[i].layerNo,
                                       hole_ps_list])
        return render_template('cptAnalysis.html',
                               projectNo=projectNo,
                               layer_hole_ps_list=layer_hole_ps_list
                               )

    if request.method == 'POST':
        str0 = "%s\t" % ('')
        for xHole in holelist:
            str0 = str0 + "%s\t" % (xHole.holeName)
        str0 = str0 + "\n"
        for i in range(0, len(FindLayers(projectNo))):
            str0 = str0 + FindLayers(projectNo)[i].layerNo + "\t"
            for xHole in holelist2:
                for yHole in holelist:
                    SumPs = 0
                    if xHole.holeName == yHole.holeName:
                        # print("%s\t"%(xHole.holeName))
                        if i >= len(xHole.layers):
                            str0 = str0 + "%s\t" % ('')
                        else:
                            xLayer = xHole.layers[i]
                            for testPoint in yHole.points:
                                # 注意小数位数不等也可能导致不相等，情况允许时，应该调整layer函数的位数
                                if (testPoint.testDep > round(xLayer.startDep, 2) and
                                   testPoint.testDep <= round(xLayer.endDep, 2)):
                                    SumPs = SumPs + testPoint.testValue
                            if xLayer.endDep - xLayer.startDep == 0:
                                str0 = str0 + "%s\t" % ('')
                            else:
                                str0 = str0 + "%.2f\t" % (SumPs / (xLayer.endDep - xLayer.startDep) / 10)
            str0 = str0 + "\n"
        basedir = os.path.abspath(os.path.dirname(__file__))
        filename = os.path.join(
            basedir,
            'static',
            'download',
            "1.txt"
        )
        f = open(filename, 'w', encoding="UTF-8")
        print(str0, file=f)
        f.close()
        myurl = url_for(
            "static",
            filename="download/1.txt"
        )
        print(myurl)
        return jsonify(result=myurl)


@analysis.route('/layerAnalysis')
def layerAnalysis():
    projectNo = request.args.get('projectNo')
    holeDict = ReceiveHoleLayer(projectNo)
    layerDict = OrderedDict()
    for xLayer in FindLayers(projectNo):
        layerNo = xLayer.layerNo
        layerName = xLayer.layerName
        maxThickness = 0
        minThickness = 1000
        maxTopElevation = -1000
        minTopElevation = 1000
        maxBottomElevation = -1000
        minBottomElevation = 1000
        dict1 = {}
        for holeName, xHole in holeDict.items():
            if xHole.layers.find(layerNo):
                dict1["layerName"] = layerName
                top = xHole.elevation - xHole.layers.find(layerNo).startDep
                bottom = xHole.elevation - xHole.layers.find(layerNo).endDep
                thickness = xHole.layers.find(layerNo).thickness
                if thickness > 0:
                    if top > maxTopElevation:
                        maxTopElevation = top
                    if top < minTopElevation:
                        minTopElevation = top
                    dict1["maxTopElevation"] = "%.2f" % maxTopElevation
                    dict1["minTopElevation"] = "%.2f" % minTopElevation
                    if layerNo != xHole.layers[-1].layerNo:
                        # 部分钻孔层位未钻穿，不应统计进去
                        if thickness > maxThickness:
                            maxThickness = thickness
                        if thickness < minThickness and thickness != 0:
                            minThickness = thickness
                        if bottom > maxBottomElevation:
                            maxBottomElevation = bottom
                        if bottom < minBottomElevation:
                            minBottomElevation = bottom
                        dict1["maxThickness"] = "%.2f" % maxThickness
                        dict1["minThickness"] = "%.2f" % minThickness
                        dict1["maxBottomElevation"] = "%.2f" % maxBottomElevation
                        dict1["minBottomElevation"] = "%.2f" % minBottomElevation
        layerDict[layerNo] = dict1
        layer_hole_elevation_list = []
        for xLayer in FindLayers(projectNo):
            layerNo = xLayer.layerNo
            list1 = []
            for holeName, xHole in holeDict.items():
                if xHole.layers.find(layerNo):
                    if layerNo != xHole.layers[-1].layerNo:
                        top = xHole.elevation - xHole.layers.find(layerNo).startDep
                        bottom = xHole.elevation - xHole.layers.find(layerNo).endDep
                        thickness = xHole.layers.find(layerNo).thickness
                        list1.append([holeName, thickness])
            layer_hole_elevation_list.append([layerNo, list1])
        '''

        layerDict = {"layerNo":{
                                "layerName":layerName,
                                "maxThickness":maxThickness,
                                "minThickness":minThickness,
                                "maxTopElevation":maxTopElevation,
                                "minTopElevation":minTopElevation,
                                "maxBottomElevation":maxBottomElevation,
                                "minBottomElevation":minBottomElevation
                                }
                    }
        '''

    return render_template('layerAnalysis.html',
                           projectNo=projectNo,
                           layerDict=layerDict,
                           layer_hole_elevation_list=layer_hole_elevation_list,
                           manager=FindManager(projectNo)
                           )
