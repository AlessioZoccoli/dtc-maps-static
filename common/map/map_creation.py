import folium as f
from folium.plugins import FastMarkerCluster, MarkerCluster
from common.sentiment_analysis.sentiment_analysis import get_sentiment
from common.color.color import sentiment_to_hex, sentiment_leaflet_palette


def create_blank_map(location=(51.509865, -0.118092), tiles="cartodbpositron"):
    """
    Return a folium map without any marker or additional detail.
    :param location: center of the map
    :param tiles: background
    :return: folium map
    """
    fmap = f.Map(location=location, zoom_start=4, tiles=tiles, prefer_canvas=True)
    return fmap


def add_markers(fmap, data_points, color='#3186cc', has_sentiment=True):
    """
    Add markers on map
    :param fmap: folium map
    :param data_points: collection containing ([x,y], text)
    :param color: circle edge color
    :param has_sentiment: show tweet sentiment
    :return: folium map

    Each word in the lexicon has scores for:
         polarity: negative vs. positive    (-1.0 => +1.0)
         subjectivity: objective vs. subjective (+0.0 => +1.0)
        intensity: modifies next word?      (x0.5 => x2.0)

    """
    cmap = sentiment_color_map()
    for tweet in data_points:
        text = tweet['text']
        lang = tweet['lang']
        """
        from textblob import TextBlob
        from textblob.exceptions import NotTranslated

        try:
            if lang == 'en':
                blob = TextBlob(text)
            else:
                blob = TextBlob(text).translate(from_lang=lang, to='en')
            sentiment, subjectivity = blob.sentiment
            if has_sentiment and subjectivity >= 0.5:
                color = cmap(int(sentiment*1000))
        except NotTranslated:
            pass
        """
        try:
            f.CircleMarker(tweet['geo']['coordinates'],
                           popup=text,
                           radius=6,
                           fill=True,
                           color=color,
                           fill_opacity=0.7).add_to(fmap)
        except KeyError:
            # no geo reference
            pass

    return fmap


def add_markers_clustered_2(fmap, data_points, color='#3186cc', has_sentiment=True):
    data_points_sentiment = data_points.copy()

    data_points_sentiment['sentiment_color'] = data_points[['text', 'lang']]\
        .apply(lambda t: str(sentiment_to_hex(get_sentiment(t['text'], t['lang']))), axis=1)

    callback = ('function (row) {'
                'var circle = L.circle(new L.LatLng(row[0], row[1]), {color: row[4],  radius: 30});'
                'return circle};')

    return fmap.add_child(FastMarkerCluster(data_points.values.tolist(), callback=callback))


def add_markers_clustered(fmap, data_points):
    # https://github.com/python-visualization/folium/blob/master/examples/MarkerCluster.ipynb
    # print(next(data_points), '\n')
    marker_cluster = MarkerCluster().add_to(fmap)
    for idx, p in enumerate(data_points):
        f.Marker(
            location=(p['longitude'], p['latitude']),
            icon=f.Icon(color=sentiment_leaflet_palette(get_sentiment(p['text'], p['lang']))),
        ).add_to(marker_cluster)

    return fmap
