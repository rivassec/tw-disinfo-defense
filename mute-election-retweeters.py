import json
import requests
from requests_oauthlib import OAuth1
import sys
from time import sleep

# Define target and allowlist
whitelist = ["orvtech"]
shitlist = [
    "realDonaldTrump",
    "immigrant4trump",
    "KatrinaPierson",
    "Always_Trump",
    "Always_Trump",
    "AnnCoulter",
]

# Ghost account credentials (used for fetching tweets)
consumer_key = ""
consumer_secret = ""
access_token_key = ""
access_token_secret = ""

# Actual account credentials (used for muting/blocking)
consumer_key2 = ""
consumer_secret2 = ""
access_token_key2 = ""
access_token_secret2 = ""

BLOCK_URL = "https://api.twitter.com/1.1/blocks/create.json"
MUTE_URL = "https://api.twitter.com/1.1/mutes/users/create.json"


def get_retweets(tweetid):
    # Return a list of screen_names who retweeted the given tweet.
    api_url = f"https://api.twitter.com/1.1/statuses/retweets/{tweetid}.json"
    payload = {"count": "100"}
    auth = OAuth1(consumer_key, consumer_secret, access_token_key, access_token_secret)

    try:
        r = requests.get(api_url, auth=auth, params=payload)
        if r.headers.get("x-rate-limit-remaining") == "0":
            print(f"[RATE LIMIT] Reached for {api_url}")
            print(f"Try again at {r.headers['x-rate-limit-reset']}")
            sys.exit()
    except KeyboardInterrupt:
        sys.exit()
    except:
        print("[WARN] Error occurred during retweet fetch")

    handles = [entry["user"]["screen_name"] for entry in r.json()]
    return handles


def get_latest_tweet_id(username):
    # Return the ID of the latest tweet from the given username.
    api_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    payload = {
        "screen_name": username,
        "count": "1",
        "trim_user": "t",
        "include_rts": "false",
    }
    auth = OAuth1(consumer_key, consumer_secret, access_token_key, access_token_secret)
    r = requests.get(api_url, auth=auth, params=payload)
    return str(r.json()[0]["id"])


def act_on_handle(api_url, auth, payload):
    # Mute or block a user via POST request.
    try:
        r = requests.post(api_url, auth=auth, params=payload)
        print(f"[ACTION] {r.headers.get('status', 'unknown')} - {payload}")
        if r.headers.get("x-rate-limit-remaining") == "0":
            print(f"[RATE LIMIT] Reached for {api_url}")
            print(f"Try again at {r.headers['x-rate-limit-reset']}")
            sys.exit()
    except KeyboardInterrupt:
        sys.exit()
    except:
        print("[WARN] Action failed or was skipped")


def main():
    for target_account in shitlist:
        try:
            tweet_id = get_latest_tweet_id(target_account)
            print(
                f"\n[INFO] Analyzing retweeters of @{target_account} (Tweet ID: {tweet_id})"
            )
            print(f"https://twitter.com/{target_account}/status/{tweet_id}")

            handles = get_retweets(tweet_id)
            for user in handles:
                if user not in whitelist:
                    auth2 = OAuth1(
                        consumer_key2,
                        consumer_secret2,
                        access_token_key2,
                        access_token_secret2,
                    )
                    payload = {"screen_name": user}
                    # Uncomment below to block users as well
                    # act_on_handle(BLOCK_URL, auth2, payload)
                    act_on_handle(MUTE_URL, auth2, payload)
                    sleep(1)
                else:
                    print(f"[SKIP] YOU FOLLOW @{user} WHO RETWEETED @{target_account}")
                    sleep(40)
            sleep(60)
        except KeyboardInterrupt:
            sys.exit()
        except:
            print(f"[WARN] Skipping @{target_account} due to error")


if __name__ == "__main__":
    main()
