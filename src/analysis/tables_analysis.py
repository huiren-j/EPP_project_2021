import pandas as pd
import numpy as np
import econtools.metrics as mt
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from itertools import *
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import data_management.figures_management
import data_management.tables_management
import analysis.tables_analysis
import analysis.figures_analysis
import final.table_produce


def table1_reg(df, panel_list, columns):
    '''Produce descriptive table
    
    Args:
        df (dataframe)
        panel_list (list)
        columns (list)
    
    Returns:
        d (dataframe)
    '''

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

def table2_reg(df, y, x):
    '''Regression table
    Args:
        df (dataframe)
        y (string)
        x (string)
    Returns:
        result (dataframe)
    '''

    result = mt.reg(df, y, x , fe_name = "school_code", cluster="hhid").summary
    result = result2.drop(index = x[3:]).rename(columns= {"coeff" : y})
    result = result[y].to_frame()

    return result

def table3_reg(df, y):
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


def table4_reg_1(df, y, x):
    '''Regression for table4, PanelA

    Args:
        df (dataframe)
        y (string)
        x (list)
    Returns:
        result (Series)
    '''

    df["score_used"] = df[y]
    df["score_used_educ"] = df["score_used"]*df["educ_ave"]
    df["educ_used"] = df["educ_ave"]

    result = mt.reg(df, "b_"+y, x, fe_name = "school_code", addcons = True).summary
    result = result.rename(columns = {"coeff": y})[y]
    return result
    


def table4_reg_2(df, y, x):
    '''Regression result table

    Args:
        df (dataframe)
        name (string)
    Returns:
        result (dataframe)
    '''
    
    df = treat_dummy(df)
    df = reg_var(df)
    if y == "ave":
        y = "u_"+y

    else:
        y = "wb_" + y
        
    result = mt.reg(df, y, x, fe_name = "school_code", cluster="hhid").summary
    result = result.rename(columns= {'coeff' : y})[y]
    
    return result