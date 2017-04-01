# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 19:44:42 2017

@author: Anish

References
Pandas dataframe - http://adilmoujahid.com/posts/2014/07/twitter-analytics/
Stop words removal - http://stackoverflow.com/questions/33245567/stopword-removal-with-nltk-and-pandas
stemming - http://stackoverflow.com/questions/37443138/python-stemming-with-pandas-dataframe
Punctuation - http://stackoverflow.com/questions/39782418/remove-punctuations-in-pandas
"""

import json
import pandas as pd
import nltk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

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

stopwords = nltk.corpus.stopwords.words('english')

tweets['tweets_clean'] = tweets['text'].replace(regex=True,to_replace=r"RT @\S+",value=r'')
tweets['tweets_clean'] = tweets['tweets_clean'].replace(regex=True,to_replace=r"https\S+",value=r'')
tweets['tweets_clean'] = tweets['tweets_clean'].replace(regex=True,to_replace=r'(?i).*trump*',value=r'')
tweets['tweets_clean'] = tweets['tweets_clean'].replace(regex=True,to_replace=r'(?i).*president*',value=r'')
tweets['tweets_clean'] = tweets['tweets_clean'].replace(regex=True,to_replace=r'(?i).*say*',value=r'')
tweets['tweets_clean'] = tweets['tweets_clean'].replace(regex=True,to_replace=r'(?i).*nightly*',value=r'')

tweets['tweets_clean'] = tweets['tweets_clean'].replace(regex=True,to_replace=r'(?i).tweet',value=r'')
tweets['tweets_clean'] = tweets['tweets_clean'].replace(regex=True,to_replace=r'(?i).need',value=r'')
tweets['tweets_clean'] = tweets['tweets_clean'].replace(regex=True,to_replace=r'(?i).know*',value=r'')
tweets['tweets_clean'] = tweets['tweets_clean'].replace(regex=True,to_replace=r'(?i).go*',value=r'')


tweets['tweets_clean'] = tweets['tweets_clean'].replace(regex=True,to_replace=r'(?i).*potus*',value=r'')
tweets['tweets_clean'] = tweets['tweets_clean'].replace(regex=True,to_replace=r'(?i).*amp*',value=r'')
tweets['tweets_clean'] = tweets['tweets_clean'].str.lower().str.split()
tweets['tweets_nostp'] = tweets['tweets_clean'].apply(lambda x: [item for item in x if item not in stopwords])
tweets['tweets_stem'] = tweets['tweets_nostp'].apply(lambda x: [ps.stem(word) for word in x])



text = ' '
for i in range(0,10000):
    try:
        for word in tweets['tweets_stem'][i]:
            text = text +' '+ word
    except:
        continue
        
wordcloud = WordCloud(max_font_size=100,background_color="white",).generate(text) 

# Display the generated image:
plt.figure()
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
