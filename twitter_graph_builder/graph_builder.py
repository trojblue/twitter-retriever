import networkx as nx
import pickle
import time
import os
from typing import List


def get_followers_and_following(twitter_handle: str) -> (List[str], List[str]):
    """
    :param twitter_handle: Twitter handle of the artist
    :return: List of followers and list of following (List[str], List[str])
    """
    # Provided method implementation
    pass


def check_is_artist(twitter_handle: str) -> bool:
    # Provided method implementation
    pass


"""
IN PROGRESS
"""
class ArtistGraphBuilder:
    def __init__(
        self,
        seed_artists: List[str],
        save_interval: int = 300,
        save_path: str = "artist_graph.pkl",
    ):
        self.seed_artists = seed_artists
        self.save_interval = save_interval
        self.save_path = save_path

        if os.path.exists(save_path):
            with open(save_path, "rb") as f:
                self.artist_graph = pickle.load(f)
        else:
            self.artist_graph = nx.DiGraph()
            self.artist_graph.add_nodes_from(seed_artists)

    def build_graph(self):
        last_save_time = time.time()
        nodes_to_process = list(self.seed_artists)

        while nodes_to_process:
            artist = nodes_to_process.pop(0)
            if artist not in self.artist_graph:
                self.artist_graph.add_node(artist)

            _, followings = get_followers_and_following(artist)

            for following in followings:
                if following not in self.artist_graph.nodes:
                    if check_is_artist(following):
                        self.artist_graph.add_node(following)
                        nodes_to_process.append(following)

                self.artist_graph.add_edge(artist, following)

            if time.time() - last_save_time > self.save_interval:
                self.save_graph()
                last_save_time = time.time()

        self.save_graph()

    def save_graph(self):
        with open(self.save_path, "wb") as f:
            pickle.dump(self.artist_graph, f)


if __name__ == "main":
    seed_artists = [
        "artist1",
        "artist2",
        "artist3",
    ]  # Replace with actual artist Twitter handles
    builder = ArtistGraphBuilder(seed_artists)
    builder.build_graph()
