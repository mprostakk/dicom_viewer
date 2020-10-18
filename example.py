import os
import sys
import gdown
import zipfile


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DICOM_FILE = os.path.join(BASE_DIR, 'dicom.zip')
DICOM_ZIP_URL = 'https://drive.google.com/uc?id=1rvyplB7gEoJ-8kzSDuYJg-Dg_NZY6Pr5'
DICOM_DEST_DIRECTORY = os.path.join(BASE_DIR, 'example')


def check_if_destination_directory_exists() -> None:
    if os.path.exists(DICOM_DEST_DIRECTORY):
        print('Directory example/ already exists!')
        sys.exit(1)


def download_dicom_zip() -> None:
    gdown.download(DICOM_ZIP_URL, DICOM_FILE, quiet=False)
    print('Downloaded dicom.zip file')


def unpack_dicom_zip_file():
    with zipfile.ZipFile(DICOM_FILE, 'r') as zip_ref:
        zip_ref.extractall(DICOM_DEST_DIRECTORY)
        print(f'Extracted dicom.zip file to {DICOM_DEST_DIRECTORY}')


def remove_dicom_zip_file():
    if os.path.exists(DICOM_FILE):
        os.remove(DICOM_FILE)
        print(f'Removed dicom.zip')


if __name__ == '__main__':
    check_if_destination_directory_exists()
    download_dicom_zip()
    unpack_dicom_zip_file()
    remove_dicom_zip_file()
    print('Finished!')
