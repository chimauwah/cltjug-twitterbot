import argparse
import httplib2
import base64
from apiclient import discovery
from oauth2client import client
from oauth2client.file import Storage
from oauth2client import tools
from email.mime.text import MIMEText
from datetime import datetime
from twilio.rest import Client
from twilio_properties import *

# Import our custom defined constants from defaults.py
from defaults import *

# Access and authorize Twilio account
twilio = Client(acct_sid, auth_token)


# send text message
def send_text_message(txt):
    twilio.messages.create(to=to_number, from_=from_number, body=txt)


def get_commandline_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-file", help="file containing filters")
    parser.add_argument("-tweet", help="file containing messages to tweet")
    parser.add_argument("-interval", help="interval in minutes to send emails", type=int)
    parser.add_argument("-frequency", help="frequency in hours to send original tweets", type=int)

    args = parser.parse_args()

    if args.interval is None:
        args.interval = DEFAULT_INTERVAL
    # if args.limit is None:
    #     args.limit = DEFAULT_LIMIT
    # if args.sleep is None:
    #     args.sleep = DEFAULT_SLEEP

    return args


def create_filter_string_from_file(file):
    filename = open(file)
    f = filename.readlines()
    filename.close()

    filters = '#shashankandchimaaregreat' # always have #java as a filter just in case reading from file fails
    for line in f:
        filters = filters + ',' +line.replace('\n','')

    print('Using the filters: ' + filters)
    return filters


def build_gmail_service():
    # Path to the client_secret.json file downloaded from the Developer Console
    CLIENT_SECRET_FILE = 'client_secret.json'

    # Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
    OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.compose'

    # Location of the credentials storage file
    STORAGE = Storage('gmail.storage')

    # Start the OAuth flow to retrieve credentials
    flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
    http = httplib2.Http()

    # Try to retrieve credentials from storage or run the flow to generate them
    credentials = STORAGE.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, STORAGE, http=http)

    # Authorize the httplib2.Http object with our credentials
    http = credentials.authorize(http)

    # Build the Gmail service from discovery
    gmail_service = discovery.build('gmail', 'v1', http=http)

    return gmail_service


def read_from_file_and_store(tweetHolder, file):
    filename = open(file,encoding='utf8')
    f = filename.readlines()
    filename.close()

    num_lines = sum(1 for line in f)
    cnt = 1
    for line in f:
        if len(line) > 140: # TODO change to use error handling
            print('Skpping line {} of {}: Line is greater than 140 characters {}'.format(cnt, num_lines, line))
        else:
            tweetHolder.getTweets().append(line)
            #send_email(line)
            # twitter.update_status(line)
            print('Successfully stored line {} of {}: {}'.format(cnt, num_lines, line))
            # sleep(sleep)
        cnt += 1


def add_email_footer(email):
    body = email['msg'] + '\n\n\n' + EMAIL_FOOTER_LINE_2_0 + '\n' \
           + EMAIL_FOOTER_LINE_2_1 + '\n' + EMAIL_FOOTER_LINE_2_2 + '\n' \
           + EMAIL_FOOTER_LINE_2_3 + '\n' + EMAIL_FOOTER_LINE_2_4
    email['msg'] = body


# send email
def send_email(email):
    # create an email message to send
    add_email_footer(email)
    msg = MIMEText(email['msg'])
    msg['to'] = email['to']
    msg['from'] = email['from']
    msg['subject'] = email['subj']
    raw = base64.urlsafe_b64encode(msg.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}

    gmail_service = build_gmail_service()
    messages = gmail_service.users().messages()

    # send email
    try:
        result = (messages.send(userId="me", body=body).execute())
        print("Successfully sent email to {} @ {}. {}".format(email['to'], datetime.now(), str(result)))
    except Exception as ex:
        print('Could not send email. An error occurred: %s' % ex)


def send_tweet(instance, twitter, tweepy, msg):
    try:
        twitter.update_status(msg)
        print('Tweeted @ {}: {}'.format(datetime.now(), msg))
        return {'success': True}
    except tweepy.TweepError as ex:
        errmsg = ex.args[0][0]['message']
        body = 'ERROR: {}\nThe following tweet was not sent: "{}"'.format(errmsg, msg)
        email = build_email(instance)
        email['msg'] = body
        email['subj'] = 'TWITTERBOT ALERT: Tweet Error'
        send_email(email)
        print(body)
        return {'success': False, 'errMsg': errmsg}


def create_collections_of_tweets_for_email(tweets):
    collection_of_tweets = '*** This email consists of {} tweets ***\n\n'.format(len(tweets))
    for tweet in tweets:
        id = tweet.id_str
        user = tweet.user.screen_name
        tweet_url = 'https://twitter.com/{}/status/{}'.format(user, id)

        collection_of_tweets = collection_of_tweets + tweet_url + '\n' + tweet.text + '\n\n'

    return collection_of_tweets


def build_email(instance):
    sender = get_config_value(instance, 'EMAIL_SENDER')
    recipient = get_config_value(instance, 'EMAIL_RECIPIENT')
    email = {'to': recipient, 'from': sender}
    return email


def load_default_configs():
    default_configs = {'DEFAULT_CONSECUTIVE_NO_TWEET_EMAIL_THRESHOLD': DEFAULT_CONSECUTIVE_NO_TWEET_EMAIL_THRESHOLD,
                       'DEFAULT_TWEET_FREQUENCY': DEFAULT_TWEET_FREQUENCY,
                       'DEFAULT_EMAIL_RECIPIENT': DEFAULT_EMAIL_RECIPIENT, 'DEFAULT_EMAIL_SENDER': DEFAULT_EMAIL_SENDER}
    return default_configs


# get config value for given config key from datastore for this instance, if not found get default
def get_config_value(instance, key):
    configs = instance.db_connection.get_configs_collection()
    document = configs.distinct(key)
    try:
        config_value = document[0]
        if config_value is None:
            raise Exception('Config value is null')
    except:
        default_configs = load_default_configs()
        config_value = default_configs['DEFAULT_'+key.upper()]

    return config_value
