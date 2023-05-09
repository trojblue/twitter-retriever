"""
inserts the cafe_aesthetic, cafe_style and cafe_waifu into the given csv
"""

import os
import pandas as pd
from PIL import Image
from imagehash import phash
from tqdm import tqdm
import concurrent.futures
try:
    from .cafe import CafePredictor
except ImportError:
    from twitter_suite.metrics.cafe import CafePredictor

extensions = (".jpg", ".jpeg", ".png", ".webp")


# Function to calculate the metrics of an image file
# def calculate_metrics(file_path, predictor: CafePredictor):
#     """
#     全部aesthetics, 慢
#     """
#     img = Image.open(file_path)
#     scores = predictor.get_string_metrics(img)
#     return (scores["cafe_aesthetic"], scores["cafe_style"], scores["cafe_waifu"])


def calculate_metrics(file_path, predictor: CafePredictor):
    img = Image.open(file_path)
    style_str = predictor.get_style_string(img)
    return [style_str]

def insert_cafe_metrics(source_root, csv_file: str = None):
    predictor = CafePredictor()

    csv_file = os.path.join(source_root, "metrics.csv") if not csv_file else csv_file

    # Read the existing CSV
    df = pd.read_csv(csv_file)

    new_csv_file = os.path.join(source_root, "aesthetic_scores_with_metrics.csv")

    # Create an empty dictionary to store the metric values
    metric_dict = {}

    # Get a list of all image file paths
    image_files = []
    for foldername, _, filenames in os.walk(source_root):
        for filename in filenames:
            if filename.lower().endswith(extensions):
                file_path = os.path.join(foldername, filename)
                image_files.append(file_path)

    # Calculate metric values for all image files in subdirectories without using multithreading
    for file_path in tqdm(image_files, total=len(image_files)):
        metrics = calculate_metrics(file_path, predictor)
        metric_dict[os.path.basename(file_path)] = metrics


    # Add new columns to the DataFrame with the metric values
    # df["phash"] = df["filename"].apply(lambda x: metric_dict[x][0] if x in metric_dict else None)
    # df["cafe_aesthetic"] = df["filename"].apply(lambda x: metric_dict[x][0] if x in metric_dict else None)
    df["cafe_style"] = df["filename"].apply(lambda x: metric_dict[x][0] if x in metric_dict else None)
    # df["cafe_waifu"] = df["filename"].apply(lambda x: metric_dict[x][2] if x in metric_dict else None)

    # Save the updated DataFrame to a new CSV file
    df.to_csv(new_csv_file, index=False)


if __name__ == '__main__':
    # Set paths
    source_root = input("root dir:")
    insert_cafe_metrics(source_root)
