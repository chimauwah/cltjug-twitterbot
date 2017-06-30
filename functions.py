import httplib2
import base64
from apiclient import discovery
from oauth2client import client
from oauth2client.file import Storage
from oauth2client import tools
from email.mime.text import MIMEText
from datetime import datetime
from utility import *
from defaults import *
from constants import *


def send_text_message(txt):
    """sends the given txt as text message using twilio API

    :param txt:
    :return:
    """
    twilio.messages.create(to=to_number, from_=from_number, body=txt)


def create_filter_string_from_db():
    """returns the filter string from database config

    :return:
    """
    filterstring = get_config_value(FILTER_STRING, DEFAULT_FILTER_STRING)
    print('Using the filters: ' + filterstring)
    return filterstring


def create_filter_string_from_file(file):
    """create filter string from given file of filters

    :param file:
    :return:
    """
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
    client_secret_file = 'client_secret.json'

    # Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
    oauth_scope = 'https://www.googleapis.com/auth/gmail.compose'

    # Location of the credentials storage file
    storage = Storage('gmail.storage')

    # Start the OAuth flow to retrieve credentials
    flow = client.flow_from_clientsecrets(client_secret_file, scope=oauth_scope)
    http = httplib2.Http()

    # Try to retrieve credentials from storage or run the flow to generate them
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, http=http)

    # Authorize the httplib2.Http object with our credentials
    http = credentials.authorize(http)

    # Build the Gmail service from discovery
    gmail_service = discovery.build('gmail', 'v1', http=http)

    return gmail_service


def add_email_footer(email):
    """add ascii art footer

    :param email:
    :return:
    """
    body = email['msg'] + '\n\n\n' + EMAIL_FOOTER_LINE_1 + '\n' \
           + EMAIL_FOOTER_LINE_2 + '\n' + EMAIL_FOOTER_LINE_3 + '\n' \
           + EMAIL_FOOTER_LINE_4 + '\n' + EMAIL_FOOTER_LINE_5
    email['msg'] = body


def send_email(email):
    """create an email message and send

    :param email:
    :return:
    """
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

    try:
        result = (messages.send(userId="me", body=body).execute())
        print("Successfully sent email to {} @ {}. {}".format(email['to'], datetime.now(), str(result)))
    except Exception as ex:
        print('Could not send email. An error occurred: %s' % ex)


def send_tweet(twitter, tweepy, msg):
    try:
        twitter.update_status(msg)
        print('Tweeted @ {}: {}'.format(datetime.now(), msg))
        return {'success': True}
    except tweepy.TweepError as ex:
        errmsg = ex.args[0][0]['message']
        body = 'ERROR: {}\nThe following tweet was not sent: "{}"'.format(errmsg, msg)
        email = build_email()
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


def build_email():
    """builds email structure with sender and recipient

    :return:
    """
    sender = get_config_value(EMAIL_SENDER, DEFAULT_EMAIL_SENDER)
    recipient = get_config_value(EMAIL_RECIPIENT, DEFAULT_EMAIL_RECIPIENT)
    email = {'to': recipient, 'from': sender}
    return email


def get_config_value(key, defaultvalue):
    """get config value for given config key from databse if not found use given default value

    :param key:
    :param defaultvalue:
    :return:
    """
    configs = DBConnection().get_configs_collection()
    document = configs.distinct(key)
    try:
        config_value = document[0]
        if config_value is None:
            raise Exception('Config value not found')
    except:
        print("Config '" + key + "' not found. Using default value: " + str(defaultvalue))
        config_value = defaultvalue

    return config_value
