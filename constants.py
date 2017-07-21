""" file containing all used constants"""

# *********************************************** #
# *********** Constants for tweet app *********** #
# *********************************************** #

# sender of twitterbot related email alerts
EMAIL_SENDER = 'EMAIL_SENDER'

# email to send twitterbot related alerts
EMAIL_RECIPIENT = 'EMAIL_RECIPIENT'

# how often to send out a tweet (measured in hours)
TWEET_FREQUENCY = 'TWEET_FREQUENCY'

# number of consecutive scheduled tweets missed before sending an email
EMAIL_ALERT_THRESHOLD = 'EMAIL_ALERT_THRESHOLD'

# number of consecutive scheduled tweets missed before sending a text
TEXT_ALERT_THRESHOLD = 'TEXT_ALERT_THRESHOLD'

# timestamp for last time an email alert was sent
LAST_EMAIL_ALERT_TSTAMP = 'LAST_EMAIL_ALERT_TSTAMP'

# timestamp for last time a text alert was sent
LAST_TEXT_ALERT_TSTAMP = 'LAST_TEXT_ALERT_TSTAMP'


# *********************************************** #
# *********** Constants for scraper app ********* #
# *********************************************** #

# maximum number of tweets needing to be reviewed before sending an email alert
MAX_TWEET_REVIEWS_EMAIL_THRESHOLD = 'MAX_TWEET_REVIEWS_EMAIL_THRESHOLD'

# maximum number of tweets needing to be reviewed before sending a text alert
MAX_TWEET_REVIEWS_TEXT_THRESHOLD = 'MAX_TWEET_REVIEWS_TEXT_THRESHOLD'

