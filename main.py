#!/usr/bin/env python

import sys
from ApplicationCls import Application

if __name__ == '__main__':
    app = Application(sys.argv)
    sys.exit(app.exec_())
