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

        if os.path.exists(self.output_csv):
            existing_df = pd.read_csv(self.output_csv)
            logged_files = set(existing_df["filename"])
        else:
            logged_files = set()

        for img in img_files:
            if os.path.basename(img) not in logged_files:
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

    def predict_aesthetics(self) -> None:
        files_to_change = []
        for root, _, _ in os.walk(self.root_dir):
            files_to_change.extend(self._scan_for_files_to_change(root))

        print(
            f"{datetime.datetime.now()} [INFO] found {len(files_to_change)} file(s) for evaluation"
        )

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
    aesthetic_monitor.predict_aesthetics()
