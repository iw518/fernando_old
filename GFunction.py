#-*-coding:utf-8-*-
#-------------------------------------------------------------------------------
# Name:        GFunction
# Purpose:
#
# Author:      Robot of Fernando
#
# Created:     17-06-2015
# Copyright:   (c) Administrator 2015
# Licence:     <GPLV3>
#-------------------------------------------------------------------------------

def Matchlist(x,xlist):
    list0=[]
    if x<=xlist[0][0]:
        return xlist[0][1]
    elif x>=xlist[-1][0]:
        return xlist[-1][1]
    else:
        for i in range(len(xlist)):
            if x==xlist[i][0]:
                return xlist[i][1]
            elif x<=xlist[i+1][0]:
                for j in range(len(xlist[i][1])):
                    y=(xlist[i+1][1][j]-xlist[i][1][j])/(xlist[i+1][0]-xlist[i][0])*(x-xlist[i][0])+xlist[i][1][j]
                    list0.append(y)
                return list0
def AddDate(xDate,num=1):
    newDate=xDate.replace('.','-').replace('/','-')
    xlist=newDate.split('-')
    if len(xlist)<3:
        return newDate
    else:
        year=int(xlist[0])
        month=int(xlist[1])
        day=int(xlist[2])+num
        if month==2:
            if day>28:
                day=1
                month=month+1
        elif month in [4,6,9,11]:
            if day>30:
                day=1
                month=month+1
        elif month in [1,3,5,7,8,12]:
            if day>31:
                day=1
                month=month+1
            if month>12:
                month=1
                year=year+1
        return '{year}-{month}-{day}'.format(year=year,month=month,day=day)

