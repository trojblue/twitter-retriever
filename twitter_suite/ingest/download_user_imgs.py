import subprocess
from pathlib import Path
from tqdm import tqdm


def read_handles(file_path: str) -> list:
    with open(file_path, "r", encoding="utf-8") as f:
        handles = [line.strip() for line in f.readlines()]
    return handles


def run_gallery_dl(handle: str, dst_dir: str = ""):
    url = f"https://twitter.com/{handle}/media"
    command = f"gallery-dl {url} --mtime-from-date --write-metadata  --write-info-json"
    if dst_dir:
        command += f" --dest {dst_dir}"

    # Change directory to D:
    subprocess.Popen("D:", shell=True)

    # Run gallery-dl
    subprocess.run(command, shell=True)


def download_users(txt_path: str, dst_dir: str = ""):
    """从txt文件中读取twitter handle, 并使用gallery-dl下载用户的media"""
    handles = read_handles(txt_path)
    progress_bar = tqdm(handles, unit="user")
    print(f"Downloading media for {len(handles)} users.")

    for handle in progress_bar:
        progress_bar.set_description(f"Downloading media for {handle}")
        run_gallery_dl(handle, dst_dir)


if __name__ == "__main__":
    file_path = "./bin/twitter-following-aisiteruekaki.txt-z3zz4.txt"
    download_users(file_path)
