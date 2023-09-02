import json
import pickle

import Scweet.utils
import dotenv
import os
from Scweet.const import load_env_variable
import signal
import atexit


"""
IN PROGRESS
"""

class InfoRetrieverBase:
    """
    selenium 浏览器相关 (存储, 退出, 信号处理)
    """

    def __init__(
        self,
        env_path: str = ".env",
        headless: bool = True,
    ):
        self.env_path = env_path
        self.headless = headless
        self.driver = None
        self._load_env_variables()

        # Register the save_storage method for handling Ctrl+C and program termination
        signal.signal(signal.SIGINT, self._handle_sigint)
        atexit.register(self._handle_exit)

    def _load_env_variables(self):
        """
        加载环境变量 (".env" 文件)
        """
        self.env = dotenv.load_dotenv(self.env_path, verbose=True)
        self.user_data_dir = load_env_variable("DRIVER_USER_DATA_DIR", none_allowed=True)
        self.storage_file = load_env_variable("DRIVER_STORAGE_FILENAME", none_allowed=True)

        if not os.path.exists(self.user_data_dir):
            os.makedirs(self.user_data_dir)

    def _get_chrome_options_str(self) -> str:
        """
        Chrome options:
        - user agent
        - user data dir
        """
        UA = "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        user_data_dir = "--user-data-dir=" + self.user_data_dir
        allow_data_saver = "--allow-insecure-localhost --allow-running-insecure-content --disable-web-security --disable-features=IsolateOrigins,site-per-filter"
        allow_storage = "--disable-web-security --allow-running-insecure-content"

        options_list = [UA, user_data_dir, allow_data_saver, allow_storage]

        return " ".join(options_list)

    def _save_storage(self):
        """
        保存localStorage, 用来保持推特登录状态
        """
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))

        # local_storage = self.driver.execute_script("return window.localStorage;")
        # session_storage = self.driver.execute_script("return window.sessionStorage;")
        # storage_data = {
        #     "local_storage": local_storage,
        #     "session_storage": session_storage,
        # }
        # with open(self.storage_file, "w") as f:
        #     json.dump(storage_data, f)

    def _load_storage(self):
        """
        读取localStorage, 用来保持推特登录状态
        """
        cookies = pickle.load(open("cookies.pkl", "rb"))
        self.driver.get('https://twitter.com')

        for cookie in cookies:
            self.driver.add_cookie(cookie)

        # with open(self.storage_file, "r") as f:
        #     storage_data = json.load(f)
        # for key, value in storage_data["local_storage"].items():
        #     driver.execute_script(f"window.localStorage.setItem('{key}', '{value}');")
        # for key, value in storage_data["session_storage"].items():
        #     driver.execute_script(f"window.sessionStorage.setItem('{key}', '{value}');")

    def init_webdriver(self):
        """
        初始化webdriver:
        - 加载chromeOptions (UA, user-data-dir)
        - 读取存储的localStorage
        """
        options = self._get_chrome_options_str()
        self.driver = Scweet.utils.init_driver(headless=self.headless, option=options)

        if os.path.exists("cookies.pkl"):
            self._load_storage()

    def _handle_sigint(self, signum, frame):
        """
        中断时保存localStorage
        """
        print("Ctrl+C detected. ...")
        # self._save_storage()
        # self.driver.quit()
        exit(0)

    def _handle_exit(self):
        """
        退出时保存localStorage
        """
        print("Program terminating. ...")
        # self._save_storage()
        # self.driver.quit()
