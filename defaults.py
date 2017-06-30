"""default configs"""

""" ******** Default configs for scraper app ******** """
# default interval (in hours) for send email with tweets to review
DEFAULT_EMAIL_INTERVAL = 8

DEFAULT_FILTER_STRING = '@burrsutter,#javaee,@stackjava,#javacodegeeks,@java,#javaee,@java_ee,@habuma,#NFJS,@nofluff,' \
                        '@springcentral,@neal4d,@kenkousen,@venkat_s,@overopshq,@SoftwareTopNews '

""" ******** Default configs for tweet app ******** """
# default interval to send out tweets (measured in hours)
DEFAULT_TWEET_FREQUENCY = 4

# default number of consecutive scheduled tweets not sent before sending an email
DEFAULT_EMAIL_ALERT_THRESHOLD = 1

# default number of consecutive scheduled tweets not sent before sending a text
DEFAULT_TEXT_ALERT_THRESHOLD = 5

# default email to send twitterbot related notifications
DEFAULT_EMAIL_RECIPIENT = 'cltjug@gmail.com'

# default sender of twitterbot related email notifications
DEFAULT_EMAIL_SENDER = 'cltjug@gmail.com'

EMAIL_FOOTER_LINE_1 = "   ___ _  _____   _ _   _  ___   _____        _ _   _           ___      _   "
EMAIL_FOOTER_LINE_2 = "  / __| ||_   _| | | | | |/ __| |_   _|_ __ _(_) |_| |_ ___ _ _| _ ) ___| |_ "
EMAIL_FOOTER_LINE_3 = " | (__| |__| || || | |_| | (_ |   | | \ V  V / |  _|  _/ -_) '_| _ \/ _ \  _|"
EMAIL_FOOTER_LINE_4 = "  \___|____|_| \__/ \___/ \___|   |_|  \_/\_/|_|\__|\__\___|_| |___/\___/\__|"
EMAIL_FOOTER_LINE_5 = "                                                                             "

EMAIL_FOOTER_LINE_2_0 = "   ____ _   _____   _ _   _  ____   _____          _ _   _            ____        _   "
EMAIL_FOOTER_LINE_2_1 = "  / ___| | |_   _| | | | | |/ ___| |_   _|_      _(_) |_| |_ ___ _ __| __ )  ___ | |_ "
EMAIL_FOOTER_LINE_2_2 = " | |   | |   | |_  | | | | | |  _    | | \ \ /\ / / | __| __/ _ \ '__|  _ \ / _ \| __|"
EMAIL_FOOTER_LINE_2_3 = " | |___| |___| | |_| | |_| | |_| |   | |  \ V  V /| | |_| ||  __/ |  | |_) | (_) | |_ "
EMAIL_FOOTER_LINE_2_4 = "  \____|_____|_|\___/ \___/ \____|   |_|   \_/\_/ |_|\__|\__\___|_|  |____/ \___/ \__|"


