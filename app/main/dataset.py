import pymssql


class MSSQL:
    def __init__(self, name='shmged', host="192.168.0.5", user="sa", pwd="58308215", db="shgeodb"):
        self.name = name
        if isinstance(self.name, type(None)):
            raise(NameError, "No setting database's name")
        elif type(self.name) != str:
            raise(NameError, "arg type is erro!")
        else:
            self.host = host
            self.user = user
            self.pwd = pwd
            self.db = db

    def __GetConnect(self):
        if not self.db:
            raise(NameError, "No setting database's information")
        self.conn = pymssql.connect(host=self.host,
                                    user=self.user,
                                    password=self.pwd,
                                    database=self.db,
                                    charset="utf8"
                                    )
        cur = self.conn.cursor()
        if not cur:
            raise(NameError, "Connection database raises Erro!")
        else:
            return cur

    def ExecQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()
        self.conn.close()
        return resList

    def ExecNonQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()
