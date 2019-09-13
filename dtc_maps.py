from flask import Flask, render_template
from common.persistence.db import Database
from common.map.map_creation import create_blank_map, add_markers_custom_cluster_color
from time import time

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    points = Database.get_tweets()
    assert points

    start_creation = time()
    fmap = create_blank_map()
    fmap = add_markers_custom_cluster_color(fmap, points)
    assert fmap

    end_creation = time()
    print("{} seconds to create the map\n".format(end_creation - start_creation))
    return fmap._repr_html_()


if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)
