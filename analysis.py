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
    holelist = FindCPT(projectNo)
    holelist2 = ReceiveHoleLayer(projectNo, 2)
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
                            for testPoint in yHole.testPoints:
                                if testPoint.testDep > round(xLayer.startDep, 2) and testPoint.testDep <= round(xLayer.endDep, 2):  # 注意小数位数不等也可能导致不相等，情况允许时，应该调整layer函数的位数
                                    SumPs = SumPs + testPoint.testValue
                            if xLayer.endDep - xLayer.startDep == 0:
                                hole_ps_list.append((xHole.holeName, 0))
                            else:
                                hole_ps_list.append((xHole.holeName,
                                                     round(SumPs / (xLayer.endDep - xLayer.startDep) / 10, 2)
                                                     )
                                                    )
            layer_hole_ps_list.append((FindLayers(projectNo)[i].layerNo,
                                       hole_ps_list))
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
                            for testPoint in yHole.testPoints:
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
        filename=os.path.join(basedir,'static', 'download', "1.txt")
        f = open(filename, 'w', encoding="UTF-8")
        print(str0, file=f)
        f.close()
        myurl=url_for("static", filename="download/1.txt")
        print(myurl)
        return jsonify(result=myurl)