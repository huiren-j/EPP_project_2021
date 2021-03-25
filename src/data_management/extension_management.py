import requests
import json
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
import os
import webbrowser
import folium
from folium import plugins


def extension_df_code():
    '''Prepare datasets for extension
    Arg: 
        None
    Return:
        df_code (dataframe)
    '''
    df_code = df_code = pd.read_excel("../original_data/district_code_seoul.xlsx")
    
    df =df[['district', 'university related institute']]
    df = df.drop([0])

    #translation korean column names to english
    df_code = df_code.rename(columns = {'통계청행정동코드' : 'code', '행자부행정동코드':'code_mois', '시도명':'city', '시군구명':'district', '행정동명': 'village'})
    
    df_code = df_code.drop([0])
    df_code["code"] = df_code["code"].astype('str')
    df_code["code_district"] = df_code["code"].str[0:5]
    df_code = df_code.drop_duplicates(['district'])
    df_code = df_code.drop(['city','village', 'code', 'code_mois'], axis = 1)
    
    return df_code 
    
def extension_df_merge(df):
    '''Merge input dataset with postal code data
    Arg:
        df (dataframe)
    Retrun:
        df (dataframe)
    '''
    
    df_code = extension_df_code()
    df = pd.merge(df, df_code, how = "left")
    
    return df

def extension_df_1():
    '''Prepare datasets for extension allocating districs postal code to private institute location
    Arg: 
        None
    Return:
        df (dataframe)
    '''
    df_institute = pd.read_excel("../original_data/private_institute.xlsx")
    df_institute =df_institute[['district', 'university related institute']]
    df_institute = df_institute.drop([0])
    
    df = extension_df_merge(df_institute)
    
    return df

def extenstion_df_2():
    '''Prepare datasets for extension allocating district postal codes to land price
    Arg:
        None
    Return:
        df (dataframe)
    '''
    
    df_land = pd.read_csv("../original_data/land_price.csv", engine = 'python')
    
    #translation columns to english
    df_land = df_land.rename(columns = {'시군구명': 'district', '필지구분명': 'land_type',  '공시지가(원/㎡)':'land_price'})
    
    #filtering land_type = living purpose land
    df_land = df_land[df_land["land_type"]=="토지"]
    df_land = pd.DataFrame(df_land.groupby("district")["land_price"].mean()).reset_index()

    df = extension_df_merge(df_land)
    
    return df