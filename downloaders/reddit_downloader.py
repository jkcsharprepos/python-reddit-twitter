import httpx
import json


class RedditDownloader:
    def __init__(self):
        self.mongodb_collection = "reddit_downloader"

    def get_posts(self, subreddit_name, logging):
        try:
            response = httpx.get(f"https://www.reddit.com/r/{subreddit_name}/new.json?limit=30&t=month")
            response_json = json.loads(response.text)
        except:
            logging.error("Error during fetch post")
            return None

        posts = response_json["data"].get("children")
        extracted_posts = []
        for post in posts:
            extracted_post = self.extract_post(post)
            if not extracted_post["id"]:
                logging.warning("Post doesnt have id. Cannot be prepared for publication")
                continue
            extracted_posts.append(extracted_post)

        return extracted_posts

    # "selftext": post["data"]["selftext"] || post["data"]["body"] ,
    def extract_post(self, post):
        return {
        "id": post["data"].get("id"),
        "created_utc": post["data"].get("created_utc"),
        "num_comments": post["data"].get("num_comments"),
        "selftext": post["data"].get("selftext") or post["data"].get("body"),
        "permalink": f'https://www.reddit.com{post["data"].get("permalink")}',
        "subreddit_subscribers": post["data"].get("subreddit_subscribers"),
        "image": post["data"]["preview"]["images"][0]["source"]["url"] if post["data"].get("preview") else None,
        "upvote_ratio": post["data"].get("upvote_ratio"),
        "ups": post["data"].get("ups"),
        "title": post["data"].get("title"),
        "author": post["data"].get("author"),
        "author_fullname": post["data"].get("author_fullname"),
        "num_crossposts": post["data"].get("num_crossposts"),
        "subreddit_id": post["data"].get("subreddit_id"),
    }
