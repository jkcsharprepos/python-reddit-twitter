from downloaders.reddit_downloader import RedditDownloader
from downloaders.twitter_downloader import TwitterDownloader

downloader_config = {
    1: {
        "downloader_name": "Reddit",
        "downloader_bot": RedditDownloader
    },
    2: {
        "downloader_name": "Twitter",
        "downloader_bot": TwitterDownloader
    }
}


if __name__ == '__main__':
    client = downloader_config[2]["downloader_bot"]()
    subreddit_name_list = ["PolskaPolityka", "Polska", "PolishLanguagePodcast", "libek", "Polska_wpz",
                           "FashionRepsPolska", "warszawa"]
    twitter_ids = ["102358648", "1171802866966831104", "63029891"]
    response = client.get_posts(twitter_ids[2])
    print(0)


