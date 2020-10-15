import sys
import os
import logging

from PyQt5 import QtWidgets
import matplotlib.pyplot as plt

import pydicom
from pydicom.data import get_testdata_files

from gui.main_window import DicomViewer


def test_dicom():
    filename = get_testdata_files('CT_small.dcm')[0]
    dataset = pydicom.dcmread(filename)
    plt.imshow(dataset.pixel_array, cmap=plt.cm.bone)
    plt.show()


if __name__ == '__main__':
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    logging.info('Starting Dicom Viewer')

    app = QtWidgets.QApplication(sys.argv)

    dicomViewer = DicomViewer()
    dicomViewer.show()

    sys.exit(app.exec_())

    # test_dicom()
