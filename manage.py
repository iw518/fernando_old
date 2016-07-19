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
from flask_script import Manager, Shell, Server

from app import create_app


def make_shell_context():
    return dict(app=app)

app = create_app('default')
manager = Manager(app)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("runserver",
                    Server(host="127.0.0.1", port=80, use_debugger=True))

if __name__ == '__main__':
    manager.run()
