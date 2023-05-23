import os
import hashlib
import datetime
import pandas as pd
from tqdm.auto import tqdm
from typing import List
import torch

try:
    from .aesthetic import AestheticPredictor
except ImportError:
    from twitter_suite.metrics.aesthetic.aesthetic import AestheticPredictor


__all_imgs_raw = (
    "jpg jpeg png bmp dds exif jp2 jpx pcx pnm ras gif tga tif tiff xbm xpm webp"
)
IMG_FILES = ["." + i.strip() for i in __all_imgs_raw.split(" ")]


def get_files_with_suffix(
    src_dir: str, suffix_list: List[str], recursive: bool = False
):
    """
    :param src_dir:
    :param suffix_list: ['.png', '.jpg', '.jpeg']
    :param recursive: 是否读取子目录
    :return: ['img_filename.jpg', 'filename2.jpg']
    """
    if recursive:  # go through all subdirectories
        filtered_files = []
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                if file.endswith(tuple(suffix_list)):
                    filtered_files.append(os.path.join(root, file))

    else:  # current dir only
        files = os.listdir(src_dir)
        filtered_files = [f for f in files if f.endswith(tuple(suffix_list))]

    return filtered_files


class AestheticMonitor:
    def __init__(self, root_dir: str, output_csv: str = "metrics.csv"):
        self.root_dir = root_dir
        self.output_csv = os.path.join(root_dir, output_csv)

    def _get_files_with_suffix(self, path, suffixes):
        return [
            os.path.join(path, f)
            for f in os.listdir(path)
            if f.lower().endswith(suffixes)
        ]

    def _scan_for_files_to_change(self, monitor_dir: str) -> List[List]:
        files_to_change = []
        img_files = get_files_with_suffix(monitor_dir, IMG_FILES)
        img_files_basename = set(os.path.basename(img) for img in img_files)

        if os.path.exists(self.output_csv):
            existing_df = pd.read_csv(self.output_csv)

            # Filter the DataFrame to only include files within the monitor_dir
            existing_df = existing_df[existing_df["filename"].isin(img_files_basename)]
            logged_files = set(existing_df["filename"])

            # Check if the 'score' and 'md5' columns exist and if they have any missing values
            if "score" not in existing_df.columns or "md5" not in existing_df.columns:
                # If the columns do not exist, add all logged files to files_to_change
                files_to_change.extend([[monitor_dir, img] for img in logged_files])
            else:
                # If the columns exist, add files with missing 'score' or 'md5' to files_to_change
                missing_score_or_md5 = existing_df.loc[
                    existing_df[["score", "md5"]].isnull().any(axis=1), "filename"
                ]
                files_to_change.extend(
                    [[monitor_dir, img] for img in missing_score_or_md5]
                )
        else:
            logged_files = set()

        for img in img_files_basename:
            if img not in logged_files:
                files_to_change.append([monitor_dir, img])

        return files_to_change

    def _predict_aesthetics(self, files_to_change: List) -> pd.DataFrame:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        predictor = AestheticPredictor(
            "ViT-L/14", 768, "bin/sac+logos+ava1-l14-linearMSE.pth", device
        )
        files = [os.path.join(i[0], i[1]) for i in files_to_change]
        scores = predictor.predict(files, 16, 2)
        md5s = [hashlib.md5(open(f, "rb").read()).hexdigest() for f in files]
        df = pd.DataFrame(
            {
                "filename": [os.path.basename(p) for p in files],
                "score": scores,
                "md5": md5s,
            }
        )
        return df

    def predict_aesthetics(self, dry_run: bool = False) -> None:
        """
        Predicts the aesthetic score of all images in the root directory.
        : param dry_run: 为True时, 不会计算图片的美学分数, 只会扫描图片文件并生成csv
        """

        files_to_change = []
        for root, _, _ in os.walk(self.root_dir):
            files_to_change.extend(self._scan_for_files_to_change(root))

        print(
            f"{datetime.datetime.now()} [INFO] found {len(files_to_change)} file(s) for evaluation"
        )

        if dry_run:
            aesthetics_df = pd.DataFrame(
                {
                    "filename": [os.path.basename(p[1]) for p in files_to_change],
                    "score": [None] * len(files_to_change),
                    "md5": [None] * len(files_to_change),
                }
            )
        else:
            aesthetics_df = self._predict_aesthetics(files_to_change)

        if os.path.exists(self.output_csv):
            existing_df = pd.read_csv(self.output_csv)
            merged_df = pd.concat([existing_df, aesthetics_df]).drop_duplicates(
                "filename", keep="last"
            )
        else:
            merged_df = aesthetics_df

        merged_df.to_csv(self.output_csv, index=False)

        print(
            f"{datetime.datetime.now()} [INFO] check complete: data written to {self.output_csv}"
        )


if __name__ == "__main__":
    root_dir = input("Enter root directory: ")
    aesthetic_monitor = AestheticMonitor(root_dir)
    aesthetic_monitor.predict_aesthetics(dry_run=False)
