import pandas as pd
import numpy as np
import econtools.metrics as mt
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from itertools import *
from functions import *

#Below functions are for tables
def treat_dummy(df):
    '''This function is to convert string type categorical variable
    to dummy variable of categorial variable'''

    df = pd.get_dummies(df,columns=["treat"])
    df["treat"] = df["treat_Treatment"]
    df = df.drop(columns=["treat_Control"])
    df = df.drop(columns=["treat_Treatment"])
    
    return df

def col_names(df, name):
    '''This function calculate and generate new variables for regression
    or rename columns. This frame is used repeatedly with different data and
    for different tables. That's why I made it as a function'''

    df["ds_"] = df["ds_" + name]
    df["ds_educ"] = df["ds_" + name]*df["educ_ave"]
    df["treat_ds_"] = df["treat_ds_"+name]
    df["treat_ds_educ"] = df["treat_ds_"+name]*df["educ_ave"]
    df["treat_educ_used"] = df["treat"]*df["educ_ave"]
    df["perf_"] = df[name]
    df["perf_educ"] = df[name]*df["educ_ave"]
    df["treat_perf"] = df["treat_"+name]
    df["treat_perf_educ"] = df["treat_"+name]*df["educ_ave"]
    
    if name != "ave" and name != "math_engl":
        df["wb_"+name] = df["wb_"+name]*100
    
    return df


def neg(df, sub, prefix = ""):
    '''
    function converting a variable to negative value.
    Parameters are dataframe, prefix list, target variable
    '''
    
    for i in prefix:
        if i == "":
            df[sub] = -df[sub]
        else:
            df[i+sub] = -df[i+sub]
    return df


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