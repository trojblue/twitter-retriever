import os
import shutil
from tqdm.auto import tqdm


def move_folders_by_txt(txt_file: str, base_dir: str, dst_dir: str, copy:bool=False) -> None:
    """
    Read a text file containing folder names, and move all folders with the given names
    from the base directory to the destination directory.

    :param txt_file: The path to the text file containing folder names.
    :param base_dir: The base directory containing the folders to be moved.
    :param dst_dir: The directory where the folders will be moved to.
    """
    method_str = "copy" if copy else "move"
    print(f"{method_str} folders listed in {txt_file} from {base_dir} to {dst_dir}: ")

    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    with open(txt_file, "r") as file:
        folder_names = file.readlines()

    for folder_name in tqdm(folder_names):
        folder_name = folder_name.strip()
        src_folder = os.path.join(base_dir, folder_name)
        dest_folder = os.path.join(dst_dir, folder_name)

        if os.path.exists(src_folder):
            if copy:
                shutil.copytree(src_folder, dest_folder, dirs_exist_ok=True)
            else:
                shutil.move(src_folder, dest_folder)
        else:
            print(f"Folder {src_folder} not found.")


if __name__ == "__main__":
    source_root = r"D:\CSC\twitter-suite\gallery-dl\twitter"
    destination_root = f"{source_root}_z3zz4"

    txt_root = r"D:\CSC\twitter-suite\bin"
    txt = os.path.join(txt_root, "twitter-following-z3zz4.txt")

    move_folders_by_txt(txt, source_root, destination_root)

    # move_similar_images(source_root, destination_root, csv_file, phash_diff_threshold)
