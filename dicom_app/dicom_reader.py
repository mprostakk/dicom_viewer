import pydicom
from pydicom.data import get_testdata_files

from PIL import Image
from PyQt5.QtGui import QImage
import matplotlib.pyplot as plt


def convert_dicom_to_QImage(cv_img):
    height, width = cv_img.shape
    bytes_per_line = 3 * width
    q_img = QImage(cv_img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
    return q_img


def get_dicom(filename='CT_small.dcm'):
    files = get_testdata_files(filename)
    return files


def get_image_from_dicom(dicon_files, index):
    file = dicon_files[index]
    dataset = pydicom.dcmread(file)
    arr = dataset.pixel_array
    return arr
