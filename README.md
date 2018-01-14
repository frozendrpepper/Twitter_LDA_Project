![alt text](https://rlhb.lexblogplatformthree.com/wp-content/uploads/sites/111/2016/10/twitter-company-statistics.jpg)
![alt text](https://fm.cnbc.com/applications/cnbc.com/resources/img/editorial/2017/12/06/104883023-4ED3-PL-TRUMP-1-120617.1910x1000.jpg)

# Twitter Topic Modeling Project

The main goal of this project is to crawl Tweets using Twitter's Open API and perform Topic Modeling using Scikit Learn's LDA algorithm

## File Description

*Twitter LDA analysis.ipynb - This jupyter notebook contains the overall analysis including EDA, actual implementation of LDA and discussion/result.

*filtered_tweet.csv - Contains 80,000 Tweets that were collected using the keyword 'jerusalem', excluding any retweets

*tweepy_test.py - This python file is the actual code used the scrape Tweets using Twitter Open API and save the data in MongoDB which is built in AWS EC2 free account server (This code is also included in the Twitter LDA Analysis.ipynb)

## Quick Summary

Since LDA algorithm does NOT provide optimal number of topics, the analysis was analyzed manually. With 80,000 Tweets with keyword 'Jerusalem', the topic was optimally divided at 4 topics (5 topics are pretty acceptable). The criteria used for "optimal solution" is the maximum number of topics without any repeated topics. As one will see in the result, starting with 6 topic divisions, there are some duplicate topics.

## Useful References
* [Tiwtter Open API](https://developer.twitter.com/en/docs/tweets/search/overview)
 -> This link provides general information on Twitter Open API
* [Youtube Tutorial on Topic Modeling](https://www.youtube.com/watch?v=BuMu-bdoVrU)
 -> A good general overview of what Topic Modeling is. The presentation is given at Pycon Texas
* [StackExchange Discussion](https://datascience.stackexchange.com/questions/12281/how-cluster-a-twitter-data-set)
 -> The thread provides a good insight into the noisiness of Twitter data and why KMeans is probably not a good algorithm to utilize
* [Python Machine Learning](https://github.com/rasbt/python-machine-learning-book)
  -> The chapter on Sentimental Analysis has a nice illustration of how to implement LDA analysis 

## Acknowledgments

This project was completed as a part of final Portfolion project for FastCampus Data Sceice School
