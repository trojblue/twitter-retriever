import os
import shutil
from pathlib import Path
from tqdm import tqdm



if __name__ == '__main__':
    root_directory_str = input("输入tagger根目录:")
    root_directory = Path(root_directory_str)

    # Get a list of all subdirectories
    subdirs = [subdir for subdir in root_directory.iterdir() if subdir.is_dir()]

    # Iterate through all subdirectories with a progress bar
    for subdir in tqdm(subdirs, desc="Processing subdirectories"):
        # Iterate through all files in the subdirectory
        for file in subdir.iterdir():
            # Check if the file is a JSON or TXT file
            if file.suffix in {".json", ".txt"}:
                # Move the file to the root directory
                shutil.move(str(file), str(root_directory / file.name))
