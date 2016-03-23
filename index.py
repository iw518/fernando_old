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

from flask import Flask, render_template, request, url_for, redirect, jsonify,make_response
from maingui import *
from genpdf import *
from auth import *
import json
from json import dumps
app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        #return redirect(url_for('index',projectNo=request.form['projectNo']))
        return projecthome(request.form['projectNo'])
    return render_template('index.html')
##当执行127.0.0.1/时其可以执行'/'，也可执行'/<projectNo>'，故需加一个判断
##此处还可进一步优化，写成127.0.0.1/?No=K059-2015形式
@app.route('/<projectNo>')
def projecthome(projectNo):
    if request.method=='POST':
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

@app.route('/<projectNo>/natural_foundation',methods=['POST','GET'])
def natural_foundation(projectNo):
    if request.method=="GET":
        layers=ExportLayers_Stat(projectNo)
        return render_template('naturalfoundation.html',
                                projectNo=projectNo,
                                layers=layers,
                                manager=FindManager(projectNo)
                                )
    else:
        depth=float(request.form['depth'])
        water_depth=float(request.form['water_depth'])
        layers=ExportLayers_Stat(projectNo,depth,water_depth)
        xlist=[]
        for xLayer in layers:
            xlist.append((xLayer.Ps_Fak,xLayer.Soil_Fak,xLayer.Fak))
        return jsonify(result=xlist)

        #print(convert_to_dicts(layers))
        #return jsonify(data=convert_to_dicts(layers))
        #return make_response(dumps(xlist))与jsonify(data=xlist)等效，
        #前者在前端中可直接用data访问，但是后者在前端中需用字典访问，即data.data形式
        #erro jsonify(data=layers)由于layers中的元素为layer对象，
        #flask由于ES5的安全原因，不允许序列化,需转换为字符串、或与字符串相关的数组，元组，字典等

@app.route('/<projectNo>/pile')
def pile(projectNo):
    holelist=ReceiveHoleLayer(projectNo,1)
    holelist.extend(ReceiveHoleLayer(projectNo,2))
    layerlist=ExportLayers_Stat(projectNo)
    return render_template('pile.html',
                            projectNo=projectNo,
                            holelist=holelist,
                            manager=FindManager(projectNo),
                            layerlist=layerlist
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
    index=None
    if request.method=='POST':
        probeNo=request.form['probeNo']
        probeArea=request.form['probeArea']
        fixedRatio=request.form['fixedRatio']
        testDate=request.form['testDate']
        probeInf={'probeNo':probeNo,'probeArea':probeArea,'fixedRatio':fixedRatio,'testDate':testDate}

        if request.form['print_btn']=='打印所有静力触探':
            MaxNofHole=4 #一天最多施工4只勘探孔
            MaxTotalDep=160 #一天总进尺最多160m
            autoDate(testDate,MaxNofHole,MaxTotalDep,holelist)
            index=None
        elif request.form['print_btn']=='打印单个静力触探':
            index=int(request.form['holeName'])
            holelist[index].testDate=testDate
        print(index)
        pdfUrl=PrintPdf(probeInf,holelist,index)
        return render_template('pdf.html',
                                url=url_for('static',filename=pdfUrl),
                                )
    return render_template('CPT.html',projectNo=projectNo,holelist=holelist,manager=FindManager(projectNo))

def convert_to_dicts(objs):
    '''把对象列表转换为字典列表'''
    obj_arr = []

    for o in objs:
        #把Object对象转换成Dict对象
        dict = {}
        #for item in dir(o):
            #dict[item]=o.item错误o没有‘item’
        #dict.update(o.__dict__)
        for item in dir(o):
            dict[item]=getattr(o,item,0)
        #print(dir(o))
        print(dict)
        obj_arr.append(dict)
    return obj_arr

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)