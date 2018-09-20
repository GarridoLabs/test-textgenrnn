# -*- coding: utf-8 -*-
from __future__ import absolute_import
'''
    @license

    Copyright(c) 2018, IBM.

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


class TestTwitterUserDump(unittest.TestCase):
    """
    Class with the unit tests
    """

    # Method to test get tweets from users
    def test_twitter_user_dump(self):

        # Test get tweets from @garridoLabs
        # Currently that account has 0 tweets, so it must return False
        self.assertFalse(
            TwitterUtils(
                '../resources/credentials/twitterCredentials.json')
            .get_all_tweets('garridoLabs', 'csv'))

    if __name__ == '__main__':
        unittest.main()
