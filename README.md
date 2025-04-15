# Twitter Cleanup Toolkit
[![Trivy Scan](https://github.com/rivassec/twitter-cleanup-toolkit/actions/workflows/trivy.yml/badge.svg?branch=main)](https://github.com/rivassec/twitter-cleanup-toolkit/actions/workflows/trivy.yml)

This repository contains a set of Python scripts for automating common Twitter hygiene tasks using the Twitter v1.1 API and `requests_oauthlib`.

⚠️ **Disclaimer**: These tools were written for educational and personal security purposes. They rely on the legacy Twitter API and may break or require adaptation as Twitter's API evolves. Use responsibly and within the terms of service.

---

## Scripts

### 1. `delete-dms.py`
Deletes all direct messages (DMs), both sent and received, from the authenticated account.

### 2. `unfollow-nonfollowers.py`
Identifies users you follow who do not follow you back and unfollows them after showing their profile info.

### 3. `mute-retweeters.py`
Fetches the latest tweet from a predefined list of users (e.g., disinformation accounts), identifies users who retweeted it, and mutes them using a secondary account.

### 4. `mute-election-retweeters.py`
Similar to the script above, but focuses on a more targeted set of disinformation sources around elections. Allows basic whitelisting.

---

## Setup

1. Clone this repo:
```bash
git clone https://github.com/yourusername/twitter-cleanup-toolkit.git
cd twitter-cleanup-toolkit
```

2. Install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Set your Twitter API credentials inside each script:
```python
consumer_key = "..."
consumer_secret = "..."
access_token_key = "..."
access_token_secret = "..."
```

---

## Security Notice

- These tools use OAuth1, which requires sensitive tokens.
- Do not commit your credentials.
- Rate limits are handled with crude checks — scripts will exit on hitting limits.

---

## License

MIT — use at your own risk.
