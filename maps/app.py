from common.persistence.db import Database
import pandas as pd
from pprint import pprint
from common.map.map_creation import create_blank_map, add_markers_clustered
import config


if __name__ == '__main__':
    points = Database.get_tweets()
    fmap = create_blank_map()
    fmap = add_markers_clustered(fmap, points)

    fmap.save(config.output_uri)
