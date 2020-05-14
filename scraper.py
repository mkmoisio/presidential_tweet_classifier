import json

import GetOldTweets3 as got
from GetOldTweets3.models import Tweet
import string
import time
import datetime
from datetime import date
import inspect

class TweetEncoder(json.JSONEncoder):
    def default(self, obj):
         if isinstance(obj, Tweet):
             return [obj.id, obj.permalink, obj.username, obj.to, obj.text, str(obj.date), str(obj.retweets), str(obj.favorites), str(obj.mentions), obj.hashtags, obj.geo]
         return json.JSONEncoder.default(self, obj)

path_raw = './data/raw/%s.txt'

usernames = ['realDonaldTrump']

beginning_of_time = date(2006, 3, 21)
ttimer = time.time()
for username in usernames:
    print('* Processing user "' +  username + '".')

    sleep_time = 5
    time_slice = 30

    end = date.today() + datetime.timedelta(days=1) # the upper bound in exclusive so set it to be tomorrow
    
    while True:
        start = end - datetime.timedelta(days=time_slice)

        print('** Querying Twitter... (user = ' + username + ', interval = ' + start.isoformat() + ' - ' + end.isoformat() + ', slice = ' + str(time_slice)+ 'd)')
        try:
            timer = time.time()

            tweetCriteria = got.manager.TweetCriteria().setUsername(username).setSince(start.isoformat()).setUntil(end.isoformat())
            tweets = got.manager.TweetManager.getTweets(tweetCriteria)

            tweet_count = len(tweets)
            elapsed = time.time() - timer

            print('>> Query finished (number of tweets = ' + str(tweet_count) + ', elapsed time = {:.2f}'.format(elapsed) + 's).')

            with open(path_raw % username, mode='a') as f:
                for tweet in tweets:
                    f.write(json.dumps(tweet, cls=TweetEncoder, ensure_ascii=False))
                    f.write('\n')

            time_slice *= 2
            sleep_time = max(1, sleep_time // 2)

            end = start

            if end < beginning_of_time:
                print('Scraping finished in {:.2f}'.format(time.time() -  ttimer) + 's.')
                break

        except BaseException as ex:

            # A hacky way to check wether the exception was raised by a failing HTTP request
            if (inspect.trace()[-1][2] == 348 and inspect.trace()[-1][3] == 'getJsonResponse'):
                time_slice = max(1, time_slice // 2)
                sleep_time *= 2
            else:
                print('Something went wrong:', str(ex))
                import sys
                sys.exit()
            
            
            
        print('^^ Sleeping... (sleep_time = ' + str(sleep_time) + 's, time_slice = ' + str(time_slice) + 'd).')
        time.sleep(sleep_time)