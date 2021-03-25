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
import analysis.extension_analysis

def extension_map_institute():
    '''Show distribution of private institutes related to university entrance exam
        on Seoul map
    Args:
        None
    Return:
        m (choropleth)
    '''
    df = extension_df_1()
    json_data = extension_map_1()
    m = extension_map_2(df, "university related institute", json_data)
    return m

def extension_map_landprice():
    '''Show the average price of land for living purpose on Seoul map
    Args:
        None
    Return:
        m (choropleth)
    '''
    df = extension_df_2()
    json_data = extension_map_1()
    m = extension_map_2(df, "land_price", json_data, color = "PuRd")
    
    return m 