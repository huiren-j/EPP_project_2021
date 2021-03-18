import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import econtools.metrics as mt

def bound_function(df, condition):
    '''
    repeated frame for several figures in common
    Args:
        df (dataframe)
        condition (series)
    Returns:
        out (list)
    '''
    x = df.loc[condition, "x"]
    lb = df.loc[condition, "lower"]
    ub = df.loc[condition, "upper"]
    m = df.loc[condition, "mean"]
    
    out = [x,lb,ub,m]
    
    return out


def figure1_reg(df, name_list):
    '''Calculate correlation and run regression between investment and trust & beliefs
    
    Args:
        df (dataframe)
        name_list (list)
    Return:
        correlation (dataframe)
        coeff (dataframe)
        coeff1 (dataframe)
    '''
    correlation = df[name_list].corr(method = "pearson")
    
    coeff = []
    coeff1 = []
    
    for name in name_list:
        if name == "truth":
            result = mt.reg(df, "ic_"+name, "truth").summary.rename(columns = {"coeff": name} , index = {"truth": "inv on truth"})[name]
            coeff.append(result)
        else:
            result = mt.reg(df, "ic_"+name, "truth").summary.rename(columns = {"coeff": name} , index = {"truth": "inv_b on truth"})[name]
            coeff.append(result)
            
            if name == 'beliefs1':
                continue
            
            else:
                result1 = mt.reg(df, "ic_"+name, name ).summary.rename(columns = {"coeff": name }, index = {name : "inv on belief"})[name]
                coeff1.append(result1)
    
    coeff = pd.concat(coeff, axis = 1)
    coeff1 = pd.concat(coeff1, axis = 1)
    return correlation, coeff, coeff1



def figure2_AB_1(df, y):
    '''
    Run regression to see the gap in the effect of treatment on beliefs
    and produce regression result dataframe

    Args:
        df (dataframe)
        y (string)
    Returns:
        result (dataframe)
    '''
    result = mt.reg(df,y,'treat',addcons = True ,cluster = "hhid").summary
    result = result[['coeff','CI_high','CI_low']]
    result = result.rename({"_cons": "control"}, axis = 'index')

    stat = result.columns.tolist()
    constant = result.iloc[1,0]

    for s in stat:
        result.loc["treat", s] = result.loc["treat", s] + constant

    result["coeff"] = result["coeff"].round(1)
    result["group_id"] = result.index
    
    return result


def figure2_BD_1(df_control, df_treat, subj):
    '''calcaulate changes in belief due to treatment by subjects
    *figure4_A has same framework

    Args:
        df_control (dataframe)
        df_treat (dataframe)
        subj (string)
    Returns:
        result (list)
    '''
    df_control["treat"] =0
    df_treat["treat"] =1
    df = pd.concat([df1,df2])
    
    df["mean"] = (df["lower"] + df["upper"]) / 2 
    
    def figure2_BD_2(i):
        '''An input of map(), save series extracted by groups of treat and control as list

        Args:
            i (int)
        Return:
            out (list)
        '''

        nonlocal df
        cond = (df["subj"]==subj)&(df["treat"]==i)
        out = bound_function(df, cond)
        return out
    
    result = list(map(figure2_BD_2, [0,1]))
    return result



def figure3_A_1(df, subj):
    ''' Prepare data to plot
    Args:
        df (dataframe)
        subj (string)
    Return:
        result (list)
    '''

    df["mean"] = (df["lower"] + df["upper"]) / 2 
    
    a = (df["subj"]==subj)
    b = (df["subj"]=="b_" + subj)
    
    def figure3_A_2(cond):
        '''
        An input for map()
        Args:
            cond (Series)
        Returns:
            out (list)
        '''

        nonlocal df
        out = bound_function(df, cond)
        return out
    
    condition = [a,b]
    result =  list(map(figure4_A_2,condition))
        
    return result


#figure3_B separate
def figure3_B_1(df, subj):
    '''
    Args:
        df (dataframe)
        subj (list)
    
    Returns:
        ax (matplotlib axies)
    '''
    
    df["mean"] = (df["lower"] + df["upper"]) / 2 
    
    def figure3_B_2(sub):
        '''
        input for map function
        Args:
            sub (string)
        Returns:
            out (list)
        '''
        nonlocal df
        condition = (df["subj"]==sub)&(df["x"]>=df["lb"])&(df["x"]<=df["ub"])
        
        out = bound_function(df, condition)
        return out

    result = list(map(figure3_B_2,subj))
    return result

