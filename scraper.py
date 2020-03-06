import json

import GetOldTweets3 as got
from GetOldTweets3.models import Tweet
import string
import time
""" with open('usernames.txt') as f:
    usernames = []
    [usernames.append(x.strip()) for x in f] """

class TweetEncoder(json.JSONEncoder):
    def default(self, obj):
         if isinstance(obj, Tweet):
             return [obj.id, obj.permalink, obj.username, obj.to, obj.text, str(obj.date), str(obj.retweets), str(obj.favorites), str(obj.mentions), obj.hashtags, obj.geo]
         return json.JSONEncoder.default(self, obj)

usernames = ['MikeBloomberg']



for username in usernames:
    print('processing user:', username)

    year = time.localtime(time.time()).tm_year

    while True:
        end = str(year) + '-12-31'
        start =  str(year) + '-01-01'

        print('Querying time interval ' + start + ' - ' + end)
        tweetCriteria = got.manager.TweetCriteria().setUsername(username).setSince(start).setUntil(end)
        tweets = got.manager.TweetManager.getTweets(tweetCriteria)
        print('Found', len(tweets), 'tweets.')

        if (len(tweets) == 0):
            break
        with open('./data/raw/' + username + '.txt', mode='a') as f:
            for tweet in tweets:
                f.write(json.dumps(tweet, cls=TweetEncoder, ensure_ascii=False))
                f.write('\n')

        time.sleep(120)
        year = year - 1