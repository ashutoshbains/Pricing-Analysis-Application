import numpy as np
from app import app
from app import main
from app import config
from pyecharts.charts import Bar
from pyecharts.charts import Line
from flask import render_template
from pyecharts import options as opts
from app.databasehandler import DbHandler

dbHandler = DbHandler()

def get_histogram(prices, bin_size):
    # Calculate the minimum and maximum prices
    min_price = min(prices)
    max_price = max(prices)

    # Calculate the number of bins
    num_bins = int(np.ceil((max_price - min_price) / bin_size))

    # Define the bins
    bins = [min_price + i * bin_size for i in range(num_bins + 1)]

    # Calculate the frequency of prices in each bin
    hist, _ = np.histogram(prices, bins=bins)

    return bins, hist.tolist()

@app.route('/')
@app.route('/dashboard')
def index():
    # Generate your Pyecharts visualization
    prices_planters = dbHandler.get_prices('Ten Thousand Villages','Planters')
    prices_door_mats = dbHandler.get_prices('Ten Thousand Villages','Earrings')
    bins, hist = get_histogram(prices_planters, 1)
    bins2, hist2 = get_histogram(prices_door_mats, 0.1)
    bar_planters = (
        Bar()
        .add_xaxis(bins)
        .add_yaxis('Freq',hist,bar_width='100%')
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar Chart"),
                          legend_opts=opts.LegendOpts(pos_right="20%", pos_top="20%"),
                            datazoom_opts=opts.DataZoomOpts(type_="slider", range_start=0, range_end=100),
                             toolbox_opts=opts.ToolboxOpts(),)
    )
    bar_doormats = (
        Bar()
        .add_xaxis(bins2)
        .add_yaxis('Freq',hist2,bar_width='100%')
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar Chart"),
                          legend_opts=opts.LegendOpts(pos_right="20%", pos_top="20%"),
                            datazoom_opts=opts.DataZoomOpts(type_="slider", range_start=0, range_end=100),
                             toolbox_opts=opts.ToolboxOpts(),)
    )
    area_chart = Line()

    # Add x-axis and y-axis data
    area_chart.add_xaxis(xaxis_data=bins2)
    area_chart.add_yaxis(
        series_name="Freq",
        y_axis=hist2,
        is_smooth=True,  # Add smooth curve to the area chart
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),  # Adjust area opacity
    )

    # Set global options
    area_chart.set_global_opts(
        title_opts=opts.TitleOpts(title="Area Chart"),
        legend_opts=opts.LegendOpts(pos_right="20%", pos_top="20%"),
        datazoom_opts=opts.DataZoomOpts(type_="slider", range_start=0, range_end=100),
        toolbox_opts=opts.ToolboxOpts(),
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
    # main.update_all_data()
    return render_template('dashboard.html', content=content,posts=posts, chart1=bar_planters.render_embed(), chart2 = bar_doormats.render_embed(),area = area_chart.render_embed())

