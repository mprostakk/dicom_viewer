import sys
import logging
import numpy as np


from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QLabel, QScrollArea, QHBoxLayout, QMenu, QWidget, QSizePolicy, QApplication, QMainWindow, QSlider, QHBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvas

from dicom_app import dicom_reader
from matplotlib.figure import Figure

class DicomViewer(QMainWindow):

    file_menu: QMenu

    test_action: QAction
    action_exit: QAction

    def __init__(self):
        super(DicomViewer, self).__init__()
        self.test_dicom = dicom_reader.get_dicom()
        self.initUI()

    def initUI(self):

        layout = QHBoxLayout()

        # slider
        sld = QSlider(Qt.Vertical, self)
        sld.setGeometry(40, 30, 30, 200)
        sld.setRange(0, 100) # len(self.test_dicom)
        sld.valueChanged[int].connect(self.changeValue)
        layout.addWidget(sld)

        # Label with number
        self.label = QLabel("0", self)
        self.label.setStyleSheet('QLabel { background: #007AA5; border-radius: 3px;}')
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.label.setMinimumWidth(80)
        layout.addWidget(self.label)

        # image
        self.figure = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.subplots()
        self.ax.imshow(dicom_reader.get_image_from_dicom(self.test_dicom, 0))
        self.ax.set_axis_off()
        layout.addWidget(self.canvas)

        # widget
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.create_actions()
        self.create_menu()

        self.setWindowTitle("Dicom Viewer")
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

    def changeValue(self, value):
        # print(str(value))
        # self.ax.imshow(dicom_reader.get_image_from_dicom(self.test_dicom, value))
        self.label.setText(str(value))

    def create_actions(self):
        self.test_action = QAction("&Test...", self, shortcut="Ctrl+T", triggered=self.test)
        self.action_exit = QAction("&Exit...", self, shortcut="Alt+F4", triggered=self.on_exit)

    def create_menu(self):
        self.file_menu = QMenu("&File", self)
        self.file_menu.addAction(self.test_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.action_exit)

        self.menuBar().addMenu(self.file_menu)

    def test(self):
        logging.info('Test')

    def on_exit(self):
        logging.info('Closing Dicom Viewer')
        self.close()

