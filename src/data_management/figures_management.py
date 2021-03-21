import pandas as pd
import numpy as np
import econtools.metrics as mt
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from itertools import *
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import data_management.tables_management
import analysis.tables_analysis
import analysis.figures_analysis
import final.table_produce



def figure1_1(df, alpha, beta):
    '''Generate beliefs variables(beliefs1, beliefs2, bliefs3) and truth variable
    
    Args:
        df (dataframe)
        alpha (float)
        beta (float)
    Returns:
        df (dataframe)
    '''

    df["truth"] = 0
    t = df.columns.get_loc("truth")

    for k in range(1,4):
        
        df["beliefs{0}".format(k)] = np.nan
        
        ind = df.columns.get_loc("beliefs{0}".format(k))
        
        for i in range(len(df)):
            if k == 1:
                df.iloc[i,ind] = df.iloc[i,t]*np.random.normal(0,20)
            elif k == 2:
                df.iloc[i, ind] = 50*(1-alpha)+alpha* df.iloc[i,t]+np.random.normal(0,30)
            else:
                df.iloc[i, ind] = 50*(1-beta)+beta* df.iloc[i,t]+np.random.normal(0,30)
                df.iloc[i,t] = (i+1) - math.floor((i+1)/100) * 100
                
        df.loc[df["beliefs{0}".format(k)] <= 0, "beliefs{0}".format(k)] = 0
        df.loc[df["beliefs{0}".format(k)] > 100, "beliefs{0}".format(k)] = 100
            
    return df



def figure1_2(df, name_list):
    '''Gernrate columns based on *beliefs* variables and *truth* variable
    
    Args:
        df (dataframe)
        name_list (list)
    
    Returns:
        df (dataframe)
    '''

    prefix = ["ic_", "is_"]
    col_list = []
    
    for pre in prefix:
        for name in name_list:
            df[pre + name] = np.nan
            col_list.append(pre + name)

    for i in range(len(df)):
        for col in col_list:
            idx = df.columns.get_loc(col)

            if col[1] =="c":

                if col[3] == "t":
                    t = df.columns.get_loc("truth")
                else:
                    t = df.columns.get_loc(col[3:])

                df.iloc[i, idx] = 30+df.iloc[i,t]+np.random.normal(0,10)

            else:
                if col[3] == "t":
                    t = df.columns.get_loc("truth")
                else:
                    t = df.columns.get_loc(col[3:])
                
                df.iloc[i, idx] = 100+ 30-df.iloc[i,t]+np.random.normal(0,10)
    return df


def figure4_1(df, x):
    '''Get lower bound and upper bound values

    Args:
        df (dataframe)
        x (string)
    Returns:
        lb (float)
        ub (float)
    '''

    df_reg = df[df["treat"]=="Control"]
    des = df_reg[x].describe(percentiles=[.05, .95])
    lb = des["5%"]
    ub = des["95%"]

    return lb, ub