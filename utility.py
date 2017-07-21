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
    """ using the singleton pattern, makes connection with Mongo client and provides ability to interact with
    database """

    __instance = None

    def __new__(cls):
        if DBConnection.__instance is None:
            DBConnection.__instance = object.__new__(cls)
            client = MongoClient(db_url)
            db = client[db_name]
            DBConnection.__instance.database = db
        return DBConnection.__instance

    def get_tweet_review(self):
        return self.database[db_tweet_review]

    def get_tweet_queue(self):
        return self.database[db_tweet_queue]

    def get_configs(self):
        return self.database[db_configs]



