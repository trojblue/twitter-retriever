from .download_user_imgs import download_users as _download_users

def download_users(txt_path: str, dst_dir: str = ""):
    """从txt文件中读取twitter handle, 并使用gallery-dl下载用户的media
    """
    _download_users(txt_path, dst_dir)
