import tweepy
import json
import math
import glob
import csv
import zipfile
import zlib
import sys
from tweepy import TweepError
from time import sleep


class TweetsDump():
    def __init__(self, credentialsPath):
        with open(credentialsPath, "r") as data_file:
            data_loaded = json.load(data_file)

        # Twitter API credentials
        self.consumer_key = data_loaded['apiKey']
        self.consumer_secret = data_loaded['apiSecretKey']
        self.access_key = data_loaded['accessToken']
        self.access_secret = data_loaded['accessTokenSecret']

    def is_retweet(self, entry):
        return 'retweeted_status' in entry.keys()

    def get_source(self, entry):
        if '<' in entry["source"]:
            return entry["source"].split('>')[1].split('<')[0]
        else:
            return entry["source"]

    def get_ids(self, ids_input_file):
        with open(ids_input_file) as f:
            ids = json.load(f)

        print('total ids: {}'.format(len(ids)))

        return ids

    def retrieve_tweets(self, api, ids):
        all_tweets = []
        start = 0
        end = 100
        limit = len(ids)
        i = math.ceil(limit / 100)

        for go in range(i):
            print('currently getting {} - {}'.format(start, end))
            sleep(6)  # needed to prevent hitting API rate limit
            id_batch = ids[start:end]
            start += 100
            end += 100
            tweets = api.statuses_lookup(id_batch)
            for tweet in tweets:
                all_tweets.append(dict(tweet._json))

        print('metadata collection complete')
        return all_tweets

    def write_tweets_json(self, output_file, tweets):
        print('creating master json file')
        with open(output_file, 'w') as outfile:
            json.dump(tweets, outfile)

    def write_tweets_plain_text(self, output_file, tweets):
        f = csv.writer(open(output_file, 'w'))
        outtweets = []
        for tweet in tweets:
            if not tweet["retweeted"]:
                f.writerow([tweet["text"]])

    def dump_all_tweets(self, ids_input_file, output_base_name):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_key, self.access_secret)
        api = tweepy.API(auth)

        output_base_name = output_base_name.lower()
        output_file = '{}.json'.format(output_base_name)
        output_file_txt = '{}.txt'.format(output_base_name)

        ids = self.get_ids(ids_input_file)
        all_data = self.retrieve_tweets(api, ids)

        self.write_tweets_json(output_file, all_data)
        self.write_tweets_plain_text(output_file_txt, all_data)


if __name__ == '__main__':
    tweetsIdsFile = 1
    outputBaseName = 2

    TweetsDump('credentials/twitterCredentials.json').dump_all_tweets(
        sys.argv[tweetsIdsFile],
        sys.argv[outputBaseName])
