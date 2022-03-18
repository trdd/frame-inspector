import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from .widgets.mainwindow import MainWindow

def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    app.exec_()
