#!/usr/bin/env python
# encoding: utf-8

import tweepy  # https://github.com/tweepy/tweepy
import csv
import json
import sys
import os


class TwitterUtils():
    """
    Utilities to work with Twitter
    """

    def __init__(self, credentialsPath):
        with open(credentialsPath, "r") as data_file:
            data_loaded = json.load(data_file)

        # Twitter API credentials
        self.consumer_key = data_loaded['apiKey']
        self.consumer_secret = data_loaded['apiSecretKey']
        self.access_key = data_loaded['accessToken']
        self.access_secret = data_loaded['accessTokenSecret']

    def get_all_tweets(self, screen_name, outputFormat):
        # Twitter only allows access to a users
        # most recent 3240 tweets with this method
        # authorize twitter, initialize tweepy

        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_key, self.access_secret)
        api = tweepy.API(auth)

        # initialize a list to hold all the tweepy Tweets
        alltweets = []

        # make initial request for most recent tweets
        # (200 is the maximum allowed count)
        new_tweets = api.user_timeline(
            screen_name=screen_name, count=200, tweet_mode='extended')

        # save most recent tweets
        alltweets.extend(new_tweets)

        try:
            # save the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1
        except:
            return False

        # keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            print("getting tweets before %s" % (oldest))

            # all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(
                screen_name=screen_name, count=200,
                tweet_mode='extended', max_id=oldest)

            # save most recent tweets
            alltweets.extend(new_tweets)

            # update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1

            print("...%s tweets downloaded so far" % (len(alltweets)))

        if outputFormat == 'csv':
            # transform the tweepy tweets into a
            # 2D array that will populate the csv
            outtweets = [[tweet.id_str, tweet.created_at,
                          tweet.full_text] for tweet in alltweets]
            # write the csv
            with open('%s_tweets.csv' % screen_name, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(["id", "created_at", "text"])
                writer.writerows(outtweets)

        if outputFormat == 'txt':
            # transform the tweepy tweets into
            # a 2D array that will populate the txt
            outtweets = [[tweet.full_text] for tweet in alltweets]
            # write the txt
            with open('%s_tweets.txt' % screen_name, 'w') as f:
                writer = csv.writer(f)
                # writer.writerow(["text"])
                writer.writerows(outtweets)

        return True


if __name__ == '__main__':
    # 1st param for this script: username
    # 2nd param: the format to save the data, csv or txt typically
    userParam = 1
    outputParam = 2
    if sys.argv[outputParam] == 'txt':
        fileFormat = 'txt'
    else:
        fileFormat = 'csv'

    TwitterUtils('credentials/twitterCredentials.json').get_all_tweets(
        str(sys.argv[userParam]), str(fileFormat))
