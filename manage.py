#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------------------
# version:      ??
# author:       fernando
# license:      MIT License
# contact:      iw518@163.com
# purpose:      manager
# date:         2016-07-19
# copyright:    copyright  2016 Xu, Aiwu
# -------------------------------------------------------------------------------
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell, Server

from app import create_app, db


def make_shell_context():
    return dict(app=app, db=db)

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("runserver",
                    Server(host="0.0.0.0", port=80, use_debugger=True))
manager.add_command('db', MigrateCommand)
if __name__ == '__main__':
    manager.run()
