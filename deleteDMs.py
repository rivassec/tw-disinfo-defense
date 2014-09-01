import json
import requests
from requests_oauthlib import OAuth1

consumer_key='<YOUR CONSUMER KEY HERE>'
consumer_secret='<YOUR CONSUMER SECRET HERE>'
access_token_key='<YOUR ACCESS TOKEN HERE>'
access_token_secret='<YOUR ACCESS TOKEN SECRET HERE>'

def get_messages_ids():
  api_url='https://api.twitter.com/1.1/direct_messages.json'
  payload = {'count':'200', 'cursor':'-1', 'skip_status':'1'}
  auth = OAuth1(consumer_key, consumer_secret, access_token_key, access_token_secret)
  r = requests.get(api_url, stream=False, auth=auth, params=payload)
  if r.headers['x-rate-limit-remaining'] and r.headers['x-rate-limit-remaining'] == "0":
    print("We reached rate limit for ", api_url)
    print("Try again at", r.headers["x-rate-limit-reset"])
    quit()
  DMs = json.loads(r.content)
  message_ids=[]
  for x in range(len(DMs)):
    current_ids=DMs[x]['id']
    message_ids.append(current_ids)
  api_url='https://api.twitter.com/1.1/direct_messages/sent.json'
  payload = {'count':'200'}
  r = requests.get(api_url, stream=False, auth=auth, params=payload)
  if r.headers['x-rate-limit-remaining'] and r.headers['x-rate-limit-remaining'] == "0":
    print("We reached rate limit for ", api_url)
    print("Try again at", r.headers["x-rate-limit-reset"])
    quit()
  DMs = json.loads(r.content)
  for x in range(len(DMs)):
    current_ids=DMs[x]['id']
    message_ids.append(current_ids)
  return message_ids



def nuke_messages(DMs):
  for x in DMs:
    api_url='https://api.twitter.com/1.1/direct_messages/destroy.json'
    payload = {'id':x}
    auth = OAuth1(consumer_key, consumer_secret, access_token_key, access_token_secret)
    r = requests.post(api_url, stream=False, auth=auth, params=payload)


while True: 
  DMs = get_messages_ids()
  if DMs and len(DMs) > 0:
    print('Deleting:', DMs)
    nuke_messages(DMs)
  else:
    print('There appears that there are no more DMs', DMs)
    break
