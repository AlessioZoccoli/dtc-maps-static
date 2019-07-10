from common.persistence.db import Database
from common.map.map_creation import create_blank_map, add_markers_clustered, add_markers_clustered_pretty_icons
import config
from time import time

if __name__ == '__main__':
    points = Database.get_tweets()

    start_creation = time()

    fmap = create_blank_map()
    fmap = add_markers_clustered_pretty_icons(fmap, points)

    end_creation = time()
    print("{} seconds for the map creation".format(end_creation - start_creation))

    fmap.save(config.output_uri)
    print("saved to ", config.output_uri)
