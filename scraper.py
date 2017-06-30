""" This app finds tweets from twitter using filters and sends them to be reviewed """

from apscheduler.schedulers.background import BackgroundScheduler
from functions import *


class TweetHolder:
    """ class to that holds and manages fetched tweets """

    # array containing tweets
    __tweets = []

    def addtweet(self, tweet):
        self.__tweets.append(tweet)

    def gettweets(self):
        return self.__tweets

    def getsize(self):
        return len(self.__tweets)

    def flush(self):
        self.__tweets = []


class MyStreamListener(tweepy.StreamListener):
    """creates an API to stream that contains a tweet holder instance"""

    __tweetholder = TweetHolder()

    def get_tweetholder(self):
        return self.__tweetholder

    def on_status(self, status):
        """when a new status arrives, the on_data method of StreamListener passes data from statusess to this method

        :param status:
        :return:
        """
        self.__tweetholder.addtweet(status)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False if on_error disconnects the stream
            return False
        print('Unhandled error in twitter stream: {0}'.format(status_code))


def email_job(tweet_holder):
    """if there is at least 1 tweet in tweetholder collection, send an email containing the collection of tweets out
    for review, and clear out the tweet holder collection

    :param tweet_holder:
    :return:
    """
    if tweet_holder.getsize() > 0:
        email = build_email()
        email['msg'] = create_collections_of_tweets_for_email(tweet_holder.gettweets())
        email['subj'] = 'TWITTERBOT ALERT: New tweets to review'
        send_email(email)
        tweet_holder.flush()
    else:
        print('No tweets found using filters in this last interval. No email to send.')


def init_twitter_stream(mystreamlistener, myfilter):
    """ open and keep open a connection to the Twitter Streaming API

    :param mystreamlistener:
    :param myfilter:
    :return:
    """
    mystream = tweepy.Stream(auth=twitter.auth, listener=mystreamlistener)
    mystream.filter(track=[myfilter], stall_warnings='true', languages=['en'], async=True)


def main():
    """ entry point of application that kicks of twitter scraper

    :return:
    """
    streamlistener = MyStreamListener()

    myfilter = create_filter_string_from_file('filters.txt')
    init_twitter_stream(streamlistener, myfilter)

    # get from config db how often this should run
    interval = get_config_value(EMAIL_INTERVAL, DEFAULT_EMAIL_INTERVAL)

    # create scheduler to send an email with all the tweets in tweet holder for configured interval
    s = BackgroundScheduler()
    s.add_job(lambda: email_job(streamlistener.get_tweetholder()), 'interval', minutes=15)
    print('CLTJUG TwitterScraper initialized and executing')
    cadence = 'minutes'
    if interval == 1:
        cadence = 'minute'
    print('Emailing every {} {}'.format(interval, cadence))
    s.start()


if __name__ == '__main__':
    main()
