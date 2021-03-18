import pandas as pd
import numpy as np
import econtools.metrics as mt
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from itertools import *

import sys
sys.path.insert(0, '../src/data_management')
import figures_management
import tables_management


def table1(df, panel_list, columns):
    '''Produce descriptive table
    
    Args:
        df (dataframe)
        panel_list (list)
        columns (list)
    
    Returns:
        d (dataframe)
    '''
    df = treat_dummy(df)

    d = {}
    for t in range(len(panel_list)):
        tab_1 = pd.DataFrame(columns = columns, index =range(0, len(panel_list[t])))
        d["Panel{0}".format(t+1)] = tab_1
        tab_1 = d["Panel"+str(t+1)]
        i = 0
        for pan in panel_list[t]:
            mean = round(df[pan].mean(),2)
            tab_1.loc[i,columns[0]] = mean

            std = round(df[pan].std(),2)
            tab_1.loc[i,columns[1]] = std

            mean_c = round(df.loc[df["treat"]==0, pan].mean(),2)
            tab_1.loc[i,columns[2]] = mean_c

            mean_t = round(df.loc[df["treat"]==1, pan].mean(),2)
            tab_1.loc[i,columns[3]] = mean_t

            result = mt.reg(df, pan, "treat", fe_name = "school_code", cluster="hhid")
            result.summary[["coeff","se","p>t"]]
            tab_1.loc[i, columns[4]] = round(result.summary.loc["treat","coeff"],2)
            tab_1.loc[i, columns[5]] = round(result.summary.loc["treat","se"],2)
            tab_1.loc[i, columns[6]] = round(result.summary.loc["treat","p>t"],2)

            i= i+1
    
    d = pd.concat(d)
    return d

def table2(df, y, x):
    '''Regression table
    Args:
        df (dataframe)
        y (string)
        x (string)
    Returns:
        result (dataframe)
    '''

    df = treat_dummy(df)
    df = col_names(df, x)
    df, X = reg_var(df)

    result = mt.reg(df, y, X , fe_name = "school_code", cluster="hhid").summary
    return result

def table3(df, y):
    '''Regression result

    Args:
        df (dataframe)
        y (list)
    
    Returns:
        d (dataframe)
    '''

    df = treat_dummy(df)
    df, ctrl_list = table3_var(df)
    X = ["treat", "treat_ave", "ave", "ave_educ_ave", "educ_ave"] + ctrl_list
    
    d = {}
    for i in y:
        result = mt.reg(df, i, X , fe_name = "school_code", cluster="hhid").summary
        d["table_{0}".format(i)] = result
    
    d = pd.concat(d)
    return d


def tab4_PanelA(df, type_list)
    '''Regression result table

    Args:
        df (dataframe)
        type_list (list)
    Returns:
        PanelA (dataframe)
    '''
    df = treat_dummy(df)

    panel_A = []

    df["score_used"] = np.nan
    df["score_used_educ"] = np.nan
    df["educ_used"] = np.nan

    for typ in type_list:

        df["score_used"] = df[typ]
        df["score_used_educ"] = df["score_used"]*df["educ_ave"]
        df["educ_used"] = df["educ_ave"]

        result = mt.reg(df, "b_"+typ, ["score_used_educ", "score_used", "educ_used"], fe_name = "school_code", addcons = True).summary
        result = result.rename(columns = {"coeff": typ})[typ]
        panel_A.append(result)

    panel_A = pd.concat(panel_A, axis = 1)
    return panel_A


def tab4_panelB(df, name):
    '''Regression result table

    Args:
        df (dataframe)
        name (string)
    Returns:
        reg_result (dataframe)
    '''
    
    df = treat_dummy(df)
    df = reg_var(df)
    y = "wb_" + name
    if name == "ave":
        y = "u_"+name
        
    reg_result = mt.reg(df, y, X, fe_name = "school_code", cluster="hhid").summary.drop(index = controls)
    reg_result = reg_result.rename(columns= {'coeff' : name})[name]
    
    return reg_result