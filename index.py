#-*-coding:utf-8-*-
#-------------------------------------------------------------------------------
# Name:        indexapp
# Purpose:     start web
#
# Author:      Robot of Fernando
#
# Created:     03-07-2015
# Copyright:   (c) Robot of Fernando 2015
# Licence:     The MIT License
#-------------------------------------------------------------------------------

from flask import Flask, render_template, request, url_for, redirect, jsonify
from maingui import *
from genpdf import *
from auth import *
import json
app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        #return redirect(url_for('index',projectNo=request.form['projectNo']))
        return projecthome(request.form['projectNo'])
    return render_template('index.html')

@app.route('/<projectNo>')
def projecthome(projectNo):
    return render_template('project_home.html',
                            projectNo=projectNo,
                            manager=FindManager(projectNo)
                            )

@app.route('/<projectNo>/water')
def water(projectNo):
    holelist=ResWater(projectNo)
    cnt=len(holelist)
    factor=GroupTotal(cnt)[0]
    rank=GroupTotal(cnt)[1]
    return render_template('water.html',
                            projectNo=projectNo,
                            holelist=holelist,
                            cnt=cnt,
                            rank=rank,
                            factor=factor,
                            manager=FindManager(projectNo)
                            )

@app.route('/<projectNo>/natural_foundation')
def natural_foundation(projectNo):
    layers=ExportLayers_Stat(projectNo)
    return render_template('naturalfoundation.html',
                            projectNo=projectNo,
                            layers=layers,
                            manager=FindManager(projectNo)
                            )
@app.route('/<projectNo>/pile')
def pile(projectNo):
    holelist=HoleAndLayer(projectNo,0)
    return render_template('pile.html',
                            projectNo=projectNo,
                            holelist=holelist,
                            manager=FindManager(projectNo)
                            )
@app.route('/pile_calculate')
def pile_calculate():
    req=request.args.to_dict()  #{"{G1:{1:[],2:[],3:[]}}":""}
    dict2list=[]
    for req_dict in req.keys(): #req_dict "{G1:{1:[],2:[],3:[]}}"
        req_dict=eval(req_dict) #eval(req_dict) {G1:{1:[],2:[],3:[]}}
        for value_dict in req_dict.values():
            dict2list=sorted(value_dict.items(),key=lambda item:int(item[0]))   #https://docs.python.org/3/howto/sorting.html#sortinghowto
            print(dict2list) #value_dict {1:[],2:[],3:[]}
    Rsk=0
    for i in range(len(dict2list)):
        try:
            dict2list[i][1][0]=float(dict2list[i][1][0])
        except ValueError:
            dict2list[i][1][0]=0
        try:
            dict2list[i][1][1]=float(dict2list[i][1][1])
        except ValueError:
            dict2list[i][1][1]=0
        if i==0:
            Rsk=dict2list[0][1][0]+dict2list[0][1][1]
        else:
            Rsk=Rsk+(dict2list[i][1][0]-dict2list[i-1][1][0])*dict2list[i][1][1]
    print(Rsk)
    return jsonify(result=Rsk)

@app.route('/<projectNo>/liquefaction')
def liquefaction(projectNo):
    siltLayers=FindSiltLayers(FindLayers(projectNo))
    siltLayersStr='、'.join('%s：%s'%(item.layerNo,item.layerName)for item in siltLayers)
    liqueHolesStr='、'.join(xHole.holeName for xHole in FindLiqueHole(projectNo))
    Reslique=ResLiquefaction(projectNo)
    return render_template('liquefaction.html',
                            projectNo=projectNo,
                            siltLayersStr=siltLayersStr,
                            liqueHolesStr=liqueHolesStr,
                            liqueList=Reslique[0],
                            caculatedHoleCount=Reslique[1],
                            caculatedPointCount=Reslique[2],
                            erroCount=Reslique[3],manager=FindManager(projectNo))

@app.route('/<projectNo>/CPT',methods=['POST','GET'])
def CPT(projectNo):
    holelist=FindCPT(projectNo)
    if request.method=='POST':
        probeNo=request.form['probeNo']
        probeArea=request.form['probeArea']
        fixedRatio=request.form['fixedRatio']
        testDate=request.form['testDate']
        holeName=request.form['holeName']
        probeInf={'probeNo':probeNo,'probeArea':probeArea,'fixedRatio':fixedRatio,'testDate':testDate}

        if request.form['action']=='打印所有静力触探':
            MaxNofHole=4 #一天最多施工4只勘探孔
            MaxTotalDep=160 #一天总进尺最多160m
            autoDate(testDate,MaxNofHole,MaxTotalDep,holelist)
            index=None
        elif request.form['action']=='打印单个静力触探':
            for xHole in holelist:
                if xHole.holeName==holeName:
                    index=holelist.index(xHole)
                    xHole.testDate=testDate
                    break
        pdfUrl=PrintPdf(probeInf,holelist,index)
        return redirect(url_for('static',filename=pdfUrl))
    return render_template('CPT.html',projectNo=projectNo,holelist=holelist,manager=FindManager(projectNo))

#生成cptpdf
@app.route('/download')
def download(probeInf,holelist,index=None):
    pdfUrl=PrintPdf(probeInf,holelist,index)
    return redirect(url_for('static',filename=pdfUrl))
##@app.route('/download/projectno=<cptstring>')
##def download(cptstring):
##    #通过string组合来传入多个值
##    holeName=cptstring.split('=')[1]
##    projectNo=cptstring.split('?')[0]
##    holelist=FindCPT(projectNo)
##    for xHole in holelist:
##        if xHole.holeName==holeName:
##            ExportPDFofCPT(xHole,probeInf)
##            pdfUrl='download/'+projectNo+'/'+holeName+'.pdf'
##            return redirect(url_for('static',filename=pdfUrl))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)