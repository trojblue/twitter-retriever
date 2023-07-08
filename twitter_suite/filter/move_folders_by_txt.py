import os
import shutil
from multiprocessing import Pool
from tqdm import tqdm
from datetime import datetime


def move_folders_by_txt(txt_file: str, base_dir: str, dst_dir: str, copy: bool = False, min_year: int = None) -> None:
    def eligible_for_transfer(src: str, min_year: int) -> bool:
        if min_year:
            modified_time = os.path.getmtime(src)
            modified_year = datetime.fromtimestamp(modified_time).year
            return modified_year >= min_year
        return True

    def transfer_file(src_dest_copy: tuple):
        src, dest, copy = src_dest_copy

        if not os.path.exists(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest))

        if copy:
            shutil.copy2(src, dest)
        else:
            shutil.move(src, dest)

    with open(txt_file, "r") as file:
        folder_names = file.readlines()

    transfer_list = []
    for folder_name in folder_names:
        folder_name = folder_name.strip()
        src_folder = os.path.join(base_dir, folder_name)
        dest_folder = os.path.join(dst_dir, folder_name)

        if os.path.exists(src_folder):
            for root, _, files in os.walk(src_folder):
                for file in files:
                    src_file = os.path.join(root, file)
                    dest_file = os.path.join(dest_folder, os.path.relpath(src_file, src_folder))
                    if eligible_for_transfer(src_file, min_year):
                        transfer_list.append((src_file, dest_file, copy))

    # Use multiprocessing pool to move files in parallel
    with Pool() as p:
        list(tqdm(p.imap(transfer_file, transfer_list), total=len(transfer_list), desc="Transferring files"))

if __name__ == "__main__":
    source_root = r"D:\CSC\twitter-suite\gallery-dl\twitter"
    destination_root = f"{source_root}me-and-troj-and-illusts=min2018"
    txt_root = r"D:\CSC\twitter-suite\bin"
    txt = os.path.join(txt_root, "twitter-list-me-and-troj-and-illusts-deduped 20230527.txt")

    move_folders_by_txt(txt, source_root, destination_root, copy=True, min_year=2019)
