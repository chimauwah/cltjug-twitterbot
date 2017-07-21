""" This app finds tweets from twitter using filters and adds them to a database to be reviewed """

from functions import *


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        """when a new status arrives, the on_data method of StreamListener passes data from statusess to this method

        :param status:
        :return:
        """
        send_for_review(status)
        handlealerts()

    def on_error(self, status_code):
        if status_code == 420:
            # returning False if on_error disconnects the stream
            return False
        print('Unhandled error in twitter stream: {0}'.format(status_code))


def handlealerts():
    """check number of tweets to be reviewed. if greater than configurable amount, send alert

    """
    db = DBConnection()

    cnt = db.get_tweet_review().count()

    configs = db.get_configs()
    lastemailtstamp = configs.distinct(LAST_EMAIL_ALERT_TSTAMP)[0]
    lasttexttstamp = configs.distinct(LAST_TEXT_ALERT_TSTAMP)[0]

    msg = 'There are ' + str(cnt) + ' tweets to review. Please go to twitter bot management console to approve.'
    subj = 'TWITTERBOT ALERT: Review tweets'

    if cnt > get_config_value(MAX_TWEET_REVIEWS_EMAIL_THRESHOLD,
                              DEFAULT_MAX_TWEET_REVIEWS_EMAIL_THRESHOLD) and alertallowed(lastemailtstamp, 'email'):
        email = build_email()
        email['msg'] = msg
        email['subj'] = subj
        send_email(email)
        # update last email alert timestamp
        configs.find_one_and_update({}, {'$set': {'LAST_EMAIL_ALERT_TSTAMP': datetime.utcnow()}})
    if cnt > get_config_value(MAX_TWEET_REVIEWS_TEXT_THRESHOLD,
                              DEFAULT_MAX_TWEET_REVIEWS_TEXT_THRESHOLD) and alertallowed(lasttexttstamp, 'text'):
        send_text_message(subj + ': ' + msg)
        # update last text alert timestamp
        configs.find_one_and_update({}, {'$set': {'LAST_TEXT_ALERT_TSTAMP': datetime.utcnow()}})


def alertallowed(tstamp, option):
    """returns true if tstamp is None (meaning no alert has been sent) or if time between last alert is greater than
    threshold. Return false if it is less than

    :param option:
    :param tstamp:
    :return:
    """
    threshold = 86400  # seconds
    if option == 'email':
        threshold = 43200

    if tstamp is None:
        return True
    difference = datetime.utcnow() - tstamp
    if difference.total_seconds() > threshold:
        return True
    else:
        return False


def send_for_review(status):
    """takes given status and saves in tweet review collection in db

    :param status:
    :return:
    """
    db = DBConnection()
    coll = db.get_tweet_review()
    document = {
        'twitterid': status.id_str,
        'tweeturl': build_tweet_url(status),
        'status': 'PENDING'
    }
    coll.insert_one(document)


def init_twitter_stream(mystreamlistener, myfilter):
    """ open and keep open a connection to the Twitter Streaming API

    :param mystreamlistener:
    :param myfilter:
    :return:
    """
    mystream = tweepy.Stream(auth=twitter.auth, listener=mystreamlistener)
    mystream.filter(track=[myfilter], stall_warnings='true', languages=['en'], async=True)


# def main():
#     """ entry point of application that kicks of twitter scraper
#
#     :return:
#     """
#     streamlistener = MyStreamListener()
#
#     myfilter = create_filter_string_from_file('filters.txt')
#     init_twitter_stream(streamlistener, myfilter)
#
#     print('CLTJUG TwitterScraper initialized and executing')
#     print('When a status is found that matches filter, it is immediately added to a database for review. If the count '
#           'of items to review reaches the configured threshold, an alert will be sent.\n')
#
#
# if __name__ == '__main__':
#     main()
