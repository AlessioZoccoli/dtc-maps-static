from branca import colormap
from matplotlib import cm
from matplotlib.colors import to_hex
from numpy import interp


def sentiment_color_map(minv=-1000, maxv=1000):
    cmap = colormap.LinearColormap(colors=['red', 'lightgreen', 'green'],
                                   index=[minv, 0, maxv], vmin=-minv, vmax=maxv)
    return cmap.to_step(7)


def sentiment_to_hex(sentiment, max_col_val=20):
    sentiment_in_range = interp(sentiment, [-1.0, 1.0], [0.0, max_col_val])
    col_range = cm.get_cmap('RdYlGn', max_col_val)
    return to_hex(col_range(sentiment_in_range))


def sentiment_leaflet_palette(sentiment):
    """
    UserWarning: color argument of Icon should be one of:
            {'lightblue', 'purple', 'orange', 'blue', 'darkgreen', 'white', 'pink', 'cadetblue', 'darkpurple',
            'green', 'darkblue', 'gray', 'lightgrayblack', 'lightgreen', 'red', 'darkred', 'lightred', 'beige'}.

    """
    if sentiment < -0.6:
        color = 'darkred'
    elif -0.6 <= sentiment < -0.3:
        color = 'red'
    elif -0.3 <= sentiment < 0.0:
        color = 'lightred'
    elif 0.0 < sentiment < 0.3:
        color = 'lightgreen'
    elif 0.3 <= sentiment < 0.6:
        color = 'green'
    elif 0.6 <= sentiment <= 1.0:
        color = 'darkgreen'
    else:
        color = 'gray'
    return color
