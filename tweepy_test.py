# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 00:53:38 2017

@author: cck3
"""

import tweepy
import pymongo
import re
import pandas as pd

def text_preprocessing(text):
    '''Simple text preprocessing method for cleansing the data'''
    '''Some Regex references:
    https://stackoverflow.com/questions/24399820/expression-to-remove-url-links-from-twitter-tweet'''
    #Let us analyze everything in lower case
    text = text.lower()
    #Get rid of http
    result = re.sub(r"http\S+", "", text)
    #ignore any person tagging
    result = re.sub(r"@([A-Za-z]+[A-Za-z0-9_]+)", "", result)
    result = re.sub(r"\?", "", result)
    #No need for hashtags
    result = re.sub(r"#", "", result)
    #Remove quotation marks and unnecessary punctuations
    result = re.sub(r'"', "", result)
    result = re.sub(r"'", "", result)
    result = re.sub(r",", "", result)
    result = re.sub(r"-", "", result)
    result = re.sub(r":", "", result)
    result = re.sub(r";", "", result)
    #Remove any brackets
    result = re.sub(r"\(", "", result)
    result = re.sub(r"\)", "", result)
    result = re.sub(r"&", "", result)
    #This call is to reduce all white space to single space and get rid of
    #trailing whitespace using .strip() method
    result = re.sub('\s+', ' ', result).strip()
    #Some twits had these weird units
    result = re.sub(r"£", "", result)
    result = re.sub(r"\.", "", result)
    result = re.sub(r"|", "", result)
    result = re.sub(r"\!", "", result)
    #Remove any price tag
    return result

'''First set up a connection to MongoDB'''
username = 'cck3'
password = 'ck1445CK'
connection = pymongo.MongoClient('mongodb://%s:%s@52.78.226.78' % (username, password))

'''Make a new db called twitter'''
db = connection.twitter

'''Make a new collection called hmm... twitter_collection'''
twitter_collection = db.twitter_collection
twitter_collection_unfiltered = db.twitter_collection_unfiltered

'''Now connect to Twitter Open API using keys and secrets'''
consumer_key = 'WJxqR6SL4JgQW2XwNlVmrCMDi'
consumer_secret = 'Y5OzWd956VjbyCoTeAYqzSoQ5MfSBAjgo95w5u0SQYM35Wx2uQ'

access_token = '946046842919202817-7JuPQBiEE7wIjlkNMwhql6khr2But2r'
access_token_secret = '6hZf8fzXOEwn7QG1eOEq7VCEeIZhCNrB1PAHpjNkn1DtY'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

'''Reference for rate limit: 
    https://stackoverflow.com/questions/21308762/avoid-twitter-api-limitation-with-tweepy'''
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

'''This keyword is used to search tweet. -filter:retweets is there to make 
sure retweets are filtered out'''
key = 'jerusalem -filter:retweets'

count = 1
'''Reference on tweet_mode input: 
https://twittercommunity.com/t/retrieve-full-tweet-when-truncated-non-retweet/75542/4
https://developer.twitter.com/en/docs/tweets/tweet-updates'''

'''Reading the tweet data and saving them in MongoDB'''
for tweet in tweepy.Cursor(api.search, q=key, include_entities=True, lang="en", tweet_mode="extended").items(80000):
    #Keep the original
    tweet_dict_unfiltered = {'original_tweet' : tweet.full_text}
    twitter_collection_unfiltered.insert_one(tweet_dict_unfiltered)
    
    #Insert the filtered tweets
    tweet_mod = text_preprocessing(tweet.full_text)
    tweet_dict = {'filtered_tweet' : tweet_mod}
    twitter_collection.insert_one(tweet_dict)
    
    if count % 1 == 0:
        print(str(count) + ':' + tweet_mod)
        print('-' * 30)
    count += 1
    
'''Problem with using Twitter is that... due to the fact the free account only allows
data from past 7 days, it is diifficult to gather large data in a particular topic. 
Also, the problem with streaming a product data is that there are
way too many ads on twitter to extract anything meaningful

My guess is that there would probably more meaningful reviews from people when a product
is just released. But when I tried Samsung Galaxy S8, which has been out for a while,
most of the tweets (around 4000) consisted largely of advertisements.

Also, non-popular topics like Tesla or Machine Learning did not have much tweets either.

So I finally decided to pick a subject that is hotly debated topic - jerusalem.'''

'''Let us call the saved data in DataFrame and save it as a csv file'''
tweet_list = []
for tweet in twitter_collection.find():
    '''Let us filter out tweets that are too short'''
    if len(tweet['filtered_tweet']) < 40:
        continue
    tweet_list.append(tweet['filtered_tweet'])
    
tweet_df = pd.DataFrame(tweet_list, columns = ['filtered_tweet'])
tweet_df.to_csv('filtered_tweet.csv')