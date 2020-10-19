import logging

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from PyQt5.QtWidgets import QMainWindow, QPushButton, QFileDialog
from skimage import measure

from .object_factory import create_slider, create_layout, \
    create_menu, create_actions, create_widget
from dicom_app.dicom_reader import DicomReader


class DicomViewer(QMainWindow):
    def __init__(self):
        super(DicomViewer, self).__init__()

        self.dicom_reader = DicomReader()
        self.layout = create_layout()

        self.opened_directory: str = ''

        # subplots
        self.axial = None
        self.sagittal = None
        self.coronal = None

        # sliders
        self.x_slider = create_slider(self, self.x_slider_change_value)
        self.y_slider = create_slider(self, self.y_slider_change_value)
        self.z_slider = create_slider(self, self.z_slider_change_value)
        self.layout.addWidget(self.x_slider)
        self.layout.addWidget(self.y_slider)
        self.layout.addWidget(self.z_slider)

        # images
        self.figure_axial = Figure()
        self.figure_sagittal = Figure()
        self.figure_coronal = Figure()
        self.canvas_axial = FigureCanvas(self.figure_axial)
        self.canvas_sagittal = FigureCanvas(self.figure_sagittal)
        self.canvas_coronal = FigureCanvas(self.figure_coronal)
        self.layout.addWidget(self.canvas_axial)
        self.layout.addWidget(self.canvas_sagittal)
        self.layout.addWidget(self.canvas_coronal)

        # plot Button
        self.plot_button = QPushButton()
        self.plot_button.clicked.connect(self.plot)
        self.layout.addWidget(self.plot_button)

        # 3d plot button
        self.plot_button_3d = QPushButton()
        self.plot_button_3d.clicked.connect(self.plot_3d)
        self.layout.addWidget(self.plot_button_3d)

        main_widget = create_widget()
        main_widget.setLayout(self.layout)
        self.setCentralWidget(main_widget)

        self.action_exit, self.action_open_directory = create_actions(self)
        self.menuBar().addMenu(create_menu(self))

        self.setWindowTitle("Dicom Viewer")
        self.setMinimumWidth(1240)
        self.setMinimumHeight(720)

    def plot(self) -> None:
        """Plot 3 axes of 3d image.

        If path to directory with .dcm files is not provided, do nothing.

        Returns:
            None.
        """

        self.dicom_reader.load_from_directory(self.opened_directory)

        self.figure_axial.clear()
        self.figure_sagittal.clear()
        self.figure_coronal.clear()

        self.axial = self.figure_axial.add_subplot(111)
        self.sagittal = self.figure_sagittal.add_subplot(111)
        self.coronal = self.figure_coronal.add_subplot(111)

        self.axial.imshow(self.dicom_reader.image_3d[:, :, 0])
        self.sagittal.imshow(self.dicom_reader.image_3d[:, 0, :])
        self.coronal.imshow(self.dicom_reader.image_3d[0, :, :].T)

        self.axial.set_aspect(self.dicom_reader.axial_aspect)
        self.sagittal.set_aspect(self.dicom_reader.sagittal_aspect)
        self.coronal.set_aspect(self.dicom_reader.coronal_aspect)

        self.x_slider.setRange(0, self.dicom_reader.image_shape[2] - 1)
        self.y_slider.setRange(0, self.dicom_reader.image_shape[1] - 1)
        self.z_slider.setRange(0, self.dicom_reader.image_shape[0] - 1)

        self.canvas_axial.draw()
        self.canvas_sagittal.draw()
        self.canvas_coronal.draw()

    def plot_3d(self) -> None:
        self.figure_axial.clear()

        threshold = 300
        image_3d_transposed = self.dicom_reader.image_3d.transpose(2, 1, 0)
        vertices, faces, normals, values = \
            measure.marching_cubes(image_3d_transposed, threshold)

        self.axial = self.figure_ax.add_subplot(111, projection='3d')
        mesh = Poly3DCollection(vertices[faces], alpha=0.1)
        face_color = [0.4, 0.4, 1]
        mesh.set_facecolor(face_color)

        self.axial.add_collection3d(mesh)
        self.axial.set_xlim(0, image_3d_transposed.shape[0])
        self.axial.set_ylim(0, image_3d_transposed.shape[1])
        self.axial.set_zlim(0, image_3d_transposed.shape[2])

        self.canvas_ax.draw()

    def on_exit(self) -> None:
        logging.info('Closing Dicom Viewer')
        self.close()

    def on_directory_open(self) -> None:
        directory = str(QFileDialog.getExistingDirectory(self, "Select directory"))
        logging.info(f'Selected directory: {directory}')
        self.opened_directory = directory
        if self.opened_directory:
            self.plot()

    def x_slider_change_value(self, value) -> None:
        self.axial.imshow(self.dicom_reader.image_3d[:, :, value])

        self.canvas_axial.draw()

    def y_slider_change_value(self, value) -> None:
        self.sagittal.imshow(self.dicom_reader.image_3d[:, value, :])

        self.canvas_sagittal.draw()

    def z_slider_change_value(self, value) -> None:
        self.coronal.imshow(self.dicom_reader.image_3d[value, :, :])

        self.canvas_coronal.draw()
