from common.persistence.db import Database
import pandas as pd
from pprint import pprint
from common.map.map_creation import create_blank_map, add_markers_clustered
import config


if __name__ == '__main__':
    points = Database.get_tweets() # Database.select() #.limit(1000)
    fmap = create_blank_map()
    # pprint(pd.DataFrame(points)[['longitude', 'latitude', 'text', 'lang']].head())

    fmap = add_markers_clustered(fmap, points) #pd.DataFrame(points)[['longitude', 'latitude', 'text', 'lang']])
    fmap.save(config.output_uri)
