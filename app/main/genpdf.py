# -*-coding:utf-8-*-
# -------------------------------------------------------------------------------
# Name:
# Purpose:     gen cpt pdf
#
# Author:      Robot of Fernando
#
# Created:     17-06-2015
# Copyright:   (c) Robot of Fernando 2015
# Licence:     The MIT License
# -------------------------------------------------------------------------------
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, cm, portrait
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
# from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak
# import reportlab.rl_config
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
pdfmetrics.registerFont(TTFont('SIMSUN', 'SIMSUN.ttc'))
pdfmetrics.registerFont(TTFont('SIMHEI', 'SIMHEI.ttf'))


def PrintPdf(projectNo, probeInf, holelist, index=None):
    import os
    from config import basedir
    cptPath = os.path.join(basedir, 'app', 'static', 'download')

    if not os.path.exists(cptPath):
        os.makedirs(cptPath)
    doc = SimpleDocTemplate(cptPath,
                            pagesize=A4,
                            rightMargin=10,
                            leftMargin=20,
                            topMargin=30,
                            bottomMargin=20
                            )
    doc.pagesize = portrait(A4)
    filename = ''
    elements = []
    for i in range(len(holelist)):
        if index is not None:
            i = index
            filename = projectNo + '__' + holelist[i].holeName + '.pdf'
            # Attenion:where elments.extend must be used,but not elements.append
            elements.extend(Cpt2Pdf(holelist[i], probeInf))
            break;
        else:
            filename = projectNo + '__' + 'all.pdf'
            # Attenion:where elments.extend must be used,but not elements.append
            elements.extend(Cpt2Pdf(holelist[i], probeInf))
    doc.filename = os.path.join(cptPath, filename)
    print("dd" + doc.filename)
    doc.build(elements)
    # url='/'.join(['download',projectNo,filename])
    # os.path.join('download',projectNo,filename)将返回download\projectNo\filename，浏览器无法识别
    return doc.filename


def Cpt2Pdf(xHole, probeInf):
    pointsList = xHole.points
    L = len(pointsList)
    if L % 250 == 0:
        pageNums = L // 250
    else:
        pageNums = L // 250 + 1
    elements = []
    for i in range(pageNums):
        data = []
        for j in range(50):
            item = []
            for k in range(5):
                Aijk = i * 250 + k * 50 + j
                if Aijk < L:
                    item.append('%.1f' % (pointsList[Aijk].testDep))
                    item.append('%.2f' % (pointsList[Aijk].testValue))
            data.append(item)
        # Send the data and build the file
        elements.append(TemplateofCPTPDF(data, xHole, probeInf))
        elements.append(PageBreak())
    return elements


