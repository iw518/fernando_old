# -*- coding: utf_8 -*-
import sqlite3

DATABASE = "E:/Pythonweb/py344/project_code/fernando/database/fernando.db"


class Sql3:
    """docstring for ClassName"""

    def __init__(self):
        self.db = DATABASE

    def __GetConnect(self):
        if not self.db:
            raise(NameError, "No setting database's information")
        self.conn = sqlite3.connect(self.db)
        self.conn.text_factory = lambda x: x.decode('latin-1')
        cur = self.conn.cursor()
        if not cur:
            raise(NameError, "Connection database raises Erro!")
        else:
            return cur

    def ExecQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()
        cur.close()
        self.conn.close()
        return resList

    def ExecNonQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        cur.close()
        self.conn.close()
