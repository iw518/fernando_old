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
from flask.ext.bootstrap import Bootstrap

from auth2 import *
from maingui import *
from module.analysis import analysis
from module.auth import auth as auth_blueprint
from module.auth.forms import LoginForm
from module.calculation import calculation
from module.diagram import diagram
from module.fieldWork import fieldWork
from module.logginData import logginData
from module.statistics import statistics
from sql3 import Sql3

app = Flask(__name__)
bootstrap=Bootstrap(app)
app.register_blueprint(logginData, url_prefix="/logginData")
app.register_blueprint(calculation, url_prefix="/calculation")
app.register_blueprint(diagram, url_prefix="/logginData")
app.register_blueprint(statistics, url_prefix="/statistics")
app.register_blueprint(analysis, url_prefix="/analysis")
app.register_blueprint(fieldWork, url_prefix="/fieldWork")
app.register_blueprint(auth_blueprint, url_prefix='/auth')
#configuration
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
app.config.from_object(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        projectNo = request.form['projectNo']
        return render_template('project.html', projectNo=projectNo)
    else:
        return render_template('index.html')


@app.route('/<projectNo>')
def projecthome(projectNo):
    return render_template('project.html', projectNo=projectNo)


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


@app.route('/reportCheck', methods=['POST', 'GET'])
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


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = {}
        user['userID'] = form.userID.data
        user['password'] = form.password.data
        print(user['userID'])
        if user['userID']=='iw518' and user['password']=='800820' :
            return render_template('index.html')
    return render_template('auth/login.html',form=form)

@app.route('/login2', methods=['GET','POST'])
def login2():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = {}
        user['userID'] = form.userID.data
        user['password'] = form.password.data
        print(user['userID'])
        if user['userID']=='iw518' and user['password']=='800820' :
            return render_template('index.html')
    return render_template('auth/login2.html',form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
