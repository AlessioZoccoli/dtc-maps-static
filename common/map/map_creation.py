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
    for p in data_points:
        sentiment = get_sentiment(p['text'], p['lang'])
        f.Marker(
            location=(p['longitude'], p['latitude']),
            popup=f.Popup("lang: {}, retweet: {}, favorited: {}".format(p['lang'],
                                                                        str(p['retweet_count']),
                                                                        str(p['favorite_count']))),
            icon=f.Icon(icon=icon_polarity(sentiment),
                        color=sentiment_leaflet_palette(sentiment),
                        radius=20),
        ).add_to(marker_cluster)

    return fmap


def add_markers_custom_cluster_color(fmap, data_points):

    def icon_polarity(sentiment):
        polarity = 'glyphicon glyphicon-hand-right'
        if sentiment > 0.0:
            polarity = 'glyphicon glyphicon-thumbs-up'
        elif sentiment < 0.0:
            polarity = 'glyphicon glyphicon-thumbs-down'
        return polarity

    icon_create_function = """
    function(cluster){
    children_count = cluster.getChildCount();
    children = cluster.getAllChildMarkers();
    
    cluster_sentiment = []
    
    children.forEach(function(marker) {
       color = marker.options.icon.options.markerColor
       if(typeof color !== 'undefined'){
           if (color.substring(0,5) === 'light'){
              cluster_sentiment.push(color.substring(5));
           } else {
              cluster_sentiment.push(color)
           }
       }
    });

    function mode(array){
            if(array.length == 0)
                return null;
            var modeMap = {};
            var maxEl = array[0], maxCount = 1;
            for(var i = 0; i < array.length; i++){
                var el = array[i];
                if(modeMap[el] == null)
                    modeMap[el] = 1;
                else
                    modeMap[el]++;  
                if(modeMap[el] > maxCount)
                {
                    maxEl = el;
                    maxCount = modeMap[el];
                }
            }
            return maxEl;
   }
    
    let sentiment = mode(cluster_sentiment); // most common color
    if(sentiment === 'lightred'){            // svg does not accept lightred
       sentiment = 'indianred'
    }
    
    console.log(sentiment + " " + cluster_sentiment.length)
    
    return L.divIcon({
    html:'<style type="text/css">.leaflet-div-icon { background: none!important; border: none!important; text-align: center;}</style><div id="container" background:"none" border:0><svg viewBox="0 0 30 30" ><circle cx="15" cy="15" r="15" fill='+sentiment+' viewBox="0 0 30 30"/><text x="50%" y="50%" text-anchor="middle" stroke="white" stroke-width="1px" dy=".3em">'+ children_count +'</text></svg></div>',
    iconSize: new L.Point(30,30)
    });
    }
    """
    # "#3F69AA"

    marker_cluster = MarkerCluster(icon_create_function=icon_create_function).add_to(fmap)

    for p in data_points:
        sentiment = get_sentiment(p['text'], p['lang'])
        f.Marker(
            location=(p['longitude'], p['latitude']),
            popup=f.Popup("lang: {}, retweet: {}, favorited: {}".format(p['lang'],
                                                                        str(p['retweet_count']),
                                                                        str(p['favorite_count']))),
            icon=f.Icon(icon=icon_polarity(sentiment),
                        color=sentiment_leaflet_palette(sentiment),
                        radius=20),
        ).add_to(marker_cluster)

    return fmap
