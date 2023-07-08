import os
import shutil
import pandas as pd
from typing import Dict
from conditions import CsvCondition, Condition


class FileMover:
    """
    Class for moving files based on certain conditions.

    Args:
        root_dir (str): Root directory containing the files to be moved.
        csv_file (str, optional): CSV file containing metadata for the files. Defaults to None.
    """

    def __init__(self, root_dir: str, csv_file: str = None):
        self.root_dir = root_dir
        self.csv_file = csv_file or os.path.join(root_dir, "metrics.csv")
        self.df = self._load_dataframe()
        self.file_index = self._create_file_index()

    def _load_dataframe(self) -> pd.DataFrame:
        """
        Load DataFrame from the CSV file.

        Returns:
            pd.DataFrame: DataFrame containing the data from the CSV file.
        """
        return pd.read_csv(self.csv_file)

    def _create_file_index(self) -> Dict[str, str]:
        """
        Create an index of files in the root directory.

        Returns:
            Dict[str, str]: Dictionary mapping file names to their paths.
        """
        file_index = {}
        for foldername, _, filenames in os.walk(self.root_dir):
            for filename in filenames:
                file_index[filename] = os.path.join(foldername, filename)
        return file_index

    def _move_files(self, df: pd.DataFrame, target_root_dir: str):
        """
        Move files based on a given DataFrame and a target directory.

        Args:
            df (pd.DataFrame): DataFrame containing the file names of the files to be moved.
            target_root_dir (str): Target root directory to which to move the files.
        """
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

    def move_files_based_on_condition(self, condition: Condition, target_suffix: str):
        """
        Move files based on a given condition and a target suffix.

        Args:
            condition (Condition): Condition to apply to the files.
            target_suffix (str): Suffix to append to the root directory to create the target directory.
        """
        filtered_df = self.df[condition.check(self.df)]
        target_root_dir = f"{self.root_dir}_{target_suffix}"
        self._move_files(filtered_df, target_root_dir)


if __name__ == "__main__":
    root_dir = input("root dir:")

    file_mover = FileMover(root_dir)
    file_mover.move_files_based_on_condition(
        CsvCondition("score", lambda x: x < 4.5, dtype='float'),
        "aes_sub4.5"
    )
