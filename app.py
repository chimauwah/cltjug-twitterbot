""" This class pulls tweets from database and tweets them at scheduled frequency """

from apscheduler.schedulers.blocking import BlockingScheduler
from functions import *
from utility import *


class TweetBotApp:
    """instance of this tweet bot application"""

    tweet_job_id = ''

    consecutive_no_tweet_cnt = 0
    send_text = True

    def reset_consecutive_no_tweet_cnt(self):
        self.consecutive_no_tweet_cnt = 0
        self.send_text = True


def get_next_tweet(coll):
    """ retrieve from given collection next message that has not already been tweeted or had an error

    :param coll:
    :return:
    """
    document = coll.find_one({'dateTweeted': None, 'dateErred': None})
    return document


def mark_as_tweeted(coll, m_id):
    coll.find_one_and_update({'_id': m_id}, {'$currentDate': {'dateTweeted': True}})


def mark_as_erred(coll, m_id, errmsg):
    coll.find_one_and_update({'_id': m_id}, {'$currentDate': {'dateErred': True}, '$set': {'errMsg': errmsg}})


def execute(instance):
    """ execute twitter bot by tweeting out next available msg. If we find a msg, reset the number of times we did not
    send out a tweet to 0 (if necessary), then attempt to send out tweet. If successful, update that tweet as tweeted,
    if not successful, mark that tweet as erred. If no message found, increase number of times we did not send out a
    tweet by 1, and send alerts that we are out of messages to tweet

    :param instance:
    :return:
    """
    coll = DBConnection().get_tweet_collection()
    document = get_next_tweet(coll)
    if document is not None:
        if instance.consecutive_no_tweet_cnt != 0:
            instance.reset_consecutive_no_tweet_cnt()
        resp = send_tweet(twitter, tweepy, document['msg'])
        if resp['success']:
            mark_as_tweeted(coll, document['_id'])
        else:
            mark_as_erred(coll, document['_id'], resp['errMsg'])

    else:
        instance.consecutive_no_tweet_cnt += 1
        print('OUT OF TWEETS!! ' + str(instance.consecutive_no_tweet_cnt))
        email_threshold = get_config_value(EMAIL_ALERT_THRESHOLD, DEFAULT_EMAIL_ALERT_THRESHOLD)
        txt_threshold = get_config_value(TEXT_ALERT_THRESHOLD, DEFAULT_TEXT_ALERT_THRESHOLD)
        if instance.consecutive_no_tweet_cnt >= email_threshold:
            subj = 'TWITTERBOT ALERT: Out of tweets - Notice {}'.format(str(instance.consecutive_no_tweet_cnt))
            msg = 'There are no more messages to tweet. Please add more messages.'
            if (instance.consecutive_no_tweet_cnt >= txt_threshold) and instance.send_text:
                send_text_message(subj + ': ' + msg)
                instance.send_text = False  # only send text 1 time for every instance out of tweets
            email = build_email()
            email['subj'] = subj
            email['msg'] = msg
            send_email(email)


def main():
    """ entry point of application that kicks of tweet scheduler

    :return:
    """
    instance = TweetBotApp()

    # get from config db how often this should run
    frequency = get_config_value(TWEET_FREQUENCY, DEFAULT_TWEET_FREQUENCY)

    # set job id in order to reference it if we need to modify job while it is running
    job_id = 'tweet_job_id'
    instance.tweet_job_id = job_id

    s = BlockingScheduler()
    s.add_job(lambda: execute(instance), 'interval', hours=frequency, id=job_id)
    print('CLTJUG TweetBot initialized and executing')
    cadence = 'hours'
    if frequency == 1:
        cadence = 'hour'
    print('Tweeting every {} {}'.format(frequency, cadence))
    s.start()


if __name__ == '__main__':
    main()
