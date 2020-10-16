import pydicom
from pydicom.data import get_testdata_files


def get_dicom(filename='CT_small.dcm'):
    files = get_testdata_files(filename)
    return files


def get_image_from_dicom(dicom_files, index):
    file = dicom_files[index]
    dataset = pydicom.dcmread(file)
    arr = dataset.pixel_array
    return arr
