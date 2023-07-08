import os
import shutil
from pathlib import Path
from tqdm import tqdm

"""
移动json和txt文件到![json]文件夹下的对应子文件夹
方便在windows文件夹里筛图
"""
def move_json_txts(dir_str: str):
    root_directory = Path(dir_str)
    json_folder = root_directory / Path("![json]")

    # Get a list of all subdirectories
    subdirs = [subdir for subdir in root_directory.iterdir() if subdir.is_dir()]

    # Iterate through all subdirectories with a progress bar
    for subdir in tqdm(subdirs, desc="Processing subdirectories"):
        # Create a corresponding subdirectory under ![json]
        json_subdir = json_folder / subdir.relative_to(root_directory)
        os.makedirs(json_subdir, exist_ok=True)

        # Iterate through all files in the subdirectory
        for file in subdir.iterdir():
            # Check if the file is a JSON or TXT file
            if file.suffix in {".json", ".txt"}:
                # Move the file to the corresponding subdirectory under ![json]
                shutil.move(str(file), str(json_subdir / file.name))


if __name__ == "__main__":
    root_directory_str = input("输入tagger根目录:")
    move_json_txts(root_directory_str)
