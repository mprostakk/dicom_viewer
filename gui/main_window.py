import cv2
import numpy as np
import logging
import threading

from PyQt5.QtWidgets import QMainWindow, QFileDialog

from .object_factory import create_slider, create_layout, \
    create_menu, create_actions, create_widget
from dicom_app.dicom_reader import DicomReader
from gui.QtImageViewer import QtImageViewer

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

        self.image_frame_x = QtImageViewer()
        self.image_frame_y = QtImageViewer()
        self.image_frame_z = QtImageViewer()
        self.image_frame_x.aspectRatioMode = QtCore.Qt.KeepAspectRatio
        self.image_frame_y.aspectRatioMode = QtCore.Qt.KeepAspectRatio
        self.image_frame_z.aspectRatioMode = QtCore.Qt.KeepAspectRatio
        self.layout.addWidget(self.image_frame_x)
        self.layout.addWidget(self.image_frame_y)
        self.layout.addWidget(self.image_frame_z)

        self.brightness: int = 0
        self.brightness_slider = create_slider(self, self.brightness_slider_change_value)
        self.layout.addWidget(self.brightness_slider)

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

        # self.image_frame_x.setMovie(self.movie)
        # self.image_frame_y.setMovie(self.movie)
        # self.image_frame_z.setMovie(self.movie)

        # self.movie.start()

        # t = threading.Thread(target=self.open_directory)
        # t.start()

        self.open_directory()

    def open_directory(self) -> None:
        if self.opened_directory:
            self.dicom_reader.load_from_directory(self.opened_directory)
            self.x_slider.setRange(0, self.dicom_reader.image_shape[2] - 1)
            self.y_slider.setRange(0, self.dicom_reader.image_shape[1] - 1)
            self.z_slider.setRange(0, self.dicom_reader.image_shape[0] - 1)

            self.x_slider_change_value(0)
            self.y_slider_change_value(0)
            self.z_slider_change_value(0)

            self.brightness_slider.setValue(50)
        else:
            pass
            # self.image_frame_x.clear()
            # self.image_frame_y.clear()
            # self.image_frame_z.clear()

        # self.movie.stop()

    def brightness_slider_change_value(self, value) -> None:
        self.brightness = int((value - 50) * 2)
        self.update_frames()

    def x_slider_change_value(self, value) -> None:
        self.image_x = self.dicom_reader.image_3d[:, :, value]
        self.update_x()

    def y_slider_change_value(self, value) -> None:
        self.image_y = self.dicom_reader.image_3d[:, value, :]
        self.update_y()

    def z_slider_change_value(self, value) -> None:
        self.image_z = self.dicom_reader.image_3d[value, :, :].T
        self.update_z()

    def update_frames(self):
        self.update_x()
        self.update_y()
        self.update_z()

    def update_x(self):
        self.image_x_qt = self.get_qt_image(self.image_x)
        self.image_frame_x.setImage(self.image_x_qt)

    def update_y(self):
        self.image_y_qt = self.get_qt_image(self.image_y)
        self.image_frame_y.setImage(self.image_y_qt)

    def update_z(self):
        self.image_z_qt = self.get_qt_image(self.image_z)
        self.image_frame_z.setImage(self.image_z_qt)

    def get_qt_image(self, image_) -> QtGui.QImage:
        h, w = image_.shape
        image = image_.copy()
        image_max = np.amax(image)
        image_min = np.amin(image)
        m = 1.0 / (image_max - image_min)
        m *= 255
        image = image * m
        image = np.require(image, np.uint8, 'C')

        image = self.add_brightness_to_image(image)

        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        image = QtGui.QImage(
            image.data, w, h, w * 3,
            QtGui.QImage.Format_RGB888).rgbSwapped()

        return image

    def add_brightness_to_image(self, image):
        cv2.add(image, self.brightness, image)
        return image
