import os
import pandas as pd
import itertools
from imagehash import hex_to_hash
from shutil import move
from tqdm import tqdm
from functools import partial
import multiprocessing as mp

def phash_diff(args, phash_dict, phash_diff_threshold):
    file1, file2 = args
    diff = phash_dict[file1] - phash_dict[file2]
    if diff < phash_diff_threshold:
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

    # Calculate phash differences and find similar files
    similar_files = set()
    combinations = list(itertools.combinations(phash_dict.keys(), 2))
    
    with mp.Pool(mp.cpu_count()) as pool:
        phash_diff_partial = partial(phash_diff, phash_dict=phash_dict, phash_diff_threshold=phash_diff_threshold)
        with tqdm(total=len(combinations), desc='Calculating phash differences') as progress_bar:
            for result in pool.imap_unordered(phash_diff_partial, combinations):
                progress_bar.update()
                if result:
                    similar_files.add(result[0])
                    similar_files.add(result[1])

    # Move the similar images
    for foldername, _, filenames in tqdm(os.walk(source_root), desc='Moving similar images'):
        for filename in filenames:
            if filename in similar_files:
                source_path = os.path.join(foldername, filename)
                relative_path = os.path.relpath(foldername, source_root)
                destination_path = os.path.join(destination_root, relative_path)

                try:
                    move(source_path, os.path.join(destination_path, filename))
                except Exception as e:
                    print(f"failed to move {filename} to {destination_path}: {e}")

phash_diff_threshold = 5
source_root = r"D:\CSC\twitter-suite\gallery-dl\twitter_z3zz4_min2020"
destination_root = f"{source_root}_phash_diff{phash_diff_threshold}"
csv_file = os.path.join(source_root, "aesthetic_scores_with_phash.csv")


move_similar_images(source_root, destination_root, csv_file, phash_diff_threshold)
