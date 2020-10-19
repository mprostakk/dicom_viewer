import os
import glob
import logging
import typing as tp

import pydicom
import numpy as np


class DicomReader:
    def __init__(self):
        self.last_dir = ''
        self.image_3d = None
        self.image_shape = None
        self.axial_aspect = 0
        self.sagittal_aspect = 0
        self.coronal_aspect = 0

    def load_from_directory(self, directory: str) -> None:
        self.create_3d_array(self._load_from_directory(directory))

    @staticmethod
    def _load_from_directory(directory: str) -> tp.List[pydicom.FileDataset]:
        dicom_files_path = os.path.join(directory, '*.dcm')
        files = []
        for file_name in glob.glob(dicom_files_path, recursive=False):
            logging.info(file_name)
            files.append(pydicom.dcmread(file_name))

        files = list(filter(lambda file: hasattr(file, 'SliceLocation'), files))
        files = list(sorted(files, key=lambda file: file.SliceLocation))

        return files

    def create_3d_array(self, slices: tp.List) -> None:
        # calculate pixel aspects
        pixel_spacing = slices[0].PixelSpacing
        slice_thickness = slices[0].SliceThickness
        self.axial_aspect = pixel_spacing[1] / pixel_spacing[0]
        self.sagittal_aspect = pixel_spacing[1] / slice_thickness
        self.coronal_aspect = slice_thickness / pixel_spacing[0]

        # create 3D array
        self.image_shape = list(slices[0].pixel_array.shape)
        self.image_shape.append(len(slices))
        self.image_3d = np.zeros(self.image_shape)
        for i, image_slice in enumerate(slices):
            self.image_3d[:, :, i] = image_slice.pixel_array
