# tweet classifier

## scraper.py

A wrapper for GetOldTweets3 to get around Twitter limits . Queries all tweets for Twitter users 'realDonaldTrump' and 'MikeBloomberg' or users listed in a file if flag -u given.

## presidential_tweet_classifier.py

A script which cleans scraped tweets and implements a simple NLP pipleline fitting models allowing prediction of the author of tweets.

