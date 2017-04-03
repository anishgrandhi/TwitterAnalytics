# TwitterAnalytics
A twitter analytics project that collects tweets on President Trump - Performs sentimental analysis, topic modeling 
and also creates a Word Cloud.

CollectTweets.py - 
1. Collects tweets from Twitter using your credentials from a json file which contains your access tokens.
2. Twython module is used to connect to Twitter API.
3. You can either search tweets by location or by keyword.

WordCloud.py -
1. From the json file where you collected tweets, all the status(text) are pulled out and a word cloud is created using 
the Word Cloud module.
2. All the tweets are processed - stop words are removed and the words are stemmed using Porter stemmer.

SentimentAnalysis.py - 
1. The text statuses that are extracted from json file are analyzed using nltk package.
2. You can plot a polarity and a subjectivity histogram

TopicModeling_LDA.py, TopicModeling_NMF.py -
1. Two different approaches are taken for topic modelling.
2. Stop words are removed and the words in the tweets are stemmed using Proter stemmer.
3. The words inside the tweets are then fed to the topic modeling modules to extract topics that people are speaking about.
