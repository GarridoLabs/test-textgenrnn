# -*- coding: utf-8 -*-
from __future__ import absolute_import
'''
    @license

    Copyright(c) 2018, GarridoLabs and the project's contributors.

    This source code is licensed under the Apache License, Version 2.0 found in
    the LICENSE.txt file in the root directory of this source tree.
'''

"""
Unit Tests
"""
from time import gmtime, strftime
import os
import sys
import unittest
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
from resources.twitter_user_dump import TwitterUtils
from test_config import skip_integration_test
import tweepy
import time


@unittest.skipIf(skip_integration_test is True, "integration test")
class IntegrationTestTwitterUserDump(unittest.TestCase):
    """
    Class with the unit tests related to integration
    """

    # Method to test get tweets from users
    def test_twitter_user_dump(self):

        # Test get tweets from @garridoLabs
        # Currently that account has 0 tweets, so it must return False
        self.assertFalse(
            TwitterUtils(
                '../resources/credentials/twitterCredentials.json')
            .get_all_tweets('garridoLabs', 'csv'))

    # Method to test get tweets from users
    def test_twitter_bad_user_dump(self):

        # Test get tweets from a random user which should not exist
        # It must return False
        self.assertFalse(
            TwitterUtils(
                '../resources/credentials/twitterCredentials.json')
            .get_all_tweets("userfake-" + str(time.time()), 'csv'))


class TestTwitterUserDump(unittest.TestCase):
    """
    Class with the unit tests unrelated to integration
    """

    def test_errors_twitter_credentials_user_dump(self):

        # Test get tweets from user

        # Test error if we don't provide the path for Twitter credentials
        self.assertRaises(TypeError, lambda:
                          TwitterUtils()  # pylint: disable=E1120
                          .get_all_tweets('', ''))

        # Test error if we provide a fake path for Twitter credentials
        self.assertRaises(
            FileNotFoundError, lambda:
            TwitterUtils(
                './fakePath.json')
            .get_all_tweets('', ''))

        # Test error if we provide bad Twitter credentials
        self.assertRaises(
            tweepy.error.TweepError, lambda:
            TwitterUtils(
                'resources/exampleTwitterCredentials.json')
            .get_all_tweets('', ''))

    if __name__ == '__main__':
        unittest.main()
