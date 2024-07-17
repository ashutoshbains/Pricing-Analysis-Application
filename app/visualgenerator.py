import json
import plotly
import numpy as np
import pandas as pd
import altair as alt
from app import main
import plotly.graph_objs as go
from app.databasehandler import DbHandler

db_handler = DbHandler()

# def label_bins(bin):
#     match bin:
#         case '(0, 5]':
#             return 1
#         case '(5, 10]':
#             return 2
#         case '(10, 15]':
#             return 3
#         case '(15, 20]':
#             return 4
#         case '(20, 25]':
#             return 5
#         case '(25, 30]':
#             return 6
#         case '(30, 35]':
#             return 7
#         case '(35, 40]':
#             return 8
#         case '(40, 45]':
#             return 9
#         case '(45, 50]':
#             return 10
#         case '(50, 55]':
#             return 11
#         case '(55, 60]':
#             return 12
#         case '(60, 65]':
#             return 13
#         case '(65, 70]':
#             return 14
#         case '(70, 75]':
#             return 15
#         case '(75, 80]':
#             return 16
#         case '(80, 85]':
#             return 17
#         case '(85, 90]':
#             return 18
#         case '(90, 95]':
#             return 19

# def get_store_prices_df(subcategory):
#     df = pd.DataFrame(columns=['url','Price','Store'])
#     stores = main.get_scrapers_for_subcategory(subcategory,get_names=True)
#     for store in stores:
#         store_df = db_handler.get_prices(store, subcategory)
#         store_df['Store'] = store
#         df = pd.concat([df, store_df],axis=0)
#     return df

# def average_price_visual(subcategory):
#     data = get_store_prices_df(subcategory)
#     min_price = data['Price'].min()
#     max_price = data['Price'].max()
#     bins = range(0,100,5)
    
#     data['Bins'] = pd.cut(data['Price'],bins=bins)
#     data.to_csv('mydata.csv')

#     # Assuming 'data' is a pandas DataFrame with columns: Name, Price, Store, Price-Bin

#     # Group by Store and Price-Bin, and count the occurrences
#     grouped = data.groupby(['Store', 'Bins']).size().reset_index(name='Count')
#     grouped['Bins'] = grouped['Bins'].astype(str)
#     grouped['Bins'] = pd.Categorical(grouped['Bins'], categories=sorted(grouped['Bins'].unique()))
#     grouped['Bins'] = grouped['Bins'].apply(label_bins)
#     grouped.to_csv('mygrouped.csv')
#     # Create traces for each store
#     traces = []
#     for store_name, store_data in grouped.groupby('Store'):
#         trace = go.Scatter(
#             x=store_data['Bins'],
#             y=store_data['Count'],
#             mode='lines+markers',
#             name=store_name
#         )
#         traces.append(trace)
#     # Define layout
#     layout = go.Layout(
#         width=500,
#         height=500
#     )

#     # Create figure object
#     fig = go.Figure(data=traces, layout=layout)

#     # Convert to JSON format
#     chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

#     return chart_json

# def get_subcategory_distribution(store, subcategory):

#     price_dict = db_handler.get_prices(store, subcategory)
#     data = pd.DataFrame(list(price_dict.items()), columns=['Product', 'Price'])

#     scale = alt.Scale(
#     domain=np.array(range(0,100)),
#     range=["#00000000"]  
#     )

#     price_upper_limit = int(data['Price'].max())
#     price_lower_limit = int(data['Price'].min())
#     print((price_upper_limit-price_lower_limit)/12)
    
#     single = alt.selection_single(fields=['bin'],on='mouseover')

#     chart = alt.Chart(data).transform_calculate(
#         bin_label="datum.bin+'-'+(datum.bin+3)"
#     ).encode(
#         alt.X('Price', axis=alt.Axis(labelColor='#707070', tickColor='#707070', labelFont='Arial'), title='', bin=alt.Bin(extent=[price_lower_limit,price_upper_limit],step=5)),
#         alt.Y('count()', title='', axis=alt.Axis(grid=False, labelColor='#707070', tickColor='#707070', labelFont='Arial')),
#         tooltip=[
#             alt.Tooltip('bin_label:O', title='Price Range'),
#             alt.Tooltip('count()', title='Product Count'),
#             alt.Tooltip('Product', title='Products in Bin', aggregate='values')
#         ]
#     ).transform_bin(
#         'bin',
#         field='Price',
#         bin=True
#     ).properties(
#         width=450,
#         height=300
#     ).interactive(
#         bind_y=False,
#         bind_x=False
#     )

#     area_chart = chart.mark_area(
#         opacity=0.6, color='#91C6BC', interpolate='monotone', line={'color': '#6CA1F0', 'width': 2}
#     )

