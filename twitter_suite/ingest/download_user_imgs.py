import subprocess
from pathlib import Path
from tqdm.auto import tqdm
import csv
import datetime
from typing import Optional


class TwitterDownloader:

    def __init__(self, check_interval_days: int = 3):
        self.check_interval = datetime.timedelta(days=check_interval_days)

    @staticmethod
    def read_handles(file_path: str) -> list:
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]

    @staticmethod
    def run_gallery_dl(handle: str, dst_dir: Optional[str] = None):
        url = f"https://twitter.com/{handle}/media"
        command = f"gallery-dl {url} --mtime-from-date --write-metadata --write-info-json"
        if dst_dir:
            command += f" --dest {dst_dir}"

        # Run gallery-dl
        subprocess.run(command, shell=True)

    def check_and_update_csv(self, csv_path: str, txt_path: str, dst_dir: Optional[str] = None):
        try:
            with open(csv_path, 'r') as csvfile:
                reader = csv.reader(csvfile)
                last_checked = {rows[0]: datetime.datetime.strptime(rows[1], '%Y-%m-%d %H:%M:%S.%f') for rows in reader}
        except FileNotFoundError:
            last_checked = {}

        handles = self.read_handles(txt_path)
        progress_bar = tqdm(handles, unit="user")
        now = datetime.datetime.now()

        for handle in progress_bar:
            if now - last_checked.get(handle, datetime.datetime.min) > self.check_interval:
                progress_bar.set_description(f"Downloading media for {handle}")
                self.run_gallery_dl(handle, dst_dir)
                last_checked[handle] = now
                # Update the CSV every 5 minutes
                if (datetime.datetime.now() - now).total_seconds() > 5 * 60:
                    self.update_csv(csv_path, last_checked)
                    now = datetime.datetime.now()

        # Save the final state
        self.update_csv(csv_path, last_checked)

    @staticmethod
    def update_csv(csv_path: str, last_checked: dict):
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for handle, checked_time in last_checked.items():
                writer.writerow([handle, checked_time])


if __name__ == "__main__":
    file_path = "./bin/twitter-list-me-and-troj-and-illusts-deduped 20230527.txt"
    downloader = TwitterDownloader()
    downloader.check_and_update_csv(file_path.replace('.txt', '.csv'), file_path)
