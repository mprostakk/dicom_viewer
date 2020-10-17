import pydicom
from pydicom.data import get_testdata_files

    def load_dicom_files(self, directory: str) -> tp.List[pydicom.FileDataset]:
        files = []
        for file_name in glob.glob(directory, recursive=False):
            logging.info(file_name)
            files.append(pydicom.dcmread(file_name))

        files = list(filter(lambda file: hasattr(file, 'SliceLocation'), files))
        files = list(sorted(files, key=lambda file: file.SliceLocation))

        return files


def get_image_from_dicom(dicom_files, index):
    file = dicom_files[index]
    dataset = pydicom.dcmread(file)
    arr = dataset.pixel_array
    return arr
