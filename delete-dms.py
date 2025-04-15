import json
import requests
from requests_oauthlib import OAuth1

# Twitter API credentials
consumer_key = "<YOUR CONSUMER KEY HERE>"
consumer_secret = "<YOUR CONSUMER SECRET HERE>"
access_token_key = "<YOUR ACCESS TOKEN HERE>"
access_token_secret = "<YOUR ACCESS TOKEN SECRET HERE>"


def get_messages_ids():
    """Retrieve IDs of received and sent direct messages."""
    message_ids = []
    auth = OAuth1(consumer_key, consumer_secret, access_token_key, access_token_secret)

    for endpoint in [
        "https://api.twitter.com/1.1/direct_messages.json",
        "https://api.twitter.com/1.1/direct_messages/sent.json",
    ]:
        payload = {"count": "200"}
        r = requests.get(endpoint, auth=auth, params=payload)

        if r.headers.get("x-rate-limit-remaining") == "0":
            print(f"[RATE LIMIT] Reached for {endpoint}")
            print(f"Try again at {r.headers['x-rate-limit-reset']}")
            quit()

        try:
            dms = r.json()
            for dm in dms:
                message_ids.append(dm["id"])
        except Exception as e:
            print(f"[ERROR] Failed to parse response from {endpoint}: {e}")

    return message_ids


def nuke_messages(dm_ids):
    """Delete direct messages by ID."""
    endpoint = "https://api.twitter.com/1.1/direct_messages/destroy.json"
    auth = OAuth1(consumer_key, consumer_secret, access_token_key, access_token_secret)

    for msg_id in dm_ids:
        payload = {"id": msg_id}
        r = requests.post(endpoint, auth=auth, params=payload)
        if r.status_code == 200:
            print(f"[OK] Deleted DM ID: {msg_id}")
        else:
            print(f"[ERROR] Failed to delete DM ID: {msg_id} — HTTP {r.status_code}")


def main():
    while True:
        dm_ids = get_messages_ids()
        if dm_ids:
            print(f"[INFO] Deleting {len(dm_ids)} messages: {dm_ids}")
            nuke_messages(dm_ids)
        else:
            print("[INFO] No more messages to delete.")
            break


if __name__ == "__main__":
    main()
