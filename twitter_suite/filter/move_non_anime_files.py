import os
import pandas as pd
import shutil
from typing import Callable, Dict


class FileMover:
    def __init__(self, root_dir: str, csv_file: str = None):
        self.root_dir = root_dir
        self.csv_file = csv_file or os.path.join(root_dir, "metrics.csv")
        self.df = self.load_dataframe()
        self.file_index = self.create_file_index()

    def load_dataframe(self) -> pd.DataFrame:
        return pd.read_csv(self.csv_file)

    def create_file_index(self) -> Dict[str, str]:
        file_index = {}
        for foldername, _, filenames in os.walk(self.root_dir):
            for filename in filenames:
                file_index[filename] = os.path.join(foldername, filename)
        return file_index

    def move_files(self, df: pd.DataFrame, target_root_dir: str):
        for _, row in df.iterrows():
            filename = row["filename"]
            source_file_path = self.file_index.get(filename)
            if source_file_path is None:
                continue

            relative_folder = os.path.relpath(
                os.path.dirname(source_file_path), self.root_dir
            )
            target_folder = os.path.join(target_root_dir, relative_folder)
            target_file_path = os.path.join(target_folder, filename)

            os.makedirs(target_folder, exist_ok=True)
            shutil.move(source_file_path, target_file_path)

    def move_files_based_on_condition(
        self,
        column: str,
        condition: Callable[[pd.Series], pd.Series],
        target_suffix: str,
    ):
        filtered_df = self.df[condition(self.df[column])]
        target_root_dir = f"{self.root_dir}_{target_suffix}"
        self.move_files(filtered_df, target_root_dir)


if __name__ == "__main__":
    root_dir = input("root dir:")

    file_mover = FileMover(root_dir)
    file_mover.move_files_based_on_condition("score", lambda x: x < 5.5, "aes_sub5.5")
