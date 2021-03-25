import requests
import json
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
import os
import webbrowser
import folium
from folium import plugins
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import data_management.extension_management

def extension_map_1():
    '''Call Seoul geometric data
    Args:
        None
    Return:
        json_data (dict)
    '''
    state_geo = '../original_data/skorea_municipalities_geo_simple.json'

    with open(state_geo, encoding='utf-8') as f:
        json_data = json.load(f)
    
    return json_data

def extension_map_2(df, x, json_data, color = 'Blues'):
    '''
    Args:
        df (dataframe)
        x (string)
        json_data (json)
        color (string)
    Return:
        m  (choropleth)
    '''
    
    #seoul geographic value
    m = folium.Map(location=[37.564214, 127.001699], tiles="OpenStreetMap", zoom_start=11)

    m.choropleth(
        geo_data=json_data,
        data=df,
        columns=['district', x],
        fill_color=color,
        fill_opacity=0.7,
        line_opacity=0.3,
        color = 'gray',
        key_on = 'feature.id'
    )
    return m