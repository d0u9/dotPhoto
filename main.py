#!/usr/bin/env python

import sys
from ApplicationCls import Application

import GlobalVar as gVar

if __name__ == '__main__':
    app = Application(sys.argv)
    gVar.SignalConnection()
    sys.exit(app.exec_())
