# -*-coding:utf-8-*-
# -------------------------------------------------------------------------------
# Name:        auth
# Purpose:     audit userlogin and projectNO
#
# Author:      Robot of Fernando
#
# Created:     17-06-2015
# Copyright:   (c) Robot of Fernando 2015
# Licence:     The MIT License
# -------------------------------------------------------------------------------
import struct

from .dataset import *


class Manager():
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def find(self):
        return None


def FindUser(user, pwd):
    sql_str = "SELECT PassWord FROM userPass Where userName='%s'" % (user)
    ms = MSSQL()
    sqlList = ms.ExecQuery(sql_str)
    if len(sqlList) > 0:
        buff = sqlList[0][0]
        PassWord = ''
        for i in range(0, len(buff), 1):
            ps = (struct.unpack('s', buff[i:i + 1])[0]).decode('gbk')
            PassWord += ps
        if pwd == PassWord:
            print('Success!')
            return user
        else:
            pwd = input('密码不对,请重新输入密码:')
            return FindUser(user, pwd)
    else:
        user = input('无此用户，请重新输入用户名:')
        pwd = input('请输入密码:')
        return FindUser(user, pwd)


def Login():
    user = input('请输入用户名:')
    pwd = input('请输入密码:')
    return FindUser(user, pwd)


def FindManager(projectNo):
    sql_str = "SELECT userPass.userName,userPass.userXinMing \
                FROM (userprj INNER JOIN base ON userprj.project_count = base.project_count) \
                INNER JOIN userPass ON userPass.userName=userprj.userName \
                Where base.project_name='%s' AND userprj.project_burden=0" % (projectNo)
    ms = MSSQL()
    sqlList = ms.ExecQuery(sql_str)
    if len(sqlList) == 0:
        sqlList = [("", "", "")]
    manager = Manager(sqlList[0][0].encode('latin-1').decode('gbk'), sqlList[0][1].encode('latin-1').decode('gbk'))
    return manager


def FindProject(user):
    sql_str = "SELECT userprj.project_Name, base.project_nameing FROM userprj INNER JOIN base ON userprj.project_count = base.project_count Where userName='%s'" % (user)
    ms = MSSQL()
    sqlList = ms.ExecQuery(sql_str)
    print('-' * 80)
    print(len(sqlList))
    for (projectNo, projectName) in sqlList:
        if projectName is not None:
            print("%s\t%s" % (projectNo.encode('latin-1').decode('gbk'), projectName.encode('latin-1').decode('gbk')))
        else:
            '部分项目名称可能为空'
            print("%s\t%s" % (projectNo.encode('latin-1').decode('gbk'), ''))
    print('-' * 80)
    return sqlList


def CheckProjectNo(user, projectNo, projectList):
    if projectNo in [item[0] for item in projectList]:
        return projectNo
    else:
        print('输入的工程编号有误,请重新输入:')
        projectNo = input('请输入工程编号：')
        '''若递归函数有显式返回值，则每一个选择分支均要由显式返回值,
        因为当递归结束时，还会执行分支后隐含的return None
        此外若return 其他值时，仅会递归一次'''
        return CheckProjectNo(user, projectNo, projectList)
