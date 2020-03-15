# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 21:44:13 2020

@author: Daisy
"""

from __future__ import print_function
import tweepy
import json
from pymongo import MongoClient
from tweepy import OAuthHandler
import csv

MONGO_HOST = 'mongodb://localhost:27017/Spyder'  # mongodb host path
FILE_NAME = ["excitement_tweet2.json","happy_tweet1.json","pleasant_tweet1.json","sad_tweet1.json","fear_tweet1.json","angry_tweet1.json"]  # file name to save
emotions=["#excitement","#excited","#astonished","#happy","#joy","#love","#pleasant","#delighted","#glad","#pleased","#down","#sad","#frustration","#depressed","#gloomy","#fear","#disgust","#depression","#angry","#anger","#annoyed"]
# get key from twitter developer
consumer_key = 
consumer_secret = 
access_token = 
access_secret = 


auth = OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)

api = tweepy.API(auth)
with open("tweets2.csv", 'w',encoding='utf-8',newline='' "") as ab:
    csv_writer = csv.writer(ab)
    csv_writer.writerow(["user_ID","tweet","creation time"])
    ab.close

        
for i in range(0,21):
    track = str(emotions[i])+"-filter:retweets" #omit the retweets to remove duplicates
    for tweet in tweepy.Cursor(api.search,q = track,lang = "en", tweet_mode='extended',include_rts = False).items(110):
        try:
            with open("tweets2.csv", 'a',encoding='utf-8',newline='' "") as ab:
                    csv_writer = csv.writer(ab)
                    csv_writer.writerow([tweet.user.id,tweet.full_text,tweet.created_at])

                    client = MongoClient(MONGO_HOST)  # connect mongodb
                    db = client.newtweet_database  # create db
                    data_json = json.loads(tweet.full_text)  # Decode the JSON from Twitter
                                                   
                       
                    db.newtweet_collection.insert(data_json) 
            ab.close()
        except Exception as e:
            print(e) 
           