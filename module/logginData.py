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

from flask import render_template, request, Blueprint,jsonify

from auth2 import *
from maingui import *

logginData = Blueprint('logginData', __name__)


@logginData.route("/layersInf", methods=["GET", "POST"])
def layersInf():
    projectNo = request.args.get('projectNo')
    layerConfigDict = importXml()
    if request.method == "POST":
        templateName = request.form["templateName"]
        print("bug"+templateName)
        print(layerConfigDict[templateName])
        return jsonify(result=layerConfigDict[templateName])

    else:
        return render_template(
            "logginData/layersInf.html",
            projectNo=projectNo,
            manager=FindManager(projectNo),
            layerConfigDict=layerConfigDict
        )

@logginData.route("/holesInf", methods=["GET", "POST"])
def holesInf():
    projectNo = request.args.get("projectNo")
    return render_template(
        "logginData/holesInf.html",
        projectNo=projectNo,
        manager=FindManager(projectNo)
    )
