Python-tools-for-twitter
========================

Scripts and tools for doing twittery stuff


**deleteDMs.py**
Deletes all direct messages in authenticated users account.


**unfollow-unfollowers.py**
Unfollows any user who doesnt follows you.

**shushbully.py**
Mutes or blocks users retweeting a specific user, usefull when a series of accounts with a large number of followers attack you.

This particular scripts uses two sets of credentials, one for reading the retweets and the ones from the account that is under attack, this also help us a bit on not reaching the ratelimit on our application.

By default the script will only mute the retweeters but you can uncomment a line to allow it to also block the accounts retweeting.

**shushellections.py**
It is a quick adaptation of shushbully.py, you can replace the account with your 'favorite' politicians, activists, or accounts you just want to mute their retweeters. #hihaters
