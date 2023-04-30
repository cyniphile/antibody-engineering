import requests
from prefect import task, flow
from prefect.tasks import task_input_hash
from utils import DATA_PATH
import shutil
import logging


URLS = [
    "https://zenodo.org/record/5095284/files/mit-ll/AlphaSeq_Antibody_Dataset-v1.0.0.zip?download=1"
]


@task(cache_key_fn=task_input_hash)  # type: ignore
def save_file_locally(url: str, path: str) -> str:
    data = requests.get(url).content
    filename = url.split("/")[-1]
    filepath = path + filename
    with open(filepath, "wb") as f:
        f.write(data)
        logging.info(f"Downloaded {filename} to {path}")
    return filepath


@flow
def download_files(urls=URLS, path: str = DATA_PATH):
    for url in urls:
        filepath = save_file_locally(url, path)
        if filepath[-4:] == ".zip":  # type: ignore
            filename = url.split("/")[-1]
            shutil.unpack_archive(filepath, path)  # type: ignore
            logging.info(f"Unzipped {filename} to {path}")


if __name__ == "__main__":
    download_files()
