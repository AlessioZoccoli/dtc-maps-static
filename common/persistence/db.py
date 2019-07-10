from pymongo import MongoClient
from config import client_uri, db_uri, collection_tweet_simple


class Database(object):
    client = MongoClient(client_uri)
    db = client[db_uri]
    tweets = db[collection_tweet_simple]

    @classmethod
    def get_n_documents(cls, n=10):
        return cls.tweets.find().limit(n)

    @classmethod
    def select(cls, field=('geo.coordinates', 'text', 'lang')):
        return cls.tweets.find({}, {f: 1 for f in field})

    @classmethod
    def get_tweets(cls):
        """
        returns tweets from mongo with their relevant fields
        """

        return cls.tweets.aggregate([
            {
                '$match': {
                    'geo.coordinates': {'$exists': True, '$ne': None}
                }
            },
            {
                '$project': {
                    'lang': 1,
                    'text': 1,
                    'favorite_count': 1,
                    'retweet_count': 1,
                    'longitude': {'$arrayElemAt': ['$geo.coordinates', 0]},
                    'latitude': {'$arrayElemAt': ['$geo.coordinates', 1]}
                }
            }
        ])