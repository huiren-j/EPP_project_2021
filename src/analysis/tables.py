import pandas as pd
import numpy as np
import econtools.metrics as mt
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from itertools import *
from functions import *
#panelA
def tab4_PanelA(df, type_list)
    '''
    This function generates table4 panelA. The parameters are dataset and 
    types of scores.
    '''
    #type_list = ["ave","math", "engl", "chich", "math_engl", "ave_12"]
    
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
    '''
    This function is generating control variables for table4 analysis.
    Parameters required are dataset and score(name) you want to conduct analysis
    '''

    def control(ctrl):
        dummies = []
        nonlocal df
        ctrl_val  = df[ctrl].value_counts().keys().sort_values()
        for i in ctrl_val:
            dummies.append(ctrl+"_"+str(i))
        return dummies
    
    ctrl_col = ["std","perf_gap_used","C1_strat"]
    controls = list(map(control,ctrl_col))
    controls = list(chain.from_iterable(controls))
    controls = controls + ["female_reg", "female_miss", "primary_resp_fem"]
    
    controls.remove("std_2")
    controls.remove("perf_gap_used_1")
    controls.remove("C1_strat_0")
    
    X = ["treat_perf","treat_perf_educ", "treat", "treat_educ_used", "perf_", "perf_educ", "educ_ave"] + controls
    
    df = pd.get_dummies(df,columns = ctrl_col)
    y = "wb_" + name
    if name == "ave":
        y = "u_"+name
        
    reg_result = mt.reg(df, y, X, fe_name = "school_code", cluster="hhid").summary.drop(index = controls)
    reg_result = reg_result.rename(columns= {'coeff' : name})[name]
    
    return reg_result