import json
import requests
from requests_oauthlib import OAuth1
from time import sleep, time
import sys

# OAuth credentials
consumer_key = ""
consumer_secret = ""
access_token_key = ""
access_token_secret = ""

def get_follower_ids():
    cursor = "-1"
    list_of_ids = []

    while cursor != "0":
        try:
            api_url = "https://api.twitter.com/1.1/followers/ids.json"
            payload = {"count": "5000", "cursor": cursor}
            auth = OAuth1(consumer_key, consumer_secret, access_token_key, access_token_secret)
            r = requests.get(api_url, auth=auth, params=payload)

            if r.headers.get("x-rate-limit-remaining") == "0":
                timeout = int(r.headers["x-rate-limit-reset"]) - int(time())
                print(f"[RATE LIMIT] Reached for {api_url}. Try again in {timeout} seconds.")
                sys.exit()

            ids = r.json()
            cursor = ids["next_cursor_str"]
            list_of_ids.extend(ids["ids"])
            sleep(1)
        except KeyError:
            print(f"[ERROR] Unable to continue with cursor: {cursor}")
            break

    return list(set(list_of_ids))

def get_friends_ids():
    cursor = "-1"
    list_of_ids = []

    while cursor != "0":
        try:
            api_url = "https://api.twitter.com/1.1/friends/ids.json"
            payload = {"count": "5000", "cursor": cursor}
            auth = OAuth1(consumer_key, consumer_secret, access_token_key, access_token_secret)
            r = requests.get(api_url, auth=auth, params=payload)

            if r.headers.get("x-rate-limit-remaining") == "0":
                print(f"[RATE LIMIT] Reached for {api_url}. Try again at {r.headers['x-rate-limit-reset']}")
                sys.exit()

            ids = r.json()
            cursor = ids["next_cursor_str"]
            list_of_ids.extend(ids["ids"])
            sleep(1)
        except KeyError:
            print(f"[ERROR] Unable to continue with cursor: {cursor}")
            break

    return list(set(list_of_ids))

def get_unfollowers_info(unfollowers):
    print(f"[INFO] Total unfollowers: {len(unfollowers)}")
    api_url = "https://api.twitter.com/1.1/users/lookup.json"
    auth = OAuth1(consumer_key, consumer_secret, access_token_key, access_token_secret)

    user_objs = []
    user_ids_batch = []

    for uid in unfollowers:
        user_ids_batch.append(uid)
        if len(user_ids_batch) == 100:
            payload = {"user_id": user_ids_batch}
            r = requests.get(api_url, auth=auth, params=payload)

            if r.headers.get("x-rate-limit-remaining") == "0":
                print(f"[RATE LIMIT] Reached for {api_url}. Try again at {r.headers['x-rate-limit-reset']}")
                sys.exit()

            tmp_user_objs = r.json()
            for user in tmp_user_objs:
                print(
                    user["screen_name"],
                    user["followers_count"],
                    user["friends_count"],
                    user.get("following"),
                    user["verified"],
                    user["default_profile"],
                )
            user_objs.extend(tmp_user_objs)
            user_ids_batch = []
            sleep(1)

    if user_ids_batch:
        payload = {"user_id": user_ids_batch}
        r = requests.get(api_url, auth=auth, params=payload)
        if r.headers.get("x-rate-limit-remaining") == "0":
            print(f"[RATE LIMIT] Reached for {api_url}. Try again at {r.headers['x-rate-limit-reset']}")
            sys.exit()
        tmp_user_objs = r.json()
        user_objs.extend(tmp_user_objs)

def unfollow_by_id(user_id):
    api_url = "https://api.twitter.com/1.1/friendships/destroy.json"
    payload = {"user_id": user_id}
    auth = OAuth1(consumer_key, consumer_secret, access_token_key, access_token_secret)
    r = requests.post(api_url, auth=auth, params=payload)
    if r.status_code == 200:
        print(f"[OK] Unfollowed {user_id}")
    else:
        print(f"[ERROR] Failed to unfollow {user_id} — HTTP {r.status_code}")

# Execution begins
followers = get_follower_ids()
print(f"[INFO] Followers: {len(followers)}")

following = get_friends_ids()
print(f"[INFO] Following: {len(following)}")

unfollower_ids = set(following) - set(followers)
print(f"[INFO] Unfollowers (not following back): {len(unfollower_ids)}")

get_unfollowers_info(unfollower_ids)
print(f"[ACTION] Preparing to unfollow {len(unfollower_ids)} users in 10 seconds...")
sleep(10)

for user_id in unfollower_ids:
    print(f"[ACTION] Unfollowing {user_id}")
    unfollow_by_id(user_id)
