import numpy as np
import pandas as pd
import altair as alt
from app.databasehandler import DbHandler

db_handler = DbHandler()

def get_subcategory_distribution(store, subcategory):

    price_dict = db_handler.get_prices(store, subcategory)
    data = pd.DataFrame(list(price_dict.items()), columns=['Product', 'Price'])

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
            alt.Tooltip('count()', title='Product Count'),
            alt.Tooltip('Product', title='Products in Bin', aggregate='values')
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

    point_chart = chart.mark_point(size=80, filled=True, opacity=1, fillOpacity=0.8).encode(
    color=alt.condition(single, alt.Color('bin:O',scale=scale,legend=None), alt.value('lightgray'))
    )   

    chart = (area_chart + point_chart).configure_view(stroke=None).add_selection(single)

    chart_json = chart.to_json()
    
    return chart_json


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
# def get_subcategory_distribution(store, subcategory):

#     price_dict = db_handler.get_prices(store, subcategory)
#     data = pd.DataFrame(list(price_dict.items()), columns=['Product', 'Price'])

#     scale = alt.Scale(
#     domain=np.array(range(0,100)),
#     range=["#5BDDC5"]  
#     )
    

#     price_upper_limit = int(data['Price'].max())
#     price_lower_limit = int(data['Price'].min())
    
#     single = alt.selection_single(fields=['bin'])

#     chart = alt.Chart(data).transform_calculate(
#         bin_label="datum.bin+'-'+(datum.bin+3)"
#     ).encode(
#         alt.X('Price', axis=alt.Axis(labelColor='#707070', tickColor='#707070', labelFont='Arial'), title='', bin=alt.Bin(extent=[price_lower_limit, price_upper_limit], step=3.0)),
#         alt.Y('count()', title='', axis=alt.Axis(grid=False, labelColor='#707070', tickColor='#707070', labelFont='Arial')),
#         tooltip=[
#             alt.Tooltip('bin_label:O', title='Price Range'),
#             alt.Tooltip('count()', title='Product Count'),
#             alt.Tooltip('Product', title='Products in Bin', aggregate='values')
#         ]
#     ).transform_bin(
#         'bin',
#         field='Price',
#         bin=alt.Bin(extent=[price_lower_limit, price_upper_limit], step=3.0)
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

#     point_chart = chart.mark_point(size=80, filled=True, opacity=1, fillOpacity=0.8).encode(
#     color=alt.condition(single, alt.Color('bin:O',scale=scale,legend=None), alt.value('lightgray'))
#     )   

#     chart = (area_chart + point_chart).configure_view(stroke=None).add_selection(single)

#     chart_json = chart.to_json()
    
#     return chart_json
