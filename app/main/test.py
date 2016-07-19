# -*- coding: utf_8 -*-
# import sqlite3
#
# db = "e:/Pythonweb/project_code/fernando/app/database/fernando.db"
# sql = "select project_name, project_nameing from base"
# conn = sqlite3.connect(db)
# conn.text_factory = lambda x: x.decode('latin-1')
# cur = conn.cursor()
# res = cur.execute(sql).fetchall()
# cur.close()
# conn.close()
# for projectNo, projectName in res:
#     print(projectName.encode('latin-1').decode('gbk'))