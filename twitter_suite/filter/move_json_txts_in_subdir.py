import os
import shutil
from pathlib import Path
from tqdm import tqdm



def move_json_txts(dir_str:str):
    root_directory = Path(dir_str)
    json_folder = root_directory / Path("![json]")
    os.makedirs(json_folder, exist_ok=True)

    # Get a list of all subdirectories
    subdirs = [subdir for subdir in root_directory.iterdir() if subdir.is_dir()]


    # Iterate through all subdirectories with a progress bar
    for subdir in tqdm(subdirs, desc="Processing subdirectories"):
        # Iterate through all files in the subdirectory
        for file in subdir.iterdir():
            # Check if the file is a JSON or TXT file
            if file.suffix in {".json", ".txt"}:
                # Move the file to the root directory
                shutil.move(str(file), str(json_folder / file.name))



if __name__ == '__main__':
    root_directory_str = input("输入tagger根目录:")
    move_json_txts(root_directory_str)

