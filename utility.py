"""utility class holding shared resources"""

import tweepy
from pymongo import MongoClient
from db_properties import *
from twilio.rest import Client
from twilio_properties import *
from credentials_cltjugtest import *

# Access and authorize our Twitter credentials
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitter = tweepy.API(auth)


# Access and authorize Twilio account
twilio = Client(acct_sid, auth_token)


class DBConnection:
    """ using the singleton pattern, makes connection with Mondo client and provides ability to interact with
    database """

    __instance = None

    def __new__(cls):
        if DBConnection.__instance is None:
            DBConnection.__instance = object.__new__(cls)
            client = MongoClient(db_url)
            db = client[db_name]
            DBConnection.__instance.database = db
        return DBConnection.__instance

    def get_tweet_collection(self):
        return self.database[db_tweet_collection]

    def get_configs_collection(self):
        return self.database[db_config_collection]



