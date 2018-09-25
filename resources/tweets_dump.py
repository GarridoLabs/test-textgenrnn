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
    # CHANGE THIS TO THE USER YOU WANT
    user = 'hectorabrahammp'

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

    def dump_all_tweets(self, ids_input_file):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_key, self.access_secret)
        api = tweepy.API(auth)

        user = self.user.lower()
        output_file = '{}.json'.format(user)
        output_file_short = '{}_short.json'.format(user)
        compression = zipfile.ZIP_DEFLATED

        with open(ids_input_file) as f:
            ids = json.load(f)

        print('total ids: {}'.format(len(ids)))

        all_data = []
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
                all_data.append(dict(tweet._json))

        print('metadata collection complete')
        print('creating master json file')
        with open(output_file, 'w') as outfile:
            json.dump(all_data, outfile)

        print('creating ziped master json file')
        zf = zipfile.ZipFile('{}.zip'.format(user), mode='w')
        zf.write(output_file, compress_type=compression)
        zf.close()

        results = []

        with open(output_file) as json_data:
            data = json.load(json_data)
            for entry in data:
                t = {
                    "created_at": entry["created_at"],
                    "text": entry["text"],
                    "in_reply_to_screen_name": entry["in_reply_to_screen_name"],
                    "retweet_count": entry["retweet_count"],
                    "favorite_count": entry["favorite_count"],
                    "source": self.get_source(entry),
                    "id_str": entry["id_str"],
                    "is_retweet": self.is_retweet(entry)
                }
                results.append(t)

        print('creating minimized json master file')
        with open(output_file_short, 'w') as outfile:
            json.dump(results, outfile)

        with open(output_file_short) as master_file:
            data = json.load(master_file)
            fields = ["favorite_count", "source", "text", "in_reply_to_screen_name", "is_retweet", "created_at", "retweet_count", "id_str"]
            print('creating CSV version of minimized json master file')
            f = csv.writer(open('{}.csv'.format(user), 'w'))
            f.writerow(fields)
            for x in data:
                f.writerow([x["favorite_count"], x["source"], x["text"], x["in_reply_to_screen_name"], x["is_retweet"], x["created_at"], x["retweet_count"], x["id_str"]])

if __name__ == '__main__':
    tweetsIdsFile = 1

    TweetsDump('/Users/hector/Documents/Develop/Python/test-textgenrnn/resources/credentials/twitterCredentials.json').dump_all_tweets(
        sys.argv[tweetsIdsFile])
