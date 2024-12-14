import os
import subprocess
import requests
from zipfile import ZipFile
from tqdm import tqdm

# URLs for the dataset
DATA_URLS = {
    "train_images": "http://images.cocodataset.org/zips/train2017.zip",
    "val_images": "http://images.cocodataset.org/zips/val2017.zip",
    "stuff_annotations": "http://calvin.inf.ed.ac.uk/wp-content/uploads/data/cocostuffdataset/stuffthingmaps_trainval2017.zip"
}

# Directories
DOWNLOAD_DIR = "downloads"
IMAGE_DIR = "dataset/images"
ANNOTATION_DIR = "dataset/annotations"
REPO_URL = "https://github.com/nightrome/cocostuff.git"
REPO_DIR = "cocostuff"

def clone_repository():
    """Clone the COCO-Stuff repository."""
    if not os.path.exists(REPO_DIR):
        print(f"Cloning repository: {REPO_URL}")
        subprocess.run(["git", "clone", REPO_URL], check=True)
    else:
        print(f"Repository '{REPO_DIR}' already exists. Skipping clone.")

def download_file(url, dest_path):
    """Download a file with a progress bar."""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    with open(dest_path, 'wb') as file, tqdm(
        desc=os.path.basename(dest_path),
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            bar.update(len(data))
            file.write(data)

def download_datasets():
    """Download all datasets."""
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    for name, url in DATA_URLS.items():
        dest_path = os.path.join(DOWNLOAD_DIR, f"{name}.zip")
        if not os.path.exists(dest_path):
            print(f"Downloading {name}...")
            download_file(url, dest_path)
        else:
            print(f"{name} already downloaded. Skipping.")

def extract_datasets():
    """Extract all downloaded ZIP files."""
    os.makedirs(IMAGE_DIR, exist_ok=True)
    os.makedirs(ANNOTATION_DIR, exist_ok=True)

    # Extract train images
    train_zip = os.path.join(DOWNLOAD_DIR, "train_images.zip")
    with ZipFile(train_zip, 'r') as zip_ref:
        zip_ref.extractall(IMAGE_DIR)

    # Extract val images
    val_zip = os.path.join(DOWNLOAD_DIR, "val_images.zip")
    with ZipFile(val_zip, 'r') as zip_ref:
        zip_ref.extractall(IMAGE_DIR)

    # Extract stuff annotations
    stuff_zip = os.path.join(DOWNLOAD_DIR, "stuff_annotations.zip")
    with ZipFile(stuff_zip, 'r') as zip_ref:
        zip_ref.extractall(ANNOTATION_DIR)

def main():
    clone_repository()
    download_datasets()
    extract_datasets()
    print("Dataset download and extraction complete.")

if __name__ == "__main__":
    main()
