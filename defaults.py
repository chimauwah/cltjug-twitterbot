"""default configs"""

# *********************************************** #
# ******** Default configs for tweet app ******** #
# *********************************************** #

# default sender of twitterbot related email notifications
DEFAULT_EMAIL_SENDER = 'cltjug@gmail.com'

# default email to send twitterbot related notifications
DEFAULT_EMAIL_RECIPIENT = 'cltjug@gmail.com'

# default value for how often to send out a tweet (measured in hours)
DEFAULT_TWEET_FREQUENCY = 4

# default number of consecutive scheduled tweets missed before sending an email
DEFAULT_EMAIL_ALERT_THRESHOLD = 1

# default number of consecutive scheduled tweets missed before sending a text
DEFAULT_TEXT_ALERT_THRESHOLD = 5


# *********************************************** #
# ******** Default configs for scraper app ****** #
# *********************************************** #

# default maximum number of tweets needing to be reviewed before sending an email alert
DEFAULT_MAX_TWEET_REVIEWS_EMAIL_THRESHOLD = '20'

# default maximum number of tweets needing to be reviewed before sending a text alert
DEFAULT_MAX_TWEET_REVIEWS_TEXT_THRESHOLD = '40'