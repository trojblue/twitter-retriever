import re
from googlesearch import search
from tqdm import tqdm

name_str = "世津田スン／REO／wacca"


def parse_names(name_str):
    return name_str.split("／")


def get_twitter_handle(url):
    match = re.search(r'https?://twitter\.com/(\w+)', url)
    return match.group(1) if match else None


def get_names(name_str):
    names = parse_names(name_str)

    with open("twitter_handles.txt", "w") as f:
        for name in names:
            query = f"{name} Twitter"
            try:
                results = search(query, num_results=1)
                result = next(results, None)
                if result:
                    twitter_handle = get_twitter_handle(result)
                    if twitter_handle:
                        print(f"{name}: {twitter_handle}")
                        f.write(twitter_handle + "\n")
            except Exception as e:
                print(f"Error occurred while searching for {name}: {e}")


if __name__ == '__main__':
    get_names(name_str)
