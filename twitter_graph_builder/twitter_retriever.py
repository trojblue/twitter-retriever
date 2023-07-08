from Scweet.scweet import scrape
from Scweet.user import (
    get_user_information,
    get_users_following,
    get_users_followers,
)
from Scweet.utils import get_users_follow
from typing import *
from retriever_base import InfoRetrieverBase


class RetriverConfig():
    def __init__(
            self, env, headless, verbose, wait, limit,
            existing_driver=None,
            login=False,
            add_at_sign=False,
            file_path=None
    ):
        self.env = env
        self.headless = headless
        self.verbose = verbose
        self.wait = wait
        self.limit = limit
        self.existing_driver = existing_driver
        self.login = login
        self.add_at_sign = add_at_sign
        self.file_path = file_path

    def to_dict(self):
        return self.__dict__


class ArtistInfoRetriever(InfoRetrieverBase):
    """
    功能实现; 浏览器相关放在 retriever_base 里节省地方
    """

    def __init__(
            self,
            env_path: str = ".env",
            verbose: int = 0,
            headless: bool = True,
            wait: int = 6,
            limit: int = float('inf'),
            scweet_file_path: str = None,
            login: bool = True,
    ):
        super().__init__(env_path, headless)
        self.config = RetriverConfig(self.env, self.headless, verbose, wait, limit, None, False, False,
                                     scweet_file_path)

        self.verbose = verbose
        self.wait = wait
        self.limit = limit
        self.scweet_file_path = scweet_file_path
        self.login = login

        # Initialize the webdriver (self.driver)
        # implemented at retriever_base
        self.init_webdriver()

    def get_user_information(self, users_list: List[str]):
        return get_user_information(
            users=users_list,
            headless=self.headless,
            driver=self.driver,
        )

    def get_users_following(self, users_list: List[str]):
        following = get_users_following(
            users=users_list,
            env=self.env_path,
            headless=self.headless,
            verbose=self.verbose,
            wait=self.wait,
            limit=self.limit,
            existing_driver=self.driver,
            login=self.login,
            add_at_sign=False,
        )
        self._save_storage()

        return following

    def get_users_followers(self, users_list: List[str]):
        followers = get_users_followers(
            users=users_list,
            env=self.env_path,
            verbose=self.verbose,
            headless=self.headless,
            wait=self.wait,
            limit=self.limit,
            file_path=self.scweet_file_path,
        )

        self._save_storage()

        return followers


def debug():
    retriever = ArtistInfoRetriever(headless=False, login=False)

    users = ["g0ach"]
    following = retriever.get_users_following(users)
    print("D")

    following_list = following['trojblue']
    with open("following.txt", "w", encoding="utf-8") as f:
        # for i in following_list:
        f.write("\n".join(following_list))


if __name__ == "__main__":
    debug()

    # users = [
    #     "yada_cc",
    # ]
    # env_path = ".env"
    #
    # following = get_users_following(
    #     users=users,
    #     env=env_path,
    #     verbose=0,
    #     headless=True,
    #     wait=2,
    #     limit=50,
    #     file_path=None,
    # )
    #
    # print("D")