#     rect_marks = chart.mark_rect(filled=True, fillOpacity=0.6).encode(
#         y=alt.YDatum(0,type='quantitative',scale=alt.Scale(domain=[0, 100])),
#         y2=alt.YDatum(100),
#         color=alt.condition(single, alt.Color('bin:O',scale=scale,legend=None), alt.value('#EEEEEE'))
#     )   

#     chart = (area_chart + rect_marks).configure_view(stroke=None).add_selection(single)

#     chart_json = chart.to_json()
    
#     return chart_json


# ------------------------------- [DEPRECATED] ---------------------------------------------

# def get_XXsubcategory_distribution(store, subcategory):
#     price_dict = db_handler.get_prices(store, subcategory)
#     data = pd.DataFrame(list(price_dict.items()), columns=['Product', 'Price'])

#     # Calculate price limits
#     price_upper_limit = int(max(price_dict.values()))
#     price_lower_limit = int(min(price_dict.values()))

#     # Define bins and labels
#     bins = range(price_lower_limit, price_upper_limit, 3)
#     labels = [f'{start}-{end}' for start, end in zip(bins[:-1], bins[1:])]

#     # Bin the data
#     data['bin'] = pd.cut(data['Price'], bins=bins, labels=labels, right=False)

#     # Count occurrences in each bin
#     bin_counts = data['bin'].value_counts().reset_index()
#     bin_counts.columns = ['bin', 'count']

#     # Aggregate product names for each bin
#     tooltip_data = pd.merge(bin_counts, data.groupby('bin')['Product'].apply(lambda x: ', '.join(x)).reset_index(), on='bin')
#     tooltip_data['x_tick'] = tooltip_data['bin'].str.split('-').str[0]
#     count_max = max(tooltip_data['count'].values)

#     single = alt.selection_interval(encodings=['x'])

#     # Create Altair chart with smoothed data
#     chart = alt.Chart(tooltip_data).mark_area(opacity=0.3, color='lightgreen',interpolate='monotone', line={'color': 'green', 'width': 2}).encode(
#         alt.X('x_tick:Q', axis=alt.Axis(
#                 tickOffset=-5,
#                 values=np.array(range(price_lower_limit,price_upper_limit,3)),
#                 grid=False
#             ),),
#         y=alt.Y('count:Q', title='', axis=alt.Axis(grid=False), scale=alt.Scale(domain=[0, count_max+10])),
#         tooltip=['bin:O', 'count:Q', 'Product:N']

#     ).properties(
#         width=450,
#         height=300,
#     ).interactive(
#         bind_y = False,
#         bind_x = False
#     ).add_selection(
#         single
#     )

#     chart_json = (chart).to_json()
#     return chart_json

# -------------------------------[CHECKPOINT] ---------------------------------------
def get_subcategory_distribution(store, subcategory):

    data = db_handler.get_prices(store, subcategory)

    scale = alt.Scale(
    domain=np.array(range(0,100)),
    range=["#5BDDC5"]  
    )
    

    price_upper_limit = int(data['Price'].max())
    price_lower_limit = int(data['Price'].min())
    
    single = alt.selection_single(fields=['bin'])

    chart = alt.Chart(data).transform_calculate(
        bin_label="datum.bin+'-'+(datum.bin+3)"
    ).encode(
        alt.X('Price', axis=alt.Axis(labelColor='#707070', tickColor='#707070', labelFont='Arial'), title='', bin=alt.Bin(extent=[price_lower_limit, price_upper_limit], step=3.0)),
        alt.Y('count()', title='', axis=alt.Axis(grid=False, labelColor='#707070', tickColor='#707070', labelFont='Arial')),
        tooltip=[
            alt.Tooltip('bin_label:O', title='Price Range'),
            alt.Tooltip('count()', title='Product Count')
            # alt.Tooltip('Product', title='Products in Bin', aggregate='values')
        ]
    ).transform_bin(
        'bin',
        field='Price',
        bin=alt.Bin(extent=[price_lower_limit, price_upper_limit], step=3.0)
    ).properties(
        width=450,
        height=300
    ).interactive(
        bind_y=False,
        bind_x=False
    )

    area_chart = chart.mark_area(
        opacity=0.6, color='#91C6BC', interpolate='monotone', line={'color': '#6CA1F0', 'width': 2}
    )

    point_chart = chart.mark_point(size=160, filled=True, opacity=1, fillOpacity=0.8).encode(
    color=alt.condition(single, alt.Color('bin:O',scale=scale,legend=None), alt.value('#00000000'))
    )   

    chart = (area_chart + point_chart).configure_view(stroke=None).add_selection(single)

    chart_json = chart.to_json()
    
    return chart_json
