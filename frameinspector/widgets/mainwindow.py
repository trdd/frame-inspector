import glob
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
import fabio
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT as NavigationToolbar,
)
import numpy as np

from .MplWidget import MplCanvas
from ..models.imagestack import imageStack

matplotlib.use('Qt5Agg')





class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # create two textboxes for the filenames and file chooser button

        self.setWindowTitle("Frame Inspector")
        self.setGeometry(600,600, 1024, 800)
        self.createConfigGroupBox()

        self.btn_bottom.clicked.connect(self.getFileName)
        self.btn_top.clicked.connect(self.getFileName)

        self.le_top.returnPressed.connect(self.updateImg)
        self.le_bottom.returnPressed.connect(self.updateImg)

        self.le_clim_min.returnPressed.connect(self.updateClim)
        self.le_clim_max.returnPressed.connect(self.updateClim)

        self.sc = MplCanvas(self)

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.sc, self)

        layout_outer = QtWidgets.QVBoxLayout()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.sc)
        layout_outer.addLayout(layout)
        layout_outer.addStretch(1)
        layout_outer.addWidget(self.configGroupBox)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout_outer)
        self.setCentralWidget(widget)

        self.imgstack_top = imageStack()
        self.imgstack_bottom = imageStack()
        self.imgstack_diff = imageStack()

        self.show()

    def createConfigGroupBox(self):
        self.le_clim_max = QtWidgets.QLineEdit("500")
        self.le_clim_max.setValidator(QtGui.QIntValidator())
        self.le_clim_min = QtWidgets.QLineEdit("0")
        self.le_clim_min.setValidator(QtGui.QIntValidator())
        self.le_top  = QtWidgets.QLineEdit("")
        self.le_top.setDragEnabled(True)
        self.le_bottom  = QtWidgets.QLineEdit("")
        self.le_bottom.setDragEnabled(True)
        self.btn_top = QtWidgets.QPushButton('open')
        self.btn_bottom = QtWidgets.QPushButton('open')
        self.configGroupBox = QtWidgets.QGroupBox("settings")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(QtWidgets.QLabel("cmin"), 0, 0, 1, 1)
        layout.addWidget(QtWidgets.QLabel("cmax"), 0, 2, 1, 1)
        layout.addWidget(self.le_clim_min, 0, 1, 1, 1)
        layout.addWidget(self.le_clim_max, 0, 3, 1, 1)
        layout.addWidget(QtWidgets.QLabel(("Filepattern for frame_1"
            +" axes (wildcards like * allowed)")), 1, 0, 1, 5)
        layout.addWidget(QtWidgets.QLabel(("Filepattern for frame_2" 
            +" axes (wildcards like * allowed)")), 3, 0, 1, 5)
        layout.addWidget(self.le_top, 2, 0, 1, 4)
        layout.addWidget(self.le_bottom, 4, 0, 1, 4)
        layout.addWidget(self.btn_top, 2, 5, 1, 1)
        layout.addWidget(self.btn_bottom, 4, 5, 1, 1)
        self.configGroupBox.setLayout(layout)

    def getFileName(self):
        sender = self.sender()
        fn, other = QtWidgets.QFileDialog.getOpenFileName(self)
        if sender == self.btn_top:
            self.le_top.setText(fn)
        else:
            self.le_bottom.setText(fn)
    def updateImg(self):
        sender = self.sender()
        if sender== self.le_top:
            self.imgstack_top.load(self.le_top.text().strip())
            self.sc.axes[0].imshow(self.imgstack_top.get_sum())
        elif sender== self.le_bottom:
            self.imgstack_bottom.load(self.le_bottom.text().strip())
            self.sc.axes[1].imshow(self.imgstack_bottom.get_sum())
        if (len(self.imgstack_top.fns) > 0) and (len(self.imgstack_bottom.fns) > 0):
            difference = self.imgstack_top.get_sum() - self.imgstack_bottom.get_sum()
            self.sc.axes[2].imshow(difference, cmap=plt.cm.seismic_r)
        self.updateClim()
        self.sc.draw()
    def updateClim(self):
        for a in self.sc.axes[:2]:
            if len(a.images) > 0:
                a.images[-1].set_clim(int(self.le_clim_min.text()),
                        int(self.le_clim_max.text()))
        if len(self.sc.axes[2].images) > 0:
            self.sc.axes[2].images[-1].set_clim(-int(self.le_clim_max.text()),
                    int(self.le_clim_max.text()))
        self.sc.draw()