# 静力触探记录表表格样式，其中的data(静力触探数据)通过函数CPT2PDF(xHole,probeInf)出入
def TemplateofCPTPDF(data, xHole, probeInf):
    projectNo = xHole.projectNo
    holeName = xHole.holeName
    holeDep = (len(xHole.points)) / 10
    probeNo = probeInf['probeNo']
    probeArea = probeInf['probeArea']
    fixedRatio = probeInf['fixedRatio']

    pagedata = [['单桥静力触探记录表', '', '', '', '', '', '', '', '', '']]
    pagedata.append(['工程编号', projectNo,
                     '孔          号', holeName,
                     '孔          深', '%.1f' % holeDep + 'm',
                     '探头编号', probeNo,
                     '测试日期', xHole.testDate]
                    )
    pagedata.append(['锥头面积', probeArea + 'cm2',
                     '标定系数', fixedRatio + 'kPa',
                     '', '', '', '', '', '']
                    )
    # 目的是空出一行，使得下划线与下一行的外框线不重合
    pagedata.append(['', '', '', '', '', '', '', '', '', ''])
    pagedata.append(['深度\n(m)', '比贯入阻力\nPs(MPa)',
                     '深度\n(m)', '比贯入阻力\nPs(MPa)',
                     '深度\n(m)', '比贯入阻力\nPs(MPa)',
                     '深度\n(m)', '比贯入阻力\nPs(MPa)',
                     '深度\n(m)', '比贯入阻力\nPs(MPa)']
                    )
    pagedata.extend(data)
    pagedata.append(['测          试',
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
    # TODO: Get this line right instead of just copying it from the docs
    style = TableStyle([('FONT', (0, 0), (-1, 0), 'SIMHEI', 20),
                        # ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),#内框
                        ('SPAN', (0, 0), (-1, 0)),
                        ('SPAN', (3, 2), (5, 2)),
                        ('FONT', (0, 1), (-1, 4), 'STSong-Light', 9.5),
                        ('FONT', (0, 5), (-1, -2), 'Times-Roman', 9),
                        ('FONT', (0, -1), (-1, -1), 'STSong-Light', 9.5),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('ALIGN', (1, 1), (1, 1), 'LEFT'),
                        ('ALIGN', (3, 1), (3, 1), 'LEFT'),
                        ('ALIGN', (5, 1), (5, 1), 'LEFT'),
                        ('ALIGN', (7, 1), (7, 1), 'LEFT'),
                        ('ALIGN', (-1, 1), (-1, 1), 'LEFT'),
                        ('ALIGN', (1, 2), (1, 2), 'LEFT'),
                        ('ALIGN', (3, 2), (5, 2), 'CENTER'),
                        ('LINEBELOW', (1, 1), (1, 1), 0.25, colors.black),
                        ('LINEBELOW', (3, 1), (3, 1), 0.25, colors.black),
                        ('LINEBELOW', (5, 1), (5, 1), 0.25, colors.black),
                        ('LINEBELOW', (7, 1), (7, 1), 0.25, colors.black),
                        ('LINEBELOW', (-1, 1), (-1, 1), 0.25, colors.black),
                        ('LINEBELOW', (1, 2), (1, 2), 0.25, colors.black),
                        ('LINEBELOW', (3, 2), (5, 2), 0.25, colors.black),
                        ('LINEBELOW', (0, 4), (-1, 4), 1.00, colors.black),
                        ('LINEBELOW', (1, -1), (2, -1), 0.25, colors.black),
                        ('LINEBELOW', (4, -1), (5, -1), 0.25, colors.black),
                        ('LINEBEFORE', (1, 4), (1, -2), 0.25, colors.black),
                        ('LINEBEFORE', (3, 4), (3, -2), 0.25, colors.black),
                        ('LINEBEFORE', (5, 4), (5, -2), 0.25, colors.black),
                        ('LINEBEFORE', (7, 4), (7, -2), 0.25, colors.black),
                        ('LINEBEFORE', (-1, 4), (-1, -2), 0.25, colors.black),
                        ('LINEAFTER', (1, 4), (1, -2), 1, colors.black),
                        ('LINEAFTER', (3, 4), (3, -2), 1, colors.black),
                        ('LINEAFTER', (5, 4), (5, -2), 1, colors.black),
                        ('LINEAFTER', (7, 4), (7, -2), 1, colors.black),
                        ('BOX', (0, 4), (-1, -2), 1.5, colors.black),  # 外边框
                        ])
    # Configure style and word wrap
    # t=Table(data,10*[1.75*cm],54*[0.5*cm])
    # colswidth,rowswidth can be list or tuple
    colswidth = []
    for i in range(5):
        colswidth.append(1.5 * cm)
        colswidth.append(2.0 * cm)
    rowswidth = [1.2 * cm, 0.6 * cm, 0.6 * cm, 0.2 * cm, 1.2 * cm]
    for i in range(50):
        rowswidth.append(0.41 * cm)
    rowswidth.append(0.6 * cm)
    t = Table(pagedata, colswidth, rowswidth)
    t.setStyle(style)
    return t
