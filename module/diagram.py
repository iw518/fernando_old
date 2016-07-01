# -*-coding:utf-8-*-
# -------------------------------------------------------------------------------
# Name:        logginData
# Purpose:     input data of layer and hole
#
# Author:      Robot of Fernando
#
# Created:     28-06-2016
# Copyright:   (c) Robot of Fernando 2015
# Licence:     The MIT License
# -------------------------------------------------------------------------------

from flask import render_template, request, Blueprint
from maingui import *
from auth import *

diagram = Blueprint('diagram', __name__)


@diagram.route('/CPT', methods=['POST', 'GET'])
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
    return render_template(
        'CPT.html',
        projectNo=projectNo,
        holelist=holelist,
        manager=FindManager(projectNo),
        holeDict=holeDict
    )


@diagram.route('/ZZT')
def ZZT():
    projectNo = request.args.get('projectNo')
    holeDict = ReceiveHoleLayer(projectNo, 1)
    return render_template(
        'ZZT.html',
        projectNo=projectNo,
        holeDict=holeDict,
        manager=FindManager(projectNo)
    )
