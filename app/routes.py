import numpy as np
from app import app
from app import config
from pyecharts.charts import Bar
from flask import render_template
from pyecharts import options as opts
from app.databasehandler import DbHandler

dbHandler = DbHandler()

def get_histogram(prices, bin_size):
    # Calculate the minimum and maximum prices
    min_price = min(prices)
    max_price = max(prices)-120

    # Calculate the number of bins
    num_bins = int(np.ceil((max_price - min_price) / bin_size))

    # Define the bins
    bins = [min_price + i * bin_size for i in range(num_bins + 1)]

    # Calculate the frequency of prices in each bin
    hist, _ = np.histogram(prices, bins=bins)

    return bins, hist.tolist()

@app.route('/')
@app.route('/index')
def index():
    # Generate your Pyecharts visualization
    prices = dbHandler.get_prices('Rural Handmade','Planters')
    bins, hist = get_histogram(prices, 0.5)
    bar = (
        Bar()
        .add_xaxis(bins)
        .add_yaxis('Freq',hist,bar_width='100%')
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar Chart"),
                          legend_opts=opts.LegendOpts(pos_right="20%", pos_top="20%"),
                            datazoom_opts=opts.DataZoomOpts(type_="slider", range_start=0, range_end=100),
                             toolbox_opts=opts.ToolboxOpts(),)
    )
    content = {'user':'Max'}
    posts = [
        {
            'author': {'username' : 'John'},
            'body' : 'To be or not to be'
        },
        {
            'author': {'username' : 'Doe'},
            'body' : 'Retrospective interpretation'
        }
    ]

    return render_template('index.html', content=content,posts=posts, chart=bar.render_embed())

