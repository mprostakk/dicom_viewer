import cv2
import numpy as np
import logging
import threading

from PyQt5.QtWidgets import QMainWindow, QFileDialog

from .object_factory import create_slider, create_layout, \
    create_menu, create_actions, create_widget
from dicom_app.dicom_reader import DicomReader

from PyQt5 import QtGui, QtCore, QtWidgets


class DicomViewer(QMainWindow):
    def __init__(self):
        super(DicomViewer, self).__init__()

        self.dicom_reader = DicomReader()
        self.layout = create_layout()

        self.opened_directory: str = ''

        self.movie = QtGui.QMovie('gui/loading.gif')

        # sliders
        self.x_slider = create_slider(self, self.x_slider_change_value)
        self.y_slider = create_slider(self, self.y_slider_change_value)
        self.z_slider = create_slider(self, self.z_slider_change_value)
        self.layout.addWidget(self.x_slider)
        self.layout.addWidget(self.y_slider)
        self.layout.addWidget(self.z_slider)

        self.image_frame_x = QtWidgets.QLabel()
        self.image_frame_y = QtWidgets.QLabel()
        self.image_frame_z = QtWidgets.QLabel()
        self.layout.addWidget(self.image_frame_x)
        self.layout.addWidget(self.image_frame_y)
        self.layout.addWidget(self.image_frame_z)

        main_widget = create_widget()
        main_widget.setLayout(self.layout)
        self.setCentralWidget(main_widget)

        self.action_exit, self.action_open_directory = create_actions(self)
        self.menuBar().addMenu(create_menu(self))

        self.setWindowTitle("Dicom Viewer")
        self.setMinimumWidth(1240)
        self.setMinimumHeight(720)

    def on_exit(self) -> None:
        logging.info('Closing Dicom Viewer')
        self.close()

    def on_directory_open(self) -> None:
        directory = str(QFileDialog.getExistingDirectory(self, "Select directory"))
        logging.info(f'Selected directory: {directory}')
        self.opened_directory = directory

        self.image_frame_x.setMovie(self.movie)
        self.image_frame_y.setMovie(self.movie)
        self.image_frame_z.setMovie(self.movie)

        self.movie.start()

        t = threading.Thread(target=self.open_directory)
        t.start()

    def open_directory(self) -> None:
        if self.opened_directory:
            self.dicom_reader.load_from_directory(self.opened_directory)
            self.x_slider.setRange(0, self.dicom_reader.image_shape[2] - 1)
            self.y_slider.setRange(0, self.dicom_reader.image_shape[1] - 1)
            self.z_slider.setRange(0, self.dicom_reader.image_shape[0] - 1)

            self.x_slider_change_value(0)
            self.y_slider_change_value(0)
            self.z_slider_change_value(0)

        else:
            self.image_frame_x.clear()
            self.image_frame_y.clear()
            self.image_frame_z.clear()

        self.movie.stop()

    def x_slider_change_value(self, value) -> None:
        self.image = self.dicom_reader.image_3d[:, :, value]

        h, w = self.image.shape
        self.image = self.image.copy()

        image_max = np.amax(self.image)
        image_min = np.amin(self.image)
        m = 1.0 / (image_max - image_min)
        m *= 255

        self.image = self.image * m
        self.image = np.require(self.image, np.uint8, 'C')
        self.image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2RGB)
        self.image = QtGui.QImage(self.image.data, w, h, w * 3,
                                  QtGui.QImage.Format_RGB888).rgbSwapped()
        self.image_frame_x.setPixmap(QtGui.QPixmap.fromImage(self.image))

    def y_slider_change_value(self, value) -> None:
        self.image = self.dicom_reader.image_3d[:, value, :]

        h, w = self.image.shape
        self.image = self.image.copy()

        image_max = np.amax(self.image)
        image_min = np.amin(self.image)
        m = 1.0 / (image_max - image_min)
        m *= 255

        self.image = self.image * m
        self.image = np.require(self.image, np.uint8, 'C')
        self.image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2RGB)
        self.image = QtGui.QImage(self.image.data, w, h, w * 3,
                                  QtGui.QImage.Format_RGB888).rgbSwapped()
        self.image_frame_y.setPixmap(QtGui.QPixmap.fromImage(self.image))

    def z_slider_change_value(self, value) -> None:
        self.image = self.dicom_reader.image_3d[value, :, :].T

        h, w = self.image.shape
        self.image = self.image.copy()

        image_max = np.amax(self.image)
        image_min = np.amin(self.image)
        m = 1.0 / (image_max - image_min)
        m *= 255

        self.image = self.image * m
        self.image = np.require(self.image, np.uint8, 'C')
        self.image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2RGB)
        self.image = QtGui.QImage(self.image.data, w, h, w * 3,
                                  QtGui.QImage.Format_RGB888).rgbSwapped()
        self.image_frame_z.setPixmap(QtGui.QPixmap.fromImage(self.image))
