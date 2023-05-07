import os
import shutil
from datetime import datetime

MIN_YEAR = 2020

source_root = r"D:\CSC\twitter-suite\gallery-dl\twitter_z3zz4"
destination_root = f"{source_root}_min{MIN_YEAR}"
extensions = (".jpg", ".jpeg", ".png", ".webp")


def copy_files_newer_than_year(source_dir, dest_dir, min_year):
    with os.scandir(source_dir) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.lower().endswith(extensions):
                modified_time = os.path.getmtime(entry.path)
                modified_year = datetime.fromtimestamp(modified_time).year

                if modified_year > min_year:
                    source_path = os.path.join(source_dir, entry.name)

                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir)

                    shutil.copy2(source_path, os.path.join(dest_dir, entry.name))
            elif entry.is_dir():
                copy_files_newer_than_year(
                    os.path.join(source_dir, entry.name),
                    os.path.join(dest_dir, entry.name),
                    min_year,
                )


copy_files_newer_than_year(source_root, destination_root, MIN_YEAR)
