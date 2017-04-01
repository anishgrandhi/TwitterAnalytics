# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 12:01:49 2017

@author: Anish
"""

from twython import TwythonStreamer
import sys
import json

count = 0
class MyStreamer(TwythonStreamer):
    '''our own subclass of TwythonStremer'''
    # overriding
    def on_success(self, data):
        global count
        if 'lang' in data and data['lang'] == 'en' and 'trump' in data['text'].lower():
            count+=1
            print count
            if count <= 494:
                self.store_json(data)
            else:
                self.disconnect()
            #tweets.append(data)
            #print len(tweets)
            #print ("received tweet #{} : {}".format(len(tweets),data['text'].encode('utf-8')))
                   
     
    # overriding
    def on_error(self, status_code, data):
        print status_code, data
        self.disconnect()

    def store_json(self,data):
        with open('tweet_stream_California_10k.json', 'a') as f:	
            json.dump(data, f)
            f.write("\n")
        
if __name__ == '__main__':

    #with open('your_twitter_credentials.json', 'r') as f:
    with open('your_twitter_credentials_2.json', 'r') as f:
        credentials = json.load(f)

    # create your own app to get consumer key and secret
    CONSUMER_KEY = credentials['CONSUMER_KEY']
    CONSUMER_SECRET = credentials['CONSUMER_SECRET']
    ACCESS_TOKEN = credentials['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = credentials['ACCESS_TOKEN_SECRET']
        
    stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET,retry_in=20)

#    if len(sys.argv) > 1:
#        keyword = sys.argv[1]
#    else:
#        keyword = 'trump'

    #Put longitude and then latitude of SW point and then long and lat of NE point of the box!!
    
    
    #stream.statuses.filter(track=keyword)
    for i in range (0,6):
        try:
            stream.statuses.filter(locations=[-124.51,32.42,-109.05,41.89])
        except:
            continue
       
