from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from time import sleep
import json
import datetime


class TwitterScrape():

    # edit these three variables
    user = 'marianorajoy'
    start = datetime.datetime(2011, 4, 1)  # year, month, day
    end = datetime.datetime(2018, 9, 22)  # year, month, day

    # only edit these if you're having problems
    delay = 1  # time to wait on each page load before reading the page
    driver = webdriver.Safari()  # options are Chrome() Firefox() Safari()

    # don't mess with this stuff
    twitter_ids_filename = 'all_ids.json'
    days = (end - start).days + 1
    id_selector = '.time a.tweet-timestamp'
    tweet_selector = 'li.js-stream-item'
    user = user.lower()
    ids = []

    def format_day(self, date):
        day = '0' + str(date.day) if len(str(date.day)) == 1 else str(date.day)
        month = '0' + str(date.month) if len(str(date.month)
                                             ) == 1 else str(date.month)
        year = str(date.year)
        return '-'.join([year, month, day])

    def form_url(self, since, until):
        p1 = 'https://twitter.com/search?f=tweets&vertical=default&q=from%3A'
        p2 = self.user + '%20since%3A' + since + '%20until%3A' + \
            until + 'include%3Aretweets&src=typd'
        return p1 + p2

    def increment_day(self, date, i):
        return date + datetime.timedelta(days=i)

    def scrape(self):
        for day in range(self.days):
            d1 = self.format_day(self.increment_day(self.start, 0))
            d2 = self.format_day(self.increment_day(self.start, 1))
            url = self.form_url(d1, d2)
            print(url)
            print(d1)
            self.driver.get(url)
            sleep(self.delay)

            try:
                found_tweets = self.driver.find_elements_by_css_selector(
                    self.tweet_selector)
                increment = 10

                while len(found_tweets) >= increment:
                    print('scrolling down to load more tweets')
                    self.driver.execute_script(
                        'window.scrollTo(0, document.body.scrollHeight);')
                    sleep(self.delay)
                    found_tweets = self.driver.find_elements_by_css_selector(
                        self.tweet_selector)
                    increment += 10

                print('{} tweets found, {} total'.format(
                    len(found_tweets), len(self.ids)))

                for tweet in found_tweets:
                    try:
                        id = tweet.find_element_by_css_selector(
                            self.id_selector).get_attribute('href').split('/')[-1]
                        self.ids.append(id)
                    except StaleElementReferenceException as e:
                        print('lost element reference', tweet)

            except NoSuchElementException:
                print('no tweets on this day')

            self.start = self.increment_day(self.start, 1)

        try:
            with open(self.twitter_ids_filename) as f:
                all_ids = self.ids + json.load(f)
                data_to_write = list(set(all_ids))
                print('tweets found on this scrape: ', len(self.ids))
                print('total tweet count: ', len(data_to_write))
        except FileNotFoundError:
            with open(self.twitter_ids_filename, 'w') as f:
                all_ids = self.ids
                data_to_write = list(set(all_ids))
                print('tweets found on this scrape: ', len(self.ids))
                print('total tweet count: ', len(data_to_write))

        with open(self.twitter_ids_filename, 'w') as outfile:
            json.dump(data_to_write, outfile)

        print('all done here')
        self.driver.close()


if __name__ == '__main__':
    TwitterScrape().scrape()
