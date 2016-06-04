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

from flask import Flask, render_template, request, url_for, jsonify
from maingui import *
from genpdf import *
from auth import *
from statistics import statistics
from calculation import calculation
app = Flask(__name__)
app.register_blueprint(calculation, url_prefix='/calculation')
app.register_blueprint(statistics, url_prefix='/statistics')


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
    holelist = FindCPT(projectNo)
    holelist2 = ReceiveHoleLayer(projectNo, 2)
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

        filename = PrintPdf(probeInf, holelist, index)
        filename = 'download/' + os.path.basename(filename)
        pdfUrl = url_for('static', filename=filename)
        print(pdfUrl)
        return render_template('pdf.html', url=pdfUrl)
    return render_template('CPT.html',
                           projectNo=projectNo,
                           holelist=holelist,
                           manager=FindManager(projectNo),
                           holelist2=holelist2)


@app.route('/<projectNo>/ZZT', methods=['POST', 'GET'])
def ZZT(projectNo):
    holelist = ReceiveHoleLayer(projectNo, 1)
    return render_template('ZZT.html',
                           projectNo=projectNo,
                           holelist=holelist,
                           manager=FindManager(projectNo)
                           )


@app.route('/index_analysis', methods=['POST', 'GET'])
def index_analysis():
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
        return render_template('index_analysis.html',
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
