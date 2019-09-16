from pymongo import MongoClient
from config import client_uri, db_uri, collection_tweet_simple


class Database(object):
    client = MongoClient(client_uri)
    db = client[db_uri]
    tweets = db[collection_tweet_simple]

    @classmethod
    def get_n_tweets(cls, n=10):
        return cls.tweets.find().limit(n)

    @classmethod
    def get_tweets_by_hashtags(cls, *hashtags):
        """
        returns tweets from mongo filtered by hashtag with their relevant fields
        """

        print("QUERY : ", hashtags)

        assert all(isinstance(s, str) for s in hashtags)
        if isinstance(hashtags, str):
            hashtags = [hashtags]

        cursor = cls.tweets.aggregate([
            {
                '$match': {
                    'geo.coordinates': {'$exists': True, '$ne': None},
                }
            },
            {
                '$unwind': '$entities.hashtags'
            },
            {
                '$project': {
                    'lang': 1,
                    'text': 1,
                    'favorite_count': 1,
                    'retweet_count': 1,
                    'longitude': {'$arrayElemAt': ['$geo.coordinates', 0]},
                    'latitude': {'$arrayElemAt': ['$geo.coordinates', 1]},
                    'entities': '$entities.hashtags.text'
                }
            },
            {
                '$group': {
                    '_id': '$_id',
                    'text': {'$first': '$text'},
                    'lang': {'$first': '$lang'},
                    'favorite_count': {'$first': '$favorite_count'},
                    'retweet_count': {'$first': '$retweet_count'},
                    'longitude': {'$first': '$longitude'},
                    'latitude': {'$first': '$latitude'},
                    'hashtags': {'$push': '$entities'}
                }
            },
            {
                '$match': {
                    'hashtags': {'$in': hashtags}
                 }
            }
        ])

        return cursor

    @classmethod
    def get_tweets(cls):
        """
        returns tweets from mongo with their relevant fields
        """
        print("QUERYING\n")

        cursor = cls.tweets.aggregate([
            {
                '$match': {
                    'geo.coordinates': {'$exists': True, '$ne': None},
                }
            },
            {
                '$project': {
                    'lang': 1,
                    'text': 1,
                    'favorite_count': 1,
                    'retweet_count': 1,
                    'longitude': {'$arrayElemAt': ['$geo.coordinates', 0]},
                    'latitude': {'$arrayElemAt': ['$geo.coordinates', 1]},
                }
            },
            {
                '$group': {
                    '_id': '$_id',
                    'text': {'$first': '$text'},
                    'lang': {'$first': '$lang'},
                    'favorite_count': {'$first': '$favorite_count'},
                    'retweet_count': {'$first': '$retweet_count'},
                    'longitude': {'$first': '$longitude'},
                    'latitude': {'$first': '$latitude'}
                }
            }
        ])
        print("... QUERY DONE\n")

        return cursor

"""
﻿db.getCollection('tweets').aggregate([
    {
        '$match': {
            'geo.coordinates': {'$exists': true, '$ne':null},
            'lang':'it'
            }
    },
    {
       '$unwind': '$entities.hashtags'    
    },
    {
        '$project': {
                'lang': 1,
                'favorite_count': 1,
                'retweet_count': 1,
                'longitude': 1,
                'latitude': 1,
                'entities': '$entities.hashtags.text'
                }
    },
    {
        '$group': {
            '_id': '$_id',
            'lang': {'$first': '$lang'},
            'favorite_count': {'$first': '$favorite_count'},
            'retweet_count': {'$first': '$retweet_count'},
            'longitude': {'$first': '$longitude'},
            'latitude': {'$first': '$latitude'},
            'hashtags': { '$push': '$entities' }
         }
    },
    {
        '$match': {
            'hashtags': {'$in': ['igers', 'UneDisciplinePourTokyo2020']}
         }
    }
    ])
"""
