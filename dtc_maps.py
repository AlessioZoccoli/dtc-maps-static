from flask import Flask
from common.persistence.db import Database
from common.map.map_creation import create_map

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def map_all_tweets():
    """
    Generate a map containing unfiltered tweets
    :return: an HTML representation for the map
    """
    tweets = Database.get_tweets()
    assert tweets
    m = create_map(tweets, limit=100)
    return m


@app.route("/hashtags/<ht>")
@app.route("/hashtag/<ht>")
def map_hashtags(ht):
    """
    Generate a map containing filtered tweets by hashtag
    :return: an HTML representation for the map
    """
    tweets = Database.get_tweets_by_hashtags(ht)
    assert tweets
    m = create_map(tweets)
    return m


if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)
