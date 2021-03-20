import pandas as pd
import numpy as np
import econtools.metrics as mt
from itertools import *
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import data_management.figures_management
import data_management.tables_management
import analysis.tables_analysis
import analysis.figures_analysis




def table1(df, **kwargs):
    '''To make a complete table1

    Args:
        df  (dataframe)
        kwargs (lists)
    Returns:
        result (dataframe)
    '''
    df = treat_dummy(df)
    df = table1_1(df1, "d_ave", ["overconf_ave","underestimate_ave"])
    
    varlist = ["exp_fees", "exp_uniforms", "exp_text", "exp_exbks", "exp_bks", "exp_tutoring", "exp_backpack", "exp_bks", "exp_exbks", "exp_text", "tot_bks_text", "tot_bks_all", "any_bks_text", "any_bks_all", "any_bks_text_s5", "any_bks_all_s5", "any_tutoring", "any_bks_text_tut", "any_exbks"]
    df = table1_3(df, varlist)

    columns = [("Full Sample", "Mean"), ("Full Sample", "SD"), ("Control", "Mean"), ("Treat", "Mean"), ("Treat - Control","Mean")
          , ("Treat - Control","SE"), ("Treat - Control", "p-val T=C")]
    columns = pd.MultiIndex.from_tuples(columns)

    def table1_(**kwargs):
        '''To collcect variables for each panel in separate list
        Args:
            args (list)
        Return:
            panel_list (list)
        '''

        panel_list = []
        for values in kwargs:
            panel_list.append(values)
        return panel_list
    
    panel_list = table1_(**kwargs)
    result = table1_reg(df, panel_list, columns)
    return result


def table2(df_list, y_list, x_list):
    '''To make a complete table2

    Args:
        df_list (list)
        y_list (list)
        x_list (list)
    Returns:
        table (dataframe)
    '''

    result = {}
    for i in range(len(df_list)):
        df = pd.read_csv("../src/original_data/"+df_list[i]+".dta")

        df = treat_dummy(df)
        df = col_names(df, x[i])
        df, X = reg_var(df)

        result["column{0}".format(i)] = table2_reg(df,y[i],X)
    
    table = pd.concat(result, axis = 1)

    return table


def table4_PanelA(df, type_list):
    '''To make a complete table4

    Args:
        df (dataframe)
        type_list (list)
    Returns:
        PanelA (dataframe)
    '''
    df = treat_dummy(df)

    panel_A = []
    x = ["score_used_educ", "score_used", "educ_used"]
    
    for y in type_list:
        result.table4_reg_1(df,y,x)
        panel_A.append(result)

    panel_A = pd.concat(panel_A, axis = 1)
    return panel_A


def table4_PanelB(df, type_list):
    '''To make a complete table4, panelB

    Args:
        df (dataframe)
        type_list (list)
    Returns:
        panel_B (dataframe)
    '''

    df = treat_dummy(df)
    df, X = reg_var(df)
    df = col_names(df)

    X.remove("std_2")
    X.remove("perf_gap_used_1")
    X.remove("C1_strat_0")

    panel_B = []
    for y in type_list:
        result = table4_reg_2(df, y, X)
        panel_B.append(result)
    
    panel_B = pd.concat(panel_B, axis = 1)
    return panel_B
    



