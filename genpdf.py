#-*-coding:utf-8-*-
#-------------------------------------------------------------------------------
# Name:
# Purpose:     gen cpt pdf
#
# Author:      Robot of Fernando
#
# Created:     17-06-2015
# Copyright:   (c) Robot of Fernando 2015
# Licence:     The MIT License
#-------------------------------------------------------------------------------
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, cm, portrait
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak

#import reportlab.rl_config
from reportlab.pdfbase import pdfmetrics

from reportlab.pdfbase.cidfonts import UnicodeCIDFont, findCMapFile
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))

from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('SIMSUN','SIMSUN.ttc'))
pdfmetrics.registerFont(TTFont('SIMHEI','SIMHEI.ttf'))

def PrintPdf(probeInf,holelist,index=None):
    import os
    projectNo=holelist[0].projectNo
    cptPath='C:/pythonweb/env/static/download/'+projectNo+'/'
    if not os.path.exists(cptPath):
        os.makedirs(cptPath)
    doc = SimpleDocTemplate(cptPath, pagesize=A4, rightMargin=10,leftMargin=20, topMargin=30,bottomMargin=20)
    doc.pagesize = portrait(A4)
    elements = []
    for i in range(len(holelist)):
        if index!=None:
            i=index
            path=holelist[i].holeName+'.pdf'
            elements.extend(Cpt2Pdf(holelist[i],probeInf)) #Attenion:where elments.extend must be used,but not elements.append
            break;
        else:
            path='all'+'.pdf'
            elements.extend(Cpt2Pdf(holelist[i],probeInf)) #Attenion:where elments.extend must be used,but not elements.append
    doc.filename=cptPath+path
    doc.build(elements)
    return (doc.filename.split('static/'))[1]

def Cpt2Pdf(xHole,probeInf):
    pointsList=xHole.testPoints
    L=len(pointsList)
    if L%250==0:
        pageNums=L//250
    else:
        pageNums=L//250+1
    elements = []
    for i in range(pageNums):
        data=[]
        for j in range(50):
            item=[]
            for k in range(5):
                Aijk=i*250+k*50+j
                if Aijk<L:
                    item.append('%.1f'%(pointsList[Aijk].testDep))
                    item.append('%.2f'%(pointsList[Aijk].testValue))
            data.append(item)
        #Send the data and build the file

        elements.append(TemplateofCPTPDF(data,xHole,probeInf))
        elements.append(PageBreak())
    return elements

#静力触探记录表表格样式，其中的data(静力触探数据)通过函数CPT2PDF(xHole,probeInf)出入
def TemplateofCPTPDF(data,xHole,probeInf):
    projectNo=xHole.projectNo
    holeName=xHole.holeName
    holeDep=(len(xHole.testPoints))/10
    probeNo=probeInf['probeNo']
    probeArea=probeInf['probeArea']
    fixedRatio=probeInf['fixedRatio']

    pagedata=[['单桥静力触探记录表','','','','','','','','','']]
    pagedata.append(['工程编号',projectNo,
                     '孔          号',holeName,
                     '孔          深','%.1f'%holeDep+'m',
                     '探头编号',probeNo,
                     '测试日期',xHole.testDate]
                     )
    pagedata.append(['锥头面积',probeArea+'cm2',
                     '标定系数',fixedRatio+'kPa',
                     '','','','','','']
                     )
    pagedata.append(['','','','','','','','','',''])#目的是空出一行，使得下划线与下一行的外框线不重合
    pagedata.append(
    ['深度\n(m)','比贯入阻力\nPs(MPa)',
    '深度\n(m)','比贯入阻力\nPs(MPa)',
    '深度\n(m)','比贯入阻力\nPs(MPa)',
    '深度\n(m)','比贯入阻力\nPs(MPa)',
    '深度\n(m)','比贯入阻力\nPs(MPa)']
    )
    pagedata.extend(data)
    pagedata.append(
    ['测          试',
    '',
    '',
    '复          核',
    '',
    '',
    '',
    '',
    '',
    '']
    )
    #TODO: Get this line right instead of just copying it from the docs
    style=TableStyle([('FONT',(0,0),(-1,0),'SIMHEI',20),
                      #('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),#内框
                      ('SPAN',(0,0),(-1,0)),
                      ('SPAN',(3,2),(5,2)),
                      ('FONT',(0,1),(-1,4),'STSong-Light',9.5),
                      ('FONT',(0,5),(-1,-2),'Times-Roman',9),
                      ('FONT',(0,-1),(-1,-1),'STSong-Light',9.5),
                      ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                      ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                      ('ALIGN',(0,0),(-1,-1),'CENTER'),
                      ('ALIGN',(1,1),(1,1),'LEFT'),
                      ('ALIGN',(3,1),(3,1),'LEFT'),
                      ('ALIGN',(5,1),(5,1),'LEFT'),
                      ('ALIGN',(7,1),(7,1),'LEFT'),
                      ('ALIGN',(-1,1),(-1,1),'LEFT'),
                      ('ALIGN',(1,2),(1,2),'LEFT'),
                      ('ALIGN',(3,2),(5,2),'CENTER'),
                      ('LINEBELOW',(1,1),(1,1),0.25,colors.black),
                      ('LINEBELOW',(3,1),(3,1),0.25,colors.black),
                      ('LINEBELOW',(5,1),(5,1),0.25,colors.black),
                      ('LINEBELOW',(7,1),(7,1),0.25,colors.black),
                      ('LINEBELOW',(-1,1),(-1,1),0.25,colors.black),
                      ('LINEBELOW',(1,2),(1,2),0.25,colors.black),
                      ('LINEBELOW',(3,2),(5,2),0.25,colors.black),
                      ('LINEBELOW',(0,4),(-1,4),1.00,colors.black),
                      ('LINEBELOW',(1,-1),(2,-1),0.25,colors.black),
                      ('LINEBELOW',(4,-1),(5,-1),0.25,colors.black),
                      ('LINEBEFORE',(1,4),(1,-2),0.25,colors.black),
                      ('LINEBEFORE',(3,4),(3,-2),0.25,colors.black),
                      ('LINEBEFORE',(5,4),(5,-2),0.25,colors.black),
                      ('LINEBEFORE',(7,4),(7,-2),0.25,colors.black),
                      ('LINEBEFORE',(-1,4),(-1,-2),0.25,colors.black),
                      ('LINEAFTER',(1,4),(1,-2),1,colors.black),
                      ('LINEAFTER',(3,4),(3,-2),1,colors.black),
                      ('LINEAFTER',(5,4),(5,-2),1,colors.black),
                      ('LINEAFTER',(7,4),(7,-2),1,colors.black),
                      ('BOX', (0,4), (-1,-2), 1.5, colors.black),#外边框
                      ])
    #Configure style and word wrap
    #t=Table(data,10*[1.75*cm],54*[0.5*cm])
    #colswidth,rowswidth can be list or tuple
    colswidth=[]
    for i in range(5):
        colswidth.append(1.5*cm)
        colswidth.append(2.0*cm)
    rowswidth=[1.2*cm,0.6*cm,0.6*cm,0.2*cm,1.2*cm]
    for i in range(50):
        rowswidth.append(0.41*cm)
    rowswidth.append(0.6*cm)
    t=Table(pagedata,colswidth,rowswidth)
    t.setStyle(style)
    return t