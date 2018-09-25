# test-textgenrnn resources

**What is this?** A collection of resources and utilities to help developers to get/transform data to use with the *textgenrnn* code.

**Included in this folder**

  * `twitter_user_dump`: A script to download the last 3240 tweets from the user selected. In this case, the typical command to use the script is: `python twitter_user_dump.py arg1 arg2`. The arguments (arg1, arg2) are:
    * *arg1*: twitter username.
    * *arg2*: the output file to save the tweets collected. This param is optional. The accepted output params are `txt` and `csv` which will save the tweets in a .csv file with the tweet-related fields *id*, *created_at* and the *text* of the tweet. In the case of txt, the script will save the contents of the tweets in a .txt file where each line is the content of a tweet. If this arg is not used used, or used another option, the script will save the tweets retrieved in both formats (csv and txt).

  * `twitter_user_scrape`: A script to download all the tweets from the user in a range of dates. For realise the download we make a scrape of the Twitter web pages searching for the seleted inputs. The typical command to execute the scrip is: `python twitter_user_scrape.py arg1 arg2 arg3`. The arguments (arg1, arg2) are:
    * *arg1*: twitter username.
    * *arg2*: the start date of the search in format yyyyMMdd
    * *arg3*: the end date of the search in format yyyyMMdd