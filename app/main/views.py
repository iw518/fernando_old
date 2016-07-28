#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      views
# date:         2016-07-19
# copyright:    copyright  2016 Xu, Aiwu
# -------------------------------------------------------------------------------
from flask import render_template, request, jsonify

from . import main
from .auth2 import *
from .maingui import *


@main.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        projectNo = request.form['projectNo']
        return render_template('project.html', projectNo=projectNo)
    else:
        return render_template('index.html')


@main.route("/layersConfig", methods=['POST', 'GET'])
def layersConfig():
    projectNo = request.args.get('projectNo')
    layerConfigDict = importXml()
    if request.method == 'POST':
        return jsonify(result=layerConfigDict)
    else:
        return render_template(
            "layersConfig.html",
            projectNo=projectNo,
            manager=FindManager(projectNo),
            layerConfigDict=layerConfigDict
        )


@main.route("/index2", methods=['POST', 'GET'])
def index2():
    if request.method == 'POST':
        projectNo = request.form['projectNo']
        # return redirect(url_for('index',projectNo=request.form['projectNo']))
        return render_template('project_home_old.html', projectNo=projectNo)
    else:
        return render_template('index_old.html')


