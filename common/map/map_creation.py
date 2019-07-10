import folium as f
from folium.plugins import MarkerCluster
from common.sentiment_analysis.sentiment_analysis import get_sentiment
from common.color.color import sentiment_leaflet_palette


def create_blank_map(location=(51.509865, -0.118092), tiles="cartodbpositron"):
    """
    Return a folium map without any marker or additional detail.
    :param location: center of the map
    :param tiles: background
    :return: folium map
    """
    fmap = f.Map(location=location, zoom_start=4, tiles=tiles, prefer_canvas=True)
    return fmap


def add_markers_clustered(fmap, data_points):
    marker_cluster = MarkerCluster().add_to(fmap)
    for idx, p in enumerate(data_points):
        f.Marker(
            location=(p['longitude'], p['latitude']),
            popup=f.Popup("lang: {}, retweet: {}, favorited: {}".format(p['lang'],
                                                                        str(p['retweet_count']),
                                                                        str(p['favorite_count']))),
            icon=f.Icon(color=sentiment_leaflet_palette(get_sentiment(p['text'], p['lang']))),
        ).add_to(marker_cluster)
    return fmap


def add_markers_clustered_pretty_icons(fmap, data_points):

    def icon_polarity(sentiment):
        polarity = 'glyphicon glyphicon-hand-right'
        if sentiment > 0.0:
            polarity = 'glyphicon glyphicon-thumbs-up'
        elif sentiment < 0.0:
            polarity = 'glyphicon glyphicon-thumbs-down'
        return polarity

    marker_cluster = MarkerCluster().add_to(fmap)
    for idx, p in enumerate(data_points):
        sentiment = get_sentiment(p['text'], p['lang'])
        f.Marker(
            location=(p['longitude'], p['latitude']),
            popup=f.Popup("lang: {}, retweet: {}, favorited: {}".format(p['lang'],
                                                                        str(p['retweet_count']),
                                                                        str(p['favorite_count']))),
            icon=f.Icon(icon=icon_polarity(sentiment),
                        icon_color=sentiment_leaflet_palette(sentiment),
                        radius=20),
        ).add_to(marker_cluster)

    return fmap
