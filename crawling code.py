# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 11:29:10 2020

@author: Daisy
"""

# import
from __future__ import print_function
import tweepy
import json
from pymongo import MongoClient
from tweepy import OAuthHandler


MONGO_HOST = 'mongodb://localhost:27017/Spyder'  # mongodb host path
FILE_NAME = ["excitement_tweet2.json","happy_tweet1.json","pleasant_tweet1.json","sad_tweet1.json","fear_tweet1.json","angry_tweet1.json"]  # file name to save
emotions=[["#excitement","#excited","#astonished"],["#happy","#joy","#love"],["#pleasant","#delighted","#glad","#pleased"],["down","#sad","#frustration","#depressed","#gloomy"],["#fear","#disgust","#depression"],["#angry","#annoyed"]]
# get key from twitter developer
consumer_key = 'SoOHCASEdu1zb4LuWdVslYNM1'
consumer_secret = '88l6hxqA1QJGPx067705ncoPlx7YcLa7p65oscYrhtPQ0kMNY8'
access_token = '1230590123705819136-z0lgV7Zae5k0EvoROpypCHPEo3abOJ'
access_secret = '51rgD4an0Qc64dh4kmTCAttT2K8WIeLinxgTDr5m67DH0'


auth = OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)

api = tweepy.API(auth)

for tweet in tweepy.Cursor(api.search,q = emotions[0][0] or emotions[0][1] or emotions[0][2],tweet_mode='extended').items(160):
    if 'RT @' not in tweet.full_text:#drop the retweets to remove duplicates
                                           try:
                                               with open(FILE_NAME[0], 'a',encoding='utf-8') as ab:
                                                   ab.writelines("Tweet text is: "+tweet.full_text+"\n")

                                                   client = MongoClient(MONGO_HOST)  # connect mongodb
                                                   db = client.excitement_database  # create db
                                                   data_json = json.loads(tweet.full_text)  # Decode the JSON from Twitter
                                                   
                                                   '''
                                                   created_at = data_json['created_at']
                                                   print("Tweet collected time is  " + str(created_at))
                                                   '''   
                                                   db.excitement_collection.insert(data_json) 
                                           except Exception as e:
                                               print(e)
                                               
for tweet in tweepy.Cursor(api.search,q = emotions[1][0] or emotions[1][1] or emotions[1][2],tweet_mode='extended' ).items(160):
    if 'RT @' not in tweet.full_text:#drop the retweets to remove duplicates
                                           try:
                                               with open(FILE_NAME[1], 'a',encoding='utf-8') as ac:
                                                   ac.writelines("Tweet text is: "+tweet.full_text+"\n")

                                                   client = MongoClient(MONGO_HOST)  # connect mongodb
                                                   db = client.happy_database  # create db
                                                   data_json = json.loads(tweet.full_text)  # Decode the JSON from Twitter
                                                   
                                                   '''
                                                   created_at = data_json['created_at']
                                                   print("Tweet collected time is  " + str(created_at))
                                                   '''   
                                                   db.happy_collection.insert(data_json) 
                                           except Exception as e:
                                               print(e)

for tweet in tweepy.Cursor(api.search,q = emotions[2][0] or emotions[2][1] or emotions[2][2],tweet_mode='extended').items(160):
    if 'RT @' not in tweet.full_text:#drop the retweets to remove duplicates
                                           try:
                                               with open(FILE_NAME[2], 'a',encoding='utf-8') as ad:
                                                   ad.writelines("Tweet text is: "+tweet.full_text+"\n")

                                                   client = MongoClient(MONGO_HOST)  # connect mongodb
                                                   db = client.pleasant_database  # create db
                                                   data_json = json.loads(tweet.full_text)  # Decode the JSON from Twitter
                                                   
                                                   '''
                                                   created_at = data_json['created_at']
                                                   print("Tweet collected time is  " + str(created_at))
                                                   '''   
                                                   db.pleasant_collection.insert(data_json) 
                                           except Exception as e:
                                               print(e)

for tweet in tweepy.Cursor(api.search,q = emotions[3][0] or emotions[3][1] or emotions[3][2],tweet_mode='extended').items(160):
    if 'RT @' not in tweet.full_text:#drop the retweets to remove duplicates
                                           try:
                                               with open(FILE_NAME[3], 'a',encoding='utf-8') as ae:
                                                   ae.writelines("Tweet text is: "+tweet.full_text+"\n")

                                                   client = MongoClient(MONGO_HOST)  # connect mongodb
                                                   db = client.sad_database  # create db
                                                   data_json = json.loads(tweet.full_text)  # Decode the JSON from Twitter
                                                   
                                                   '''
                                                   created_at = data_json['created_at']
                                                   print("Tweet collected time is  " + str(created_at))
                                                   '''   
                                                   db.sad_collection.insert(data_json) 
                                           except Exception as e:
                                               print(e)

for tweet in tweepy.Cursor(api.search,q = emotions[4][0] or emotions[4][1] or emotions[4][2],tweet_mode='extended').items(160):
    if 'RT @' not in tweet.full_text:#drop the retweets to remove duplicates
                                           try:
                                               with open(FILE_NAME[4], 'a',encoding='utf-8') as af:
                                                   af.writelines("Tweet text is: "+tweet.full_text+"\n")

                                                   client = MongoClient(MONGO_HOST)  # connect mongodb
                                                   db = client.fear_database  # create db
                                                   data_json = json.loads(tweet.full_text)  # Decode the JSON from Twitter
                                                   
                                                   '''
                                                   created_at = data_json['created_at']
                                                   print("Tweet collected time is  " + str(created_at))
                                                   '''   
                                                   db.fear_collection.insert(data_json) 
                                           except Exception as e:
                                               print(e)

for tweet in tweepy.Cursor(api.search,q = emotions[5][0] or emotions[5][1] or emotions[5][2],tweet_mode='extended').items(160):
    if 'RT @' not in tweet.full_text:#drop the retweets to remove duplicates
                                           try:
                                               with open(FILE_NAME[5], 'a',encoding='utf-8') as ag:
                                                   ag.writelines("Tweet text is: "+tweet.full_text+"\n")

                                                   client = MongoClient(MONGO_HOST)  # connect mongodb
                                                   db = client.angry_database  # create db
                                                   data_json = json.loads(tweet.full_text)  # Decode the JSON from Twitter
                                                   
                                                   '''
                                                   created_at = data_json['created_at']
                                                   print("Tweet collected time is  " + str(created_at))
                                                   '''   
                                                   db.angry_collection.insert(data_json) 
                                           except Exception as e:
                                               print(e)