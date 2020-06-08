# tweet classifier

## scraper.py

A wrapper for GetOldTweets3 to get around Twitter limits . Queries all tweets for Twitter users 'realDonaldTrump' and 'MikeBloomberg' or users listed in a file if flag -u given.

## presidential_tweet_classifier.py

A script which cleans scraped tweets and implements a simple NLP pipleline fitting models allowing prediction of the author of tweets.

Creation pipleline:

1. Filter samples (tweets) so that very short messages are thrown away. 100 characters default threshold.
2. Samples are tokenized and lemmatized. Non-alpha tokens and stop words are removed. Also tokens with no lemma found (that is, words not in the English vocabulary) are removed.
3. Each sample is converted to numeric. The result is a N x F matrix in which N is the amount of samples and F is the amount of features.
4. Dimensionality reduction is applied so that the result is N x <img src="https://render.githubusercontent.com/render/math?math=\tilde{F}"> matrix where <img src="https://render.githubusercontent.com/render/math?math=\tilde{F}"> = 100. Original F was around 30000. Dimensionality reduction used is truncated singular value decomposition.
5. An SVC (C-Support Vector Classifier) is fitted with with data generated with SVD

Steps to obtain classifications:

1. Repeat steps 1 - 3 for unseen sample(s).
2. Transform the sample(s) with SVD fitted in step 4.
3. Obtain results from SVC.
