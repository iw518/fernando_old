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
from analysis import analysis

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
