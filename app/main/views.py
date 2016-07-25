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
from .sql3 import Sql3


@main.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        projectNo = request.form['projectNo']
        return render_template('register.html', projectNo=projectNo)
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


@main.route('/reportCheck', methods=['POST', 'GET'])
def reportCheck():
    projectNo = request.args.get('projectNo')
    opinions=""
    if request.method == "POST":
        opinions=request.form["content"]
        print("opinions="+opinions)
        database = Sql3()
        sql = "SELECT [reportOpinions].[pid] FROM [reportOpinions] INNER JOIN [projectInfo] ON [projectInfo].[pid] = [reportOpinions].[pid] WHERE [projectInfo].[projectNo] = '%s'" % (projectNo)
        if(database.ExecQuery(sql)):
            sql ="UPDATE [reportOpinions] SET [opinions] = '%s' WHERE [pid] = (SELECT [pid] FROM [projectInfo] WHERE [projectInfo].[projectNo] = '%s')" % (opinions, projectNo)
        else:
            sql = "INSERT INTO [reportOpinions] ([pid],[opinions]) VALUES ((SELECT [pid] FROM [projectInfo] WHERE [projectInfo].[projectNo] = '%s'), '%s')" % (projectNo,opinions)
        database.ExecNonQuery(sql)
        return jsonify(result="success!")

    else:
        database = Sql3()
        sql = "SELECT reportOpinions.opinions from reportOpinions INNER JOIN projectInfo on projectInfo.pid=reportOpinions.pid WHERE projectInfo.projectNo='%s'" % (projectNo)
        try:
            res = database.ExecQuery(sql)
            opinions = res[0][0].encode('latin-1').decode('utf-8')
            print(opinions)
        except Exception as e:
            print(e)
            opinions=e
        return render_template(
            'check/reportCheck.html',
            projectNo=projectNo,
            manager=FindManager(projectNo),
            opinions=opinions
        )
