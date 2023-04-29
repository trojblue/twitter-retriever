import os
import shutil

MIN_YEAR = 2020

source_root = r"D:\Andrew\Pictures\Grabber\twitter_saver"  
destination_root = f"{source_root}_min{MIN_YEAR}"  # Replace with your destination root folder path
extensions = ('.jpg', '.jpeg', '.png', '.webp')

def move_files(source_dir, dest_dir):
    with os.scandir(source_dir) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.lower().endswith(extensions):
                try:
                    year_string = entry.name.split('__')[1][:4]
                except IndexError:
                    print(entry.name, " isn't __ separated")
                    continue
                year = int(year_string)

                if year < MIN_YEAR:
                    source_path = os.path.join(source_dir, entry.name)

                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir)

                    shutil.move(source_path, os.path.join(dest_dir, entry.name))
            elif entry.is_dir():
                move_files(os.path.join(source_dir, entry.name),
                           os.path.join(dest_dir, entry.name))

move_files(source_root, destination_root)
