# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 19:41:03 2017

@author: Anish

References
Pandas dataframe - http://adilmoujahid.com/posts/2014/07/twitter-analytics/
"""

import json
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

data_twitter = []
tweets_file = open("tweet_stream_NewJersey_10k.json", "r")
for line in tweets_file:
    try:
        data_twitter.append(json.loads(line))
    except:
        continue
    
tweets = pd.DataFrame()
tweets['text'] = map(lambda tweet: tweet['text'], data_twitter)

del data_twitter[:]


tweets['blobs'] = tweets['text'].apply(lambda tweet: TextBlob(tweet))
tweets['polarity'] = tweets['blobs'].apply(lambda tweet: tweet.polarity)
tweets['subjectivity'] = tweets['blobs'].apply(lambda tweet: tweet.subjectivity)

plt.hist(tweets['polarity'], bins=15)
plt.xlabel('polarity score')
plt.ylabel('Number of Tweets')
plt.grid(True)
#plt.savefig('subjectivity.pdf')
plt.show()

plt.hist(tweets['subjectivity'], bins=15)
plt.xlabel('Subjectivity score')
plt.ylabel('Number of Tweets')
plt.grid(True)
#plt.savefig('subjectivity.pdf')
plt.show()

print ("Polarity mean = {}".format(tweets['polarity'].mean()))
print ("Subjectivity mean = {}".format(tweets['subjectivity'].mean()))