import os
import json
import glob
import pandas as pd
from datetime import datetime
from tqdm.auto import tqdm

def get_pixiv_filename(illust, url):
    if "create_date" in illust:
        create_date = datetime.fromisoformat(illust["create_date"])
        date_str = create_date.strftime("%Y%m%d")
    else:
        return None
    if "user" in illust and "account" in illust["user"]:
        user = illust["user"]["account"]
    else:
        return None
    filename = os.path.basename(url)
    return f"px_{date_str}_{user}_pid{filename}"

def get_row(filename, df: pd.DataFrame):
    row = df.loc[df['filename'] == filename]
    if not row.empty:
        return row.squeeze()
    else:
        return None

def fill_aesthetic(filename, df: pd.DataFrame):
    with open(filename, 'r') as f:
        json_object = json.load(f)
    if json_object is None:
        return
    cnt = 0
    for day in json_object:
        cnt += len(json_object[day])
    bar = tqdm(total=cnt)
    for day in json_object:
        for illust in json_object[day]:
            if "meta_single_page" in illust and len(illust["meta_single_page"]) > 0:
                url = illust["meta_single_page"]["original_image_url"]
                image_name = get_pixiv_filename(illust, url)
                row = get_row(image_name, df)
                if row is not None:
                    illust["meta_single_page"]["aesthetic"] = row["score"]
                    illust["meta_single_page"]["md5"] = row["md5"]
            elif "meta_pages" in illust and len(illust["meta_pages"]) > 0:
                for item in illust["meta_pages"]:
                    url = item["image_urls"]["original"]
                    image_name = get_pixiv_filename(illust, url)
                    row = get_row(image_name, df)
                    if row is not None:
                        item["aesthetic"] = row["score"]
                        item["md5"] = row["md5"]
            bar.update(1)
    name, _ = os.path.splitext(os.path.basename(filename))
    path = os.path.dirname(filename)
    with open(os.path.join(path, f"{name}-aes.json"), 'w') as f:
        json.dump(json_object, f)

if __name__ == "__main__":
    df = pd.read_csv("scores-2021-merge.csv")
    files = glob.glob("2021/*.json")
    for f in files:
        print(f"fill {f}")
        fill_aesthetic(f, df)
