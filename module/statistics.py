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

from flask import Blueprint, render_template, request

from auth2 import *
from maingui import *

statistics = Blueprint('statistics', __name__)


@statistics.route('/workloads')
def workloads():
    projectNo = request.args.get('projectNo')
    holeDict = ReceiveHoleBasicInf(projectNo)
    dict_workloads = {}
    dict_soilloads = workloads_soiltest(projectNo)
    for key in DICT_HoleType.keys():
        sumN = 0
        sumDep = 0
        for holeName, xHole in holeDict.items():
            if xHole.holeType == DICT_HoleType[key][0]:
                sumDep = sumDep + xHole.Dep
                sumN = sumN + 1
        dict_workloads[key] = (DICT_HoleType[key][1], sumN, sumDep)
    list1=[]
    list2=[]
    holeDict=ReceiveHoleBasicInf(projectNo, 1)
    for holeName, xHole in holeDict.items():
        list1.append(xHole)
    holeDict=FindHoleAndDep(projectNo)
    for holeName, xHole in holeDict.items():
        list2.append(xHole)

    return render_template('statistics/workloads.html', projectNo=projectNo, dict_workloads=dict_workloads, dict_soilloads=dict_soilloads, manager=FindManager(projectNo),list1=list1,list2=list2)


@statistics.route('/excavation')
def excavation():
    projectNo = request.args.get('projectNo')
    layers = ExportLayers_Stat(projectNo, 2)
    return render_template('statistics/excavation.html', projectNo=projectNo, manager=FindManager(projectNo), layers=layers)
