import os


def delete_empty_folders(path):
    for root, dirs, _ in os.walk(path, topdown=False):
        for d in dirs:
            dir_path = os.path.join(root, d)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                print(f"Deleted empty folder: {dir_path}")


source_root = "D:\Andrew\Pictures\Grabber"  # Replace with your source root folder path
delete_empty_folders(source_root)
