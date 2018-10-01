import datetime
import json
import sys
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


class TwitterScrape:
    TWITTER_IDS_FILES_SUBFIX = "_ids.json"
    ID_SELECTOR = '.time a.tweet-timestamp'
    TWEET_SELECTOR = 'li.js-stream-item'
    TWEETS_PER_PAGE = 10
    DEFAULT_DELAY_IN_SECONDS = 1

    def twitter_ids_filename(self, user: str):
        return user + self.TWITTER_IDS_FILES_SUBFIX

    def format_day(self, date):
        day = '0' + str(date.day) if len(str(date.day)) == 1 else str(date.day)
        month = '0' + str(date.month) if len(str(date.month)
                                             ) == 1 else str(date.month)
        year = str(date.year)
        return '-'.join([year, month, day])

    def form_url(self, user, since, until):
        p1 = 'https://twitter.com/search?f=tweets&vertical=default&q=from%3A'
        p2 = user + '%20since%3A' + self.format_day(since) + '%20until%3A' + \
            self.format_day(until) + 'include%3Aretweets&src=typd'
        return p1 + p2

    def increment_day(self, date, number_of_increments_in_days=1):
        return date + datetime.timedelta(days=number_of_increments_in_days)

    def find_all_tweets_on_actual_page(
            self, driver, delay, tweets_per_page=TWEETS_PER_PAGE):
        found_tweets = driver.find_elements_by_css_selector(
            self.TWEET_SELECTOR)

        number_loads = 1

        while len(found_tweets) >= tweets_per_page * number_loads:
            print('scrolling down to load more tweets')
            number_loads += 1
            driver.execute_script(
                'window.scrollTo(0, document.body.scrollHeight);')
            sleep(delay)
            found_tweets = driver.find_elements_by_css_selector(
                self.TWEET_SELECTOR)

        return found_tweets

    def extract_tweets_ids(self, found_tweets_html_elements):
        ids = []
        for tweet in found_tweets_html_elements:
            try:
                id = tweet.find_element_by_css_selector(
                    self.ID_SELECTOR).get_attribute('href').split('/')[-1]
                ids.append(id)
            except StaleElementReferenceException:
                print('lost element reference', tweet)

        return ids

    def write_found_tweets(
            self, user, ids, merge_with_previous_ids_in_same_file=True):
        if merge_with_previous_ids_in_same_file:
            try:
                with open(self.twitter_ids_filename(user)) \
                        as user_tweet_ids_file:
                    ids = list(set(ids + json.load(user_tweet_ids_file)))
            except FileNotFoundError:
                print('Warning: no previous file found to merge')

        print('tweets found on this scrape: ', len(ids))
        print('total tweet count: ', len(ids))

        with open(self.twitter_ids_filename(user), 'w') as outfile:
            json.dump(ids, outfile)

    def get_url(self, driver, url, delay):
        print(url)
        driver.get(url)
        sleep(delay)

    def scrape(self, user, start_date, end_date,
               delay=DEFAULT_DELAY_IN_SECONDS):
        driver = webdriver.Safari()  # options are Chrome() Firefox() Safari()
        user = user.lower()
        days = (end_date - start_date).days + 1
        ids = []
        for _ in range(days):
            self.get_url(driver,
                         self.form_url(user, start_date,
                                       self.increment_day(start_date)),
                         delay)

            try:
                found_tweets = self.find_all_tweets_on_actual_page(
                    driver, delay)
                ids = ids + self.extract_tweets_ids(found_tweets)
                print('{} tweets found, {} total'.format(
                    len(found_tweets), len(ids)))

            except NoSuchElementException:
                print('no tweets on this day')

            start_date = self.increment_day(start_date)

        self.write_found_tweets(user, ids)

        print('all done here')
        driver.close()


if __name__ == '__main__':
    twitterUserParam = 1
    startDateParam = 2
    endDateParam = 3

    def parse_date(date):
        return datetime.datetime.strptime(date, '%Y%m%d')

    TwitterScrape().scrape(
        sys.argv[twitterUserParam],
        parse_date(sys.argv[startDateParam]),
        parse_date(sys.argv[endDateParam])
    )
