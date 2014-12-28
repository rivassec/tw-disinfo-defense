import json
import requests
from requests_oauthlib import OAuth1
import re
from time import sleep
import operator
import sys
import os
import collections


consumer_key=''
consumer_secret=''
access_token_key=''
access_token_secret=''



def get_follower_ids():
  cursor = "-1"
  listadeIDs = []
  while cursor != '0':
    try:
      api_url='https://api.twitter.com/1.1/followers/ids.json'
      payload = {'count':'5000', 'cursor':cursor}
      auth = OAuth1(consumer_key, consumer_secret, access_token_key, access_token_secret)
      r = requests.get(api_url, stream=False, auth=auth, params=payload)
      if r.headers['x-rate-limit-remaining'] and r.headers['x-rate-limit-remaining'] == "0":
        time_out = int(r.headers["x-rate-limit-reset"]) - int(time.time())
        print("We reached rate limit for ", api_url)
        print "Try again in", time_out, "seconds"
        quit()
      IDs = json.loads(r.content)
      cursor = IDs['next_cursor_str']
      listadeIDs = listadeIDs + IDs['ids']
      sleep(1)
    except KeyError:
      print "Unable to navigate through cursors, last attempt: ", cursor
      break
  return list(set(listadeIDs))


def get_friends_ids():
  cursor = "-1"
  listadeIDs = []
  while cursor != '0':
    try:
      api_url='https://api.twitter.com/1.1/friends/ids.json'
      payload = {'count':'5000', 'cursor':cursor}
      auth = OAuth1(consumer_key, consumer_secret, access_token_key, access_token_secret)
      r = requests.get(api_url, stream=False, auth=auth, params=payload)
      if r.headers['x-rate-limit-remaining'] and r.headers['x-rate-limit-remaining'] == "0":
        print("We reached rate limit for ", api_url)
        print("Try again at", r.headers["x-rate-limit-reset"])
        quit()
      IDs = json.loads(r.content)
      cursor = IDs['next_cursor_str']
      listadeIDs = listadeIDs + IDs['ids']
      sleep(1)
    except KeyError:
      print "Unable to navigate through cursors, last attempt: ", cursor
      break
  return list(set(listadeIDs))






def get_unfollowers_info(unfollowers):
   print len(unfollowers)
   api_url='https://api.twitter.com/1.1/users/lookup.json'
   auth = OAuth1(consumer_key, consumer_secret, access_token_key, access_token_secret)
   user_objs = {}
   sleep(1)
   i = 0
   user_id = []
   for i in unfollowers:
     user_id.append(i)
     if (len(user_id) == 100):
       payload = {'user_id':user_id}
       r = requests.get(api_url, stream=False, auth=auth, params=payload)
       if r.headers['x-rate-limit-remaining'] and r.headers['x-rate-limit-remaining'] == "0":
         print("We reached rate limit for ", api_url)
         print("Try again at", r.headers["x-rate-limit-reset"])
         quit()
       tmp_user_objs = json.loads(r.content)
       for y in range(len(tmp_user_objs)):
         print tmp_user_objs[y]['screen_name'] , tmp_user_objs[y]['followers_count'] , tmp_user_objs[y]['friends_count'] , tmp_user_objs[y]['following'] , tmp_user_objs[y]['verified'], tmp_user_objs[y]['default_profile']
       user_objs = user_objs , tmp_user_objs
       user_id = []
   payload = {'user_id':user_id}
   r = requests.get(api_url, stream=False, auth=auth, params=payload)
   if r.headers['x-rate-limit-remaining'] and r.headers['x-rate-limit-remaining'] == "0":
     print("We reached rate limit for ", api_url)
     print("Try again at", r.headers["x-rate-limit-reset"])
     quit()
   tmp_user_objs = json.loads(r.content)
   user_objs = user_objs , tmp_user_objs

def unfollow_by_id(user_id):
  api_url='https://api.twitter.com/1.1/friendships/destroy.json'
  payload = {'user_id':user_id}
  auth = OAuth1(consumer_key, consumer_secret, access_token_key, access_token_secret)
  r = requests.post(api_url, stream=False, auth=auth, params=payload)


followers = get_follower_ids()
print "Followers: ", len(followers)
following = get_friends_ids()
print "Following: ", len(following)

unfollower_ids = set(following) - set(followers)
print "unfollower ids: ", unfollower_ids , len(unfollower_ids)


get_unfollowers_info(unfollower_ids)
print "About to unfollow: " , len(unfollower_ids) , "users."
sleep(10)

for user_id in unfollower_ids:
  print "Unfollowing ", user_id
  unfollow_by_id(user_id)    
