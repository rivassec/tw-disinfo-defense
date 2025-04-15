import json
import requests
from requests_oauthlib import OAuth1
import sys
import csv
from time import sleep

whitelist = ['orvtech']

shitlist = ['amaia_roja', 'anat5', 'carollafra', 'contraofensiva', 
            'correoorinoco', 'forocandanga', 'guerrillaragua', 
            'hectorodriguez', 'izarradeverdad', 'jorgerpsuv', 
            'jrodriguezpsuv', 'lahojillaentv', 'laradiodelsur', 
            'maperezpirela', 'nicolasmaduro', 'prisciliano_alf', 
            'thaivama', 'yndiratorregros', 'PatriciaDorta40']



#credentials from ghost account get your keys from https://apps.twitter.com/
consumer_key=''
consumer_secret=''
access_token_key=''
access_token_secret=''


#credentials from actual account get your keys from https://apps.twitter.com/ 
consumer_key2=''
consumer_secret2=''
access_token_key2=''
access_token_secret2=''



def get_retweets(tweetid):
  retweetdata={}
  handles=[]
  api_url="https://api.twitter.com/1.1/statuses/retweets/"+tweetid+".json"
  payload = {'count':'100'}
  auth = OAuth1(consumer_key, consumer_secret, access_token_key, access_token_secret)
  r = requests.get(api_url, stream=False, auth=auth, params=payload)
  try:
    if r.headers['x-rate-limit-remaining'] and r.headers['x-rate-limit-remaining'] == "0":
      print("We reached rate limit for ", api_url)
      print("Try again at", r.headers["x-rate-limit-reset"])
      quit()
  except KeyboardInterrupt:
      sys.exit()
  except:
     print "OK"
  retweetsObj = json.loads(r.content)
  for y in range(len(retweetsObj)):
    handles.append(retweetsObj[y]['user']['screen_name'])
  return handles



BLOCK_URL = 'https://api.twitter.com/1.1/blocks/create.json'
MUTE_URL = 'https://api.twitter.com/1.1/mutes/users/create.json'

def getTweets(usuarios):
   api_url="https://api.twitter.com/1.1/statuses/user_timeline.json"
   payload = {'screen_name': usuarios, 'count':'1', 'trim_user':'t', 'include_rts':'false'}
   auth = OAuth1(consumer_key, consumer_secret, access_token_key, access_token_secret)
   r = requests.get(api_url, stream=False, auth=auth, params=payload)
   statusObj = json.loads(r.content)
   return statusObj[0]['id']


def act_on_handle(api_url, auth, payload):
    try:
       r = requests.post(api_url, stream=False, auth=auth, params=payload)
       msgs = json.loads(r.content)
       print r.headers['status'] , payload
       if r.headers['x-rate-limit-remaining'] and r.headers['x-rate-limit-remaining'] == "0":
          print('We reached rate limit for {url}'.format(url=api_url))
          print('Try again at {reset}'.format(reset=r.headers["x-rate-limit-reset"]))
          sys.exit()
    except KeyboardInterrupt:
       sys.exit()
    except:
       pass



def main():
    for cuenta in shitlist:
       try:
         tweet = str(getTweets(cuenta))
         print "\nAnalizyng retweeters of" , cuenta , "TweetID:", tweet
         print "https://twitter.com/" + cuenta + "/status/" + tweet
         HANDLES = get_retweets(tweet)
         for user in HANDLES:
            if user not in whitelist:
              auth2 = OAuth1(consumer_key2, consumer_secret2, access_token_key2, access_token_secret2)
              payload = "screen_name=" + user
              #act_on_handle(BLOCK_URL, auth2, payload)
              act_on_handle(MUTE_URL, auth2, payload)
              sleep(1)
            else:
              print "YOU FOLLOW " , user , "WHO RETWEETED" , cuenta
              sleep(40)
         sleep(60)
       except KeyboardInterrupt:
         sys.exit()
       except:
         pass
     
if __name__ == '__main__':
    main()
