__author__ = 'gaspardzul'


#! /usr/bin/env python
# -*- coding: utf-8 -*-

from app.damfaraUI import *


def main():
    app = QtGui.QApplication(sys.argv)
    damfara = MainUI()
    damfara.run()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()