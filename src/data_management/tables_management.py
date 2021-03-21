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
import analysis.tables_analysis
import analysis.figures_analysis
import final.table_produce

def treat_dummy(df):
    '''Convert string type categorical variable to dummy variable
    
    Args:
        df (dataframe)
    Returns:
        df (dataframe)
    '''

    df = pd.get_dummies(df,columns=["treat"])
    df["treat"] = df["treat_Treatment"]
    df = df.drop(columns=["treat_Control"])
    df = df.drop(columns=["treat_Treatment"])
    
    return df


def neg(df, sub, prefix = ""):
    '''Converting a variable to negative value.
    
    Args:
        df (dataframe)
        sub (string)
        prefix (list)
    
    Returns:
        df (dataframe)
    '''
    
    for i in prefix:
        if i == "":
            df[sub] = -df[sub]
        else:
            df[i+sub] = -df[i+sub]
    return df


def col_names(df, name):
    '''Repeated framework calculating new variables for regression 
    Args:
        df (dataframe)
        name (string)
    Returns:
        df (dataframe)
    '''

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

def reg_var(df):
    '''Get dummy variables for regression and define control variables names

    Args:
        df (dataframe)
    Returns:
        df (dataframe)
        X (list)
    '''

    def control(ctrl):
        '''input for map()
        generate dummy variables name list

        Arg:
            ctrl (string)
        return:
            dummies (list)
        '''

        dummies = []
        nonlocal df
        ctrl_val  = df[ctrl].value_counts().keys().sort_values()
        for i in ctrl_val:
            dummies.append(ctrl+"_"+str(i))
        return dummies
    
    ctrl_col = ["std","perf_gap_used","C1_strat"]
    result = list(map(control,ctrl_col))
    result = list(chain.from_iterable(result))
    
    X = ["treat_perf", "treat", "perf_", "educ_ave_reg", "educ_ave_miss", "female_reg", "female_miss", "primary_resp_fem"] + result
    
    df = pd.get_dummies(df,columns = ctrl_col)
    
    return df, X


def table1_1(df, cond, subject):
    '''Allocate values under certain condtions in dataframe to certain values

    Arg:
        df (dataframe)
        cond (string)
        subject (list)
    Return:
        df (dataframe)
    '''

    def table1_2(subj):
        '''input of map()

        Arg: 
            subj (string)
        Return:
            df (dataframe)
        '''
        nonlocal df
        df.loc[(df[cond].isnull()==False) & (df[cond]>0),subj] = 1
    
        return df
    
    df = list(map(tab1_var_iter,subject))
    df = pd.concat(df).drop_duplicates()
    return df
    

def tabable1_3(df, varlist):
    '''Change negative values to NaN

    Args:
        df (dataframe)
        varlist (list)
    Return:
        df (dataframe)
    '''
    
    def table1_4(var):
        '''input of map()
        Arg:
            var (string)
        Return:
            df (dataframe)
        '''

        nonlocal df
        df.loc[(df[var]<0), var] = np.nan
        return df
    
    df = list(map(tab1_npn_iter, varlist))
    df = pd.concat(df).drop_duplicates()
    return df

def table1_max(df, subj, group):
    '''Taking max value by group
    Args:
        df (dataframe)
        subj (string)
        group (string)

    Returns:
        df (dataframe)
    '''
    
    df[subj] = df.groupby([group])[subj].transform(max)
    return df

def table3_var(df):
    '''Produce dummy variables and get variables' names

    Args:  
        df (dataframe)
    Returns:
        df (dataframe)
        ctrl_list (list)
    '''
    def control(ctrl):
        '''input of map
        Save dummy variables' names

        Args:
            ctrl (string)
        Returns:
            dummies (list)
        '''

        dummies = []
        nonlocal df
        ctrl_val  = df[ctrl].value_counts().keys().sort_values()
        for i in ctrl_val:
            dummies.append(ctrl+"_"+str(i))
        return dummies
    
    ctrl_col = ["std","perf_gap_used","C1_strat"]
    ctrl_list = list(map(control,ctrl_col))
    ctrl_list = list(chain.from_iterable(ctrl_list))
    df = pd.get_dummies(df,columns = ctrl_col)
    
    return df, ctrl_list



