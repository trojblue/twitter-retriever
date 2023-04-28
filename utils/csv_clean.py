import csv
import re
from urllib.parse import urlparse


def print_twitter_usernames_from_csv(csv_path):
    with open(csv_path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)

        for row in csv_reader:
            url = row[0]  # Assuming the URL is in the first column
            parsed_url = urlparse(url)

            if parsed_url.netloc == "twitter.com" or parsed_url.netloc == "www.twitter.com":
                username = re.search(r'(?<=twitter.com/)[^/?]+', url)
                if username:
                    print(username.group(0))


if __name__ == '__main__':
    # Example usage:
    csv_path = r"D:\CSC\twitter-retriever\bin\sdcn_artist_urls_20230425.csv"
    print_twitter_usernames_from_csv(csv_path)
