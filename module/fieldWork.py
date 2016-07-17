# -*-coding:utf-8-*-
# -------------------------------------------------------------------------
# Name:        fieldWork
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

fieldWork = Blueprint('fieldWork', __name__)


@fieldWork.route("/sitePhoto", methods=['POST', 'GET'])
def sitePhoto():
    if request.method == "GET":
        projectNo = request.args.get('projectNo')
        return render_template(
            'fieldWork/sitePhoto.html',
            projectNo=projectNo,
            manager=FindManager(projectNo)
        )
    else:
        files = request.files.getlist('file[]')
        # 多个同名name的input提交采用getlist
        notes = request.form.getlist("note")
        # 此处需重复
        basedir = os.path.abspath(os.path.dirname(__file__))
        basedir = os.path.abspath(os.path.dirname(basedir))
        filedir = os.path.join(basedir, 'upload')
        responseTxt = "%d files have been uploaded!" % len(files)
        print(responseTxt)
        for i in range(0, len(files)):
            note = notes[i]
            f = files[i]
            filename = f.filename
            f.save(os.path.join(filedir, filename))
            print("%s note:%s" % (filename, note))
        return responseTxt


@fieldWork.route("/siteMap")
def siteMap():
    projectNo = request.args.get('projectNo')
    return render_template(
        'fieldWork/siteMap.html',
        projectNo=projectNo,
        manager=FindManager(projectNo)
    )
