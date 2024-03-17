import httpx
import json


class TwitterDownloader:
    def __init__(self):
        pass

    def get_posts(self, user_id):
        url = 'https://twitter.com/i/api/graphql/WwS-a6hAhqAAe-gItelmHA/UserTweets'

        variables = {
            "userId": user_id,
            "count": 20,
            "cursor": "DAABCgABGIdz9eT__-UKAAIYgh2mGhdQ6ggAAwAAAAIAAA",
            "includePromotedContent": True,
            "withQuickPromoteEligibilityTweetFields": True,
            "withVoice": True,
            "withV2Timeline": True
        }

        features = {
            "responsive_web_graphql_exclude_directive_enabled": True,
            "verified_phone_label_enabled": False,
            "creator_subscriptions_tweet_preview_api_enabled": True,
            "responsive_web_graphql_timeline_navigation_enabled": True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "c9s_tweet_anatomy_moderator_badge_enabled": True,
            "tweetypie_unmention_optimization_enabled": True,
            "responsive_web_edit_tweet_api_enabled": True,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
            "view_counts_everywhere_api_enabled": True,
            "longform_notetweets_consumption_enabled": True,
            "responsive_web_twitter_article_tweet_consumption_enabled": True,
            "tweet_awards_web_tipping_enabled": False,
            "freedom_of_speech_not_reach_fetch_enabled": True,
            "standardized_nudges_misinfo": True,
            "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
            "rweb_video_timestamps_enabled": True,
            "longform_notetweets_rich_text_read_enabled": True,
            "longform_notetweets_inline_media_enabled": True,
            "responsive_web_enhance_cards_enabled": False
        }

        headers = {
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "cookie": 'des_opt_in=Y; twtr_pixel_opt_in=Y; guest_id=v1%3A169468880047459457; kdt=vrsOFaaE3Ap1HLgBEeK9Lt1KAkpOVCofqPFGXj4U; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCK7H2y%252BOAToMY3NyZl9p%250AZCIlYzEyYzJjZDEzOWExZGY0YzJiMTZkZTk4MzY4OTU4N2Q6B2lkIiUzYTFi%250AMzljZmE4YzE4MmZlYzMyMWFjNzZhMmZhNGRmYw%253D%253D--28c6974765270cfe49ccd1438205de4d1600cdd3; g_state={"i_l":0}; auth_token=d80912d8f897ad17a772fcfcb959a26326a03f77; ct0=f153cb895e8150f46e1c135175d2b95812bd7c985cb84baa7619da61f649c330817cc9ae60d5699438f17ab9cd4918628950502751255bf4421d972daa7f03af51e222de35d49c0d91bfac7742182990; att=1-CIUafeDXxMg1qwxLHmAFEwcqikE7GOTU6DmuHhFD; lang=en; twid=u%3D1559499647877582849; d_prefs=MToxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw; guest_id_ads=v1%3A169468880047459457; guest_id_marketing=v1%3A169468880047459457; personalization_id="v1_5MAfF+YLKq5XNsJziNMdoA=="; _ga=GA1.2.473077003.1710241343; _gid=GA1.2.1311584651.1710241343; ct0=e7b33b4638b2be0a17369abb509a1adeb3a49d8040ded0f557e84d9cd76bc176f3910bc1eb77bcfa127814429869a487f37b9dc6990477d5420e30cd0b112b221c4d4dc2da6831821ab76c88a5991646',
            "x-client-uuid": "a4f2f9dc-50f6-42cf-a2f3-f6180564244f",
            "x-csrf-token": "f153cb895e8150f46e1c135175d2b95812bd7c985cb84baa7619da61f649c330817cc9ae60d5699438f17ab9cd4918628950502751255bf4421d972daa7f03af51e222de35d49c0d91bfac7742182990"
        }

        variables_encoded = json.dumps(variables)
        features_encoded = json.dumps(features)

        response = httpx.get(
            url,
            params={'variables': variables_encoded, 'features': features_encoded},
            headers=headers
        )

        response_json = json.loads(response.text)
        first_post = response_json["data"]["user"]["result"]['timeline_v2']['timeline']['instructions'][0]["entry"]
        rest_posts = response_json["data"]["user"]["result"]['timeline_v2']['timeline']['instructions'][1]["entries"]
        posts = [first_post] + rest_posts
        screen_name = response_json["data"]["user"]["result"]['timeline_v2']['timeline']['instructions'][0]["entry"]["content"]["itemContent"]["tweet_results"]["result"]["core"]["user_results"]["result"]["legacy"]["screen_name"]
        extracted_posts = []

        for post in posts:
            extracted_post = self.extract_post(post, screen_name)
            if extracted_post is None:
                continue

            extracted_posts.append(extracted_post)

        return extracted_posts

    def extract_post(self, post, screen_name):
        try:
            legacy = post.get("content").get('itemContent').get('tweet_results').get('result').get('legacy')
        except:
            try:
                legacy = post.get("content").get('items')[0].get('item').get('itemContent').get('tweet_results').get('result').get(
                'legacy')
            except:
                return None

        post_id = legacy.get('id_str')

        return {
            "id": post_id,
            'created_at': legacy.get('created_at'),
            'favorite_count': legacy.get('favorite_count'),
            'full_text': legacy.get('full_text'),
            'lang': legacy.get('lang'),
            'quote_count': legacy.get('quote_count'),
            'reply_count': legacy.get('reply_count'),
            'retweet_count': legacy.get('retweet_count'),
            'user_id_str': legacy.get('user_id_str'),
            'post_url': f"https://twitter.com/{screen_name}/status/{post_id}",
            'company_name': screen_name
        }
