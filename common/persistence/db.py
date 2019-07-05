from pymongo import MongoClient
from config import client_uri, db_uri, collection_tweet_simple


class Database(object):
    client = MongoClient(client_uri)
    db = client[db_uri]
    tweets = db[collection_tweet_simple]

    @classmethod
    def get_n_documents(cls, n=10):
        return cls.tweets.find().limit(n)
