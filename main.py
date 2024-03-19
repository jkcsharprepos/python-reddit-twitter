import os
import logging

from downloaders.reddit_downloader import RedditDownloader
from downloaders.twitter_downloader import TwitterDownloader
from ServiceConnector import ServiceConnector

DOWNLOADER_CONFIG = {
    1: {
        "downloader_name": "Reddit",
        "downloader_bot": RedditDownloader,
    },
    2: {
        "downloader_name": "Twitter",
        "downloader_bot": TwitterDownloader
    }
}
DOWNLOADER_TYPE = int(os.environ.get("DOWNLOADER_TYPE", 1))

subreddit_name_list = ["PolskaPolityka", "Polska",
                       "PolishLanguagePodcast", "libek", "Polska_wpz",
                           "FashionRepsPolska", "warszawa"]

twitter_tasks = [{"id": "102358648", "screen_name": ""},
                 {"id": "1171802866966831104", "screen_name": ""},
                 {"id": "63029891", "screen_name": ""}]



if __name__ == '__main__':
    service_connector = ServiceConnector(mongodb={"db": "web-scraper"})
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    client = DOWNLOADER_CONFIG[DOWNLOADER_TYPE]["downloader_bot"]()

    logging.info(f"Start processing {DOWNLOADER_CONFIG[DOWNLOADER_TYPE]['downloader_name']}")

    extracted_posts = client.get_posts(subreddit_name_list[1], logging)

    logging.info(f"Successfully proceed task: {subreddit_name_list[1]} for {DOWNLOADER_CONFIG[DOWNLOADER_TYPE]['downloader_name']}")

    for post in extracted_posts:
        new_id = service_connector.insert_row_mongo(client.mongodb_collection, post)













