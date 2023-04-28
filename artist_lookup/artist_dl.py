import subprocess
from pathlib import Path
from tqdm import tqdm


def read_handles(file_path: str) -> list:
    with open(file_path, "r", encoding="utf-8") as f:
        handles = [line.strip() for line in f.readlines()]
    return handles


def run_gallery_dl(handle: str):
    url = f"https://twitter.com/{handle}/media"
    command = f"gallery-dl {url} --mtime-from-date --write-metadata  --write-info-json"

    # Change directory to D:
    subprocess.Popen("D:", shell=True)

    # Run gallery-dl
    subprocess.run(command, shell=True)


if __name__ == "__main__":
    file_path = "./bin/twitter-following-z3zz4.txt"
    handles = read_handles(file_path)

    for handle in tqdm(handles, desc="Downloading media"):
        run_gallery_dl(handle)
