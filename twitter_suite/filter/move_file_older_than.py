import os
import shutil
from datetime import datetime
from tqdm.auto import tqdm

extensions = (".jpg", ".jpeg", ".png", ".webp", ".tiff", ".bmp")


def count_folders(source_dir: str):
    count = 0
    for root, dirs, files in os.walk(source_dir):
        count += len(dirs)
    return count


def move_files_older_than_year(source_dir: str, dest_dir: str = None, max_year: int = 2018, progress_bar=None):
    if progress_bar is None:
        total_folders = count_folders(source_dir)
        progress_bar = tqdm(total=total_folders, desc="Moving folders")

    true_dest_dir = str(source_dir) + f"_max{max_year}" if not dest_dir else dest_dir
    print("move_files_older_than_year: ", source_dir, true_dest_dir, max_year, sep="\n")

    with os.scandir(source_dir) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.lower().endswith(extensions):
                modified_time = os.path.getmtime(entry.path)
                modified_year = datetime.fromtimestamp(modified_time).year

                if modified_year < max_year:
                    source_path = os.path.join(source_dir, entry.name)

                    if not os.path.exists(true_dest_dir):
                        os.makedirs(true_dest_dir)

                    shutil.move(source_path, os.path.join(true_dest_dir, entry.name))
            elif entry.is_dir():
                move_files_older_than_year(
                    os.path.join(source_dir, entry.name),
                    os.path.join(true_dest_dir, entry.name),
                    max_year,
                    progress_bar,
                )
                progress_bar.update(1)
    if progress_bar.n == progress_bar.total:
        progress_bar.close()


if __name__ == '__main__':
    MAX_YEAR = 2020
    source_root = r"D:\CSC\twitter-suite\gallery-dl\twitter_z3zz4"
    destination_root = f"{source_root}_max{MAX_YEAR}"
    move_files_older_than_year(source_root, destination_root, MAX_YEAR)
