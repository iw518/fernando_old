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

from flask import render_template, request, jsonify, Blueprint
from maingui import *
from genpdf import *
from auth import *
from GFunction import *
calculation = Blueprint('calculation', __name__)


@calculation.route('/water')
def water():
    projectNo = request.args.get('projectNo')
    holeDict = ReceiveHoleBasicInf(projectNo, 1)
    # holelist=list(filter(lambda xHole: type(xHole.waterLevel) is float, holelist))
    # lambda example:    lambda x: boolfun(x), sequen
    # oldway:   filter(lambda xHole: type(xHole.waterLevel) is float, holelist)
    # newway:    list(filter(...))

    holelist = []
    for holeName, xHole in holeDict.items():
        if FilterZero(xHole.waterLevel) != '-':
            holelist.append(xHole)
    cnt = len(holelist)
    factor = GroupTotal(cnt)[0]
    rank = GroupTotal(cnt)[1]
    return render_template('water.html',
                           projectNo=projectNo,
                           holelist=holelist,
                           cnt=cnt,
                           rank=rank,
                           factor=factor,
                           manager=FindManager(projectNo)
                           )


@calculation.route('/natural_foundation', methods=['POST', 'GET'])
def natural_foundation():
    projectNo = request.args.get('projectNo')
    if request.method == "GET":
        layers = ExportLayers_Stat(projectNo)
        return render_template('naturalfoundation.html',
                               projectNo=projectNo,
                               layers=layers,
                               manager=FindManager(projectNo)
                               )
    else:
        depth = float(request.form['depth'])
        water_depth = float(request.form['water_depth'])
        layers = ExportLayers_Stat(projectNo)
        xlist = []
        for xLayer in layers:
            xlist.append((xLayer.Ps_Fak(depth, water_depth),
                          xLayer.Soil_Fak(depth, water_depth),
                          xLayer.Fak(depth, water_depth)
                          ))
        return jsonify(result=xlist)
        # return make_response(dumps(xlist))与jsonify(data=xlist)等效，
        # 前者在前端中可直接用data访问，但是后者在前端中需用字典访问，即data.data形式
        # erro jsonify(data=layers)由于layers中的元素为layer对象，
        # flask由于ES5的安全原因，不允许序列化,需转换为字符串、或与字符串相关的数组，元组，字典等


@calculation.route('/pile')
def pile():
    projectNo = request.args.get('projectNo')
    holeDict = ReceiveHoleLayer(projectNo, 1)
    holeDict.update(ReceiveHoleLayer(projectNo, 2))
    print(holeDict)
    holelist=[]
    for holeName, xHole in holeDict.items():
        holelist.append(xHole)
    layerlist = ExportLayers_Stat(projectNo)
    return render_template('pile.html',
                           projectNo=projectNo,
                           holelist=holelist,
                           manager=FindManager(projectNo),
                           layerlist=layerlist
                           )
# @calculation.route('/pile_calculate')
# def pile_calculate():
#     req=request.args.to_dict()  #{"{G1:{1:[],2:[],3:[]}}":""}
#     dict2list=[]
#     for req_dict in req.keys(): #req_dict "{G1:{1:[],2:[],3:[]}}"
#         req_dict=eval(req_dict) #eval(req_dict) {G1:{1:[],2:[],3:[]}}
#         for value_dict in req_dict.values():
#             dict2list=sorted(value_dict.items(),key=lambda item:int(item[0]))
#             https://docs.python.org/3/howto/sorting.html#sortinghowto
#             print(dict2list) #value_dict {1:[],2:[],3:[]}
#     Rsk=0
#     for i in range(len(dict2list)):
#         try:
#             dict2list[i][1][0]=float(dict2list[i][1][0])
#         except ValueError:
#             dict2list[i][1][0]=0
#         try:
#             dict2list[i][1][1]=float(dict2list[i][1][1])
#         except ValueError:
#             dict2list[i][1][1]=0
#         if i==0:
#             Rsk=dict2list[0][1][0]+dict2list[0][1][1]
#         else:
#             Rsk=Rsk+(dict2list[i][1][0]-dict2list[i-1][1][0])*dict2list[i][1][1]
#     print(Rsk)
#     return jsonify(result=Rsk)


@calculation.route('/liquefaction')
def liquefaction():
    projectNo = request.args.get('projectNo')
    siltLayers = FindSiltLayers(FindLayers(projectNo))
    siltLayersStr = '、'.join('%s：%s' % (item.layerNo, item.layerName) for item in siltLayers)
    liqueHolesStr = '、'.join(xHole.holeName for xHole in FindLiqueHole(projectNo))
    Reslique = ResLiquefaction(projectNo)
    return render_template('liquefaction.html',
                           projectNo=projectNo,
                           siltLayersStr=siltLayersStr,
                           liqueHolesStr=liqueHolesStr,
                           liqueList=Reslique[0],
                           caculatedHoleCount=Reslique[1],
                           caculatedPointCount=Reslique[2],
                           erroCount=Reslique[3],
                           manager=FindManager(projectNo)
                           )
