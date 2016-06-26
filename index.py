# -*-coding:utf-8-*-
# -------------------------------------------------------------------------------
# Name:        indexapp
# Purpose:     start web
#
# Author:      Robot of Fernando
#
# Created:     03-07-2015
# Copyright:   (c) Robot of Fernando 2015
# Licence:     The MIT License
# -------------------------------------------------------------------------------

from flask import Flask, render_template, request, url_for,jsonify
from maingui import *
from genpdf import *
from auth import *
from statistics import statistics
from calculation import calculation
from analysis import analysis
from GHole import *
from GLayer import *
from GPoint import *
from GFunction import *

app = Flask(__name__)
app.register_blueprint(calculation, url_prefix='/calculation')
app.register_blueprint(statistics, url_prefix='/statistics')
app.register_blueprint(analysis, url_prefix='/analysis')


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        projectNo = request.form['projectNo']
        # return redirect(url_for('index',projectNo=request.form['projectNo']))
        return render_template('project_home.html', projectNo=projectNo)
    else:
        return render_template('index.html')


@app.route('/<projectNo>')
def projecthome(projectNo):
    return render_template('project_home.html', projectNo=projectNo)


@app.route('/CPT', methods=['POST', 'GET'])
def CPT():
    projectNo = request.args.get('projectNo')
    holeDict = FindCPT(projectNo)
    holelist = []
    for holeName, xHole in holeDict.items():
        holelist.append(xHole)
    holeDict = ReceiveHoleLayer(projectNo, 2)
    index = None
    if request.method == 'POST':
        probeNo = request.form['probeNo']
        probeArea = request.form['probeArea']
        fixedRatio = request.form['fixedRatio']
        testDate = request.form['testDate']
        probeInf = {'probeNo': probeNo,
                    'probeArea': probeArea,
                    'fixedRatio': fixedRatio,
                    'testDate': testDate}

        if request.form['print_btn'] == '打印所有静力触探':
            MaxNofHole = 4          # 一天最多施工4只勘探孔
            MaxTotalDep = 160       # 一天总进尺最多160m
            autoDate(testDate, MaxNofHole, MaxTotalDep, holelist)
            index = None
        elif request.form['print_btn'] == '打印单个静力触探':
            index = int(request.form['holeName'])
            holelist[index].testDate = testDate

        filename = PrintPdf(projectNo, probeInf, holelist, index)
        filename = 'download/' + os.path.basename(filename)
        pdfUrl = url_for('static', filename=filename)
        print(pdfUrl)
        return render_template('pdf.html', url=pdfUrl)
    return render_template('CPT.html',
                           projectNo=projectNo,
                           holelist=holelist,
                           manager=FindManager(projectNo),
                           holeDict=holeDict)


@app.route('/ZZT')
def ZZT():
    projectNo = request.args.get('projectNo')
    holeDict = ReceiveHoleLayer(projectNo, 1)
    return render_template('ZZT.html',
                           projectNo=projectNo,
                           holeDict=holeDict,
                           manager=FindManager(projectNo)
                           )
@app.route('/layerAnalysis')
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
            list1=[]
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


@app.route("/layersInf")
def layersInf():
    projectNo = request.args.get('projectNo')
    layerConfigDict = importXml()
    return render_template("layersInf.html", projectNo=projectNo, manager=FindManager(projectNo), layerConfigDict=layerConfigDict)


@app.route("/layersConfig", methods=['POST', 'GET'])
def layersConfig():
    projectNo = request.args.get('projectNo')
    layerConfigDict = importXml()
    if request.method == 'POST':
        return jsonify(result=layerConfigDict)
    else:
        return render_template("layersConfig.html", projectNo=projectNo, manager=FindManager(projectNo), layerConfigDict=layerConfigDict)    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
