from scraper import *
from tweeter import *
from apscheduler.schedulers.background import BackgroundScheduler

def main():

    # == == == == == == == == == #
    # Initiate tweetbot-scraper  #
    # == == == == == == == == == #
    # == == == == == == == == == #

    streamlistener = MyStreamListener()

    myfilter = create_filter_string_from_file('filters.txt')
    init_twitter_stream(streamlistener, myfilter)

    print('CLTJUG TwitterScraper initialized and executing')
    print('When a status is found that matches filter, it is immediately added to a database for review. If the count '
          'of items to review reaches the configured threshold, an alert will be sent.\n')

    # == == == == == == == == == #
    # Initiate tweetbot-tweeter  #
    # == == == == == == == == == #
    # == == == == == == == == == #

    instance = TweetBotApp()

    # get from config db how often this should run
    frequency = get_config_value(TWEET_FREQUENCY, DEFAULT_TWEET_FREQUENCY)

    # set job id in order to reference it if we need to modify job while it is running
    job_id = 'job-id-07212017'
    instance.tweet_job_id = job_id

    s = BackgroundScheduler()
    s.add_job(lambda: execute(instance), 'interval', hours=frequency, id=job_id)
    print('CLTJUG TweetBot initialized and executing')
    cadence = 'hours'
    if frequency == 1:
        cadence = 'hour'
    print('Tweeting every {} {}'.format(frequency, cadence))
    s.start()


if __name__ == '__main__':
    main()
