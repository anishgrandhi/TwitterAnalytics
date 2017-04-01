# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 08:18:26 2017

@author: Anish

References
Pandas dataframe - http://adilmoujahid.com/posts/2014/07/twitter-analytics/
Stop words removal - http://stackoverflow.com/questions/33245567/stopword-removal-with-nltk-and-pandas
stemming - http://stackoverflow.com/questions/37443138/python-stemming-with-pandas-dataframe
Punctuation - http://stackoverflow.com/questions/39782418/remove-punctuations-in-pandas
"""

from __future__ import division, print_function
import json
import pandas as pd
#import numpy as np
import nltk
#from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models

import logging
logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO

data_twitter = []
tweets_file = open("tweet_stream_Central_6k.json", "r")
for line in tweets_file:
    try:
        data_twitter.append(json.loads(line))
    except:
        continue
    
tweets = pd.DataFrame()
tweets['text'] = map(lambda tweet: tweet['text'], data_twitter)

stopwords = nltk.corpus.stopwords.words('english')

tweets['tweets_clean'] = tweets['text'].replace(regex=True,to_replace=r"RT @\S+",value=r'')
tweets['tweets_clean'] = tweets['tweets_clean'].replace(regex=True,to_replace=r"http\S+",value=r'')
tweets['tweets_clean'] = tweets['tweets_clean'].replace(regex=True,to_replace=r'(?i).*trump*',value=r'')
tweets['tweets_clean'] = tweets['tweets_clean'].replace(regex=True,to_replace=r'(?i).*president*',value=r'')
tweets['tweets_clean'] = tweets['tweets_clean'].replace(regex=True,to_replace=r'(?i).*say*',value=r'')
tweets['tweets_clean'] = tweets['tweets_clean'].replace(regex=True,to_replace=r'(?i).*know*',value=r'')

#tweets['tweets_clean'] = tweets['tweets_clean'].replace(regex=True,to_replace=r'(?i).*cnn*',value=r'')
#tweets['tweets_clean'] = tweets['tweets_clean'].replace(regex=True,to_replace=r'(?i).*cnbc*',value=r'')
#tweets['tweets_clean'] = tweets['tweets_clean'].replace(regex=True,to_replace=r'(?i).*cbs*',value=r'')

tweets['tweets_clean'] = tweets['tweets_clean'].replace(regex=True,to_replace=r'(?i).tweet',value=r'')
tweets['tweets_clean'] = tweets['tweets_clean'].replace(regex=True,to_replace=r'(?i).need',value=r'')
tweets['tweets_clean'] = tweets['tweets_clean'].replace(regex=True,to_replace=r'(?i).know*',value=r'')
tweets['tweets_clean'] = tweets['tweets_clean'].str.replace('[^\w\s]','')
tweets['tweets_clean'] = tweets['tweets_clean'].replace(regex=True,to_replace=r'(?i).*potus*',value=r'')
tweets['tweets_clean'] = tweets['tweets_clean'].replace(regex=True,to_replace=r'(?i).*amp*',value=r'')
tweets['tweets_clean'] = tweets['tweets_clean'].str.lower().str.split()

tweets['tweets_clean'] = tweets['tweets_clean'].apply(lambda x: [item for item in x if item not in stopwords])

ps = PorterStemmer()
tweets['tweets_clean'] = tweets['tweets_clean'].apply(lambda x: [ps.stem(word) for word in x])

listOfTweets = []
for line in tweets['tweets_clean']:
    try:
        listOfTweets.append(line)
    except:
        continue


dic = corpora.Dictionary(listOfTweets)
corpus = [dic.doc2bow(text) for text in listOfTweets]
print(type(corpus), len(corpus))
    
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

NUM_TOPICS = 16
model = models.ldamodel.LdaModel(corpus_tfidf, 
                                 num_topics=NUM_TOPICS, 
                                 id2word=dic, 
                                 update_every=1, 
                                 passes=100)
print("LDA model")
topics_found = model.print_topics(20)
for t in topics_found:
    #print(t[1].split('+'), type(t[1]))
    print(t[1].split('+'))