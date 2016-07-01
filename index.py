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

from flask import Flask, render_template, request, jsonify
from maingui import *
from genpdf import *
from auth import *
from GHole import *
from GLayer import *
from GPoint import *
from GFunction import *
from module.logginData import logginData
from module.calculation import calculation
from module.diagram import diagram
from module.analysis import analysis
from module.statistics import statistics

app = Flask(__name__)
app.register_blueprint(logginData, url_prefix="/logginData")
app.register_blueprint(calculation, url_prefix="/calculation")
app.register_blueprint(diagram, url_prefix="/logginData")
app.register_blueprint(statistics, url_prefix="/statistics")
app.register_blueprint(analysis, url_prefix="/analysis")


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        projectNo = request.form['projectNo']        
        return render_template('project_home.html', projectNo=projectNo)
    else:
        return render_template('index.html')


@app.route('/<projectNo>')
def projecthome(projectNo):
    return render_template('project_home.html', projectNo=projectNo)


@app.route("/layersConfig", methods=['POST', 'GET'])
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


@app.route("/index2", methods=['POST', 'GET'])
def index2():
    if request.method == 'POST':
        projectNo = request.form['projectNo']
        # return redirect(url_for('index',projectNo=request.form['projectNo']))
        return render_template('project_home_old.html', projectNo=projectNo)
    else:
        return render_template('index_old.html')


@app.route('/reportCheck')
def reportCheck():
    projectNo = request.args.get('projectNo')
    return render_template('check/reportCheck.html', projectNo=projectNo, manager=FindManager(projectNo))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
