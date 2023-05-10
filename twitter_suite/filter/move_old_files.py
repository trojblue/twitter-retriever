import os
import shutil

extensions = (".jpg", ".jpeg", ".png", ".webp")


def _move_files(source_dir, dest_dir, min_year):
    with os.scandir(source_dir) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.lower().endswith(extensions):
                try:
                    year_string = entry.name.split("__")[1][:4]
                except IndexError:
                    print(entry.name, " isn't __ separated")
                    continue
                year = int(year_string)

                if year < min_year:
                    source_path = os.path.join(source_dir, entry.name)

                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir)

                    shutil.move(source_path, os.path.join(dest_dir, entry.name))
            elif entry.is_dir():
                _move_files(
                    os.path.join(source_dir, entry.name),
                    os.path.join(dest_dir, entry.name),
                    min_year,
                )


def move_files_older_than(source_root: str, min_year: int = 2020):
    destination_root = (
        f"{source_root}_min{min_year}"  # Replace with your destination root folder path
    )

    _move_files(source_root, destination_root, min_year)


if __name__ == "__main__":
    source_root = input("sources root:")
    min_year = int(input("min year:"))
    move_files_older_than(source_root, min_year)
