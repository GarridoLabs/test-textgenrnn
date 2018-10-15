# -*- coding: utf-8 -*-
'''
    @license

    Copyright(c) 2018, GarridoLabs and the project's contributors.

    This source code is licensed under the Apache License, Version 2.0 found in
    the LICENSE.txt file in the root directory of this source tree.
'''

import csv
import json
import math
import sys
from time import sleep

import tweepy


class TweetsDump:
    def __init__(self, credentials_path):
        with open(credentials_path, "r") as data_file:
            data_loaded = json.load(data_file)

        # Twitter API credentials
        self.consumer_key = data_loaded['apiKey']
        self.consumer_secret = data_loaded['apiSecretKey']
        self.access_key = data_loaded['accessToken']
        self.access_secret = data_loaded['accessTokenSecret']

        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_key, self.access_secret)
        self.api = tweepy.API(auth)

    @staticmethod
    def is_retweet(tweet):
        return tweet["retweeted"]

    @staticmethod
    def get_ids(ids_input_file):
        with open(ids_input_file) as f:
            ids = json.load(f)

        print('total ids: {}'.format(len(ids)))

        return ids

    @staticmethod
    def write_non_retweeted_tweets_plain_text(output_file, tweets):
        with open(output_file, 'w', newline='\n') as csvfile:
            f = csv.writer(csvfile, quoting=csv.QUOTE_NONE)
            for tweet in tweets:
                if not TweetsDump.is_retweet(tweet):
                    f.writerow([tweet["text"]])

    @staticmethod
    def write_tweets_json(output_file, tweets):
        print('creating master json file')
        with open(output_file, 'w') as outfile:
            json.dump(tweets, outfile)

    def retrieve_tweets(self, ids):
        all_tweets = []
        start = 0
        end = 100
        limit = len(ids)
        i = math.ceil(limit / 100)

        for _ in range(i):
            print('currently getting {} - {}'.format(start, end))
            sleep(6)  # needed to prevent hitting API rate limit
            id_batch = ids[start:end]
            start += 100
            end += 100
            tweets = self.api.statuses_lookup(id_batch)
            for tweet in tweets:
                all_tweets.append(dict(tweet._json))

        return all_tweets

    def dump_all_tweets(self, ids_input_file, output_base_name):

        output_base_name = output_base_name.lower()
        output_file = '{}.json'.format(output_base_name)
        output_file_txt = '{}.txt'.format(output_base_name)

        ids = self.get_ids(ids_input_file)
        all_data = self.retrieve_tweets(ids)

        self.write_tweets_json(output_file, all_data)
        self.write_non_retweeted_tweets_plain_text(output_file_txt, all_data)


if __name__ == '__main__':
    tweetsIdsFile = 1
    outputBaseName = 2

    TweetsDump('credentials/twitterCredentials.json').dump_all_tweets(
        sys.argv[tweetsIdsFile],
        sys.argv[outputBaseName])
