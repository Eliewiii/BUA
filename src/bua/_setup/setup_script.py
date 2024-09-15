import os
import urllib.request
from zipfile import ZipFile
import sys

# todo : import paths from config

# todo : overwrite the machine files/folders/data not the main one, but keep the user data and
def check_user_deprecated_structure(folder):
    """Check if the folder has a deprecated structure."""
    if not os.path.exists(folder):
        return False

    # Example check: look for an outdated file or folder
    outdated_file = os.path.join(folder, 'deprecated_file.txt')  # Example deprecated file
    if os.path.exists(outdated_file):
        print(f"Warning: Deprecated structure detected in {folder}.")
        print("Please update the structure or migrate your data.")
        return True

    return False

def download_file(url, destination):
    print(f"Downloading from {url} to {destination}...")
    try:
        urllib.request.urlretrieve(url, destination)
        print(f"Downloaded to {destination}")
    except Exception as e:
        print(f"Failed to download file. Error: {e}")

def unzip_file(zip_path, extract_to):
    print(f"Unzipping {zip_path} to {extract_to}...")
    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extraction complete. Contents extracted to {extract_to}")

def setup_package():
    target_directory = os.path.expanduser("~/.your_package_data")
    zip_url = "https://example.com/path/to/your/file.zip"
    zip_file_path = os.path.join(target_directory, "file.zip")

    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
        print(f"Created directory {target_directory}")

    download_file(zip_url, zip_file_path)
    unzip_file(zip_file_path, target_directory)


def setup_package():
    print("zob zob")

if __name__ == "__main__":
    setup_package()
    # if 'setup' in sys.argv:
