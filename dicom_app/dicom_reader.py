import pydicom
from pydicom.data import get_testdata_files

from PIL import Image
from PyQt5.QtGui import QImage
import matplotlib.pyplot as plt


def convert_dicom_to_QImage(cvImg):
    height, width = cvImg.shape
    bytesPerLine = 3 * width
    qImg = QImage(cvImg.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
    return qImg


def get_dicom(filename='CT_small.dcm'):
    files = get_testdata_files(filename)
    return files


def get_image_from_dicom(dicon_files, index):
    file = dicon_files[index]
    dataset = pydicom.dcmread(file)
    arr = dataset.pixel_array
    return arr
