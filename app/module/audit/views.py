#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      views
# date:         2016-07-27
# copyright:    copyright  2016 Xu, Aiwu
# -------------------------------------------------------------------------------
from flask import render_template, request, jsonify

from app import db
from app.models import Project, Opinion
from . import audit


@audit.route('/reportCheck', methods=['POST', 'GET'])
def reportCheck():
    projectNo = request.args.get('projectNo')
    project = Project.query.filter_by(identifier=projectNo).first()
    project_id = project.id
    if request.method == "POST":
        opinion_content = request.form["content"]
        opinion_stage = request.form["stage"]
        for opinion in project.opinions:
            if opinion.stage == opinion_stage:
                opinion.content = opinion_content
                db.session.commit()
                return jsonify(result='successful!')
        opinion = Opinion(project_id, opinion_stage, opinion_content)
        db.session.add(opinion)
        db.session.commit()
        return jsonify(result='successful!')
    stages = {'tender': '标书', 'scheme': '纲要', 'report': '报告'}
    return render_template(
        'audit/reportCheck.html',
        projectNo=projectNo,
        project=project, stages=stages
    )
