"""
1. if the two files have similar size (< 20%), and the dimensions are the same, keep the smaller file.
2. if the two files have large differences (>20%), keep the larger file.
"""

import os
import pandas as pd
from imagehash import hex_to_hash
from shutil import move
from tqdm import tqdm
import multiprocessing as mp
from PIL import Image
import concurrent.futures

def phash_diff(file1, file2, phash_dict, phash_diff_threshold):
    diff = phash_dict[file1].__sub__(phash_dict[file2])
    if diff < phash_diff_threshold:
        return True
    return False


def size_and_dimension(filepath):
    size = os.path.getsize(filepath)
    with Image.open(filepath) as img:
        width, height = img.size
    return size, width, height


def find_similar_files(args):
    file1, file2, phash_dict, phash_diff_threshold = args
    if phash_diff(file1, file2, phash_dict, phash_diff_threshold):
        return (file1, file2)
    return None



def move_similar_images(source_root, destination_root, csv_file, phash_diff_threshold):
    # Read the existing CSV
    df = pd.read_csv(csv_file)
    df['phash'] = df['phash'].apply(lambda x: hex_to_hash(x) if isinstance(x, str) else None)

    # Filter out rows with missing phash values
    df = df.dropna(subset=['phash'])

    # Create a dictionary to store the phash values
    phash_dict = {row['filename']: row['phash'] for _, row in df.iterrows()}

    # Create a dictionary to store author-file mappings
    author_files = {}
    for filename in phash_dict:
        author = filename.split('__')[0]
        if author in author_files:
            author_files[author].append(filename)
        else:
            author_files[author] = [filename]

    # Find similar files
    similar_files = set()
    for author, files in tqdm(author_files.items(), desc='Processing authors'):
        for i, file1 in enumerate(files):
            for file2 in files[i + 1:]:
                diff = phash_dict[file1].__sub__(phash_dict[file2])
                if diff < phash_diff_threshold:
                    similar_files.add((file1, file2))

    # Move the similar images
    for foldername, _, filenames in tqdm(os.walk(source_root), desc='Moving similar images'):
        for filename1, filename2 in similar_files:
            if filename1 in filenames and filename2 in filenames:
                file1_path = os.path.join(foldername, filename1)
                file2_path = os.path.join(foldername, filename2)

                try:
                    size1, width1, height1 = size_and_dimension(file1_path)
                    size2, width2, height2 = size_and_dimension(file2_path)
                except FileNotFoundError:
                    print(f"one of paths doesnt exist: {file1_path} | {file2_path}")
                    continue

                size_diff = abs(size1 - size2) / max(size1, size2)

                file_to_move = None
                if width1 == width2 and height1 == height2:
                    if size_diff < 0.2:
                        file_to_move = file1_path if size1 > size2 else file2_path
                elif size_diff > 0.2:
                    file_to_move = file1_path if size1 < size2 else file2_path

                if file_to_move:
                    relative_path = os.path.relpath(foldername, source_root)
                    destination_path = os.path.join(destination_root, relative_path)

                    if not os.path.exists(destination_path):
                        os.makedirs(destination_path)

                    move(file_to_move, os.path.join(destination_path, os.path.basename(file_to_move)))




def debug():
    file1 = "1357697817985179648_1.jpg"
    file2 = "1357697817985179648_2.jpg"
    base_dir = r"D:\CSC\twitter-suite\gallery-dl\twitter_z3zz4_min2020"
    csv_file = os.path.join(base_dir, "aesthetic_scores_with_phash.csv")
    df = pd.read_csv(csv_file)
    df['phash'] = df['phash'].apply(lambda x: hex_to_hash(x) if isinstance(x, str) else None)

    # Filter out rows with missing phash values
    df = df.dropna(subset=['phash'])

    # Create a dictionary to store the phash values
    phash_dict = {row['filename']: row['phash'] for _, row in df.iterrows()}

    print(phash_diff(file1, file2, phash_dict, 50))






if __name__ == '__main__':
    # debug()
    phash_diff_threshold = 50
    source_root = input("source dir:")
    destination_root = f"{source_root}_phash_diff{phash_diff_threshold}"
    csv_file = os.path.join(source_root, "aesthetic_scores_with_phash.csv")

    move_similar_images(source_root, destination_root, csv_file, phash_diff_threshold)
