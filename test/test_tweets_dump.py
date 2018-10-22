# -*- coding: utf-8 -*-
'''
    @license

    Copyright(c) 2018, GarridoLabs and the project's contributors.

    This source code is licensed under the Apache License, Version 2.0 found in
    the LICENSE.txt file in the root directory of this source tree.
'''

from __future__ import absolute_import

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
from resources.tweets_dump import TweetsDump

"""
Unit Tests
"""

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

output_file = "test_output_file.txt"

tweets = [{"retweeted": True, "text": 'Retweet bla bla'},
          {"retweeted": False, "text": "bla bla, bli bli..."},
          {"retweeted": True, "text": "Retweet bli bli"},
          {"retweeted": False, "text": "ble ble, blo blo..."}]


class TestTwitterUserDump(unittest.TestCase):

    # noinspection PyBroadException
    @classmethod
    def setUpClass(cls):
        import os
        try:
            os.remove(output_file)
        except BaseException:
            print("Non outfile to delete\n")

    def test_is_retweeted_return_correct_value_for_retweet(self):
        tweet = {"retweeted": True}
        self.assertTrue(TweetsDump.is_retweet(tweet))

    def test_is_retweeted_return_correct_value_for_tweet(self):
        tweet = {"retweeted": False}
        self.assertFalse(TweetsDump.is_retweet(tweet))

    def test_get_ids_return_correct_values(self):
        expected = [
            "1043054925020901382",
            "1043020125014642694",
            "1043048036337901568"]
        self.assertListEqual(TweetsDump.get_ids(
            "resources/test_get_ids.json"), expected)

    def test_write_tweets_plain_text_generated_correctly_output_file(self):
        TweetsDump.write_non_retweeted_tweets_plain_text(output_file, tweets)

        with open(output_file, 'r') as test_file:
            lines = test_file.read().splitlines()

        self.assertEqual(len(lines), 2)
        self.assertEqual("bla bla, bli bli...", lines[0])
        self.assertEqual("ble ble, blo blo...", lines[1])

    if __name__ == '__main__':
        unittest.main()
