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

import json
import pandas as pd
import numpy as np
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn import decomposition

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
tweets['tweets_clean'] = tweets['tweets_clean'].replace(regex=True,to_replace=r"https\S+",value=r'')
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
for i in range(0,10000):
    try:
        for line in tweets['tweets_clean'][i]:
            listOfTweets.append(line)
    except:
        continue
        
vectorizer = TfidfVectorizer(stop_words='english', min_df=2)
doc_term_matrix = vectorizer.fit_transform(listOfTweets)
#print doc_term_matrix.shape
vocab = vectorizer.get_feature_names() # list of unique vocab, we will use this later
#print len(vocab), '# of unique words'
#print vocab[-10:] # last ten keywords
#print vocab[:10] # first ten keywords

num_topics = 14

clf = decomposition.NMF(n_components=num_topics, random_state=1)
doc_topic = clf.fit_transform(doc_term_matrix)
#print type(doc_topic), doc_topic.shape
print num_topics, clf.reconstruction_err_

topic_words = []
num_top_words = 10

for topic in clf.components_:
    #print topic.shape, topic[:5]
    word_idx = np.argsort(topic)[::-1][0:num_top_words]
    #print word_idx
    words = [vocab[i] for i in word_idx]
    print words
    
print '----end----' * 10    