import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import econtools.metrics as mt

def fig1_reg(df, name_list):
    '''This function is analysis to see investment on belief and
    belief on truth. Here, we will have a look at correlation with regression results'''

    correlation = df[name_list].corr(method = "pearson")
    
    coeff = []
    coeff1 = []
    
    for name in name_list:
        if name == "truth":
            result = mt.reg(df, "ic_"+name, "truth").summary.rename(columns = {"coeff": name} , index = {"truth": "inv on truth"})[name]
            coeff.append(result)
        else:
            result = mt.reg(df, "ic_"+name, "truth").summary.rename(columns = {"coeff": name} , index = {"truth": "inv on truth"})[name]
            result1 = mt.reg(df, "ic_"+name, name ).summary.rename(columns = {"coeff": name }, index = {name : "inv on belief"})[name]
            coeff.append(result)
            coeff1.append(result1)
    
    coeff = pd.concat(coeff, axis = 1)
    coeff1 = pd.concat(coeff1, axis = 1)
    return correlation, coeff, coeff1

#draw graph
def figure1(slope_b, slope_s):
    '''Draw line graphs

    Args:
        slope_b (float)
        slope_s (float)
    Returns:
        ax (matplotlib axies)
    
    ***axis labeling must be added***
    '''

    #slope_b= 0.3  #belief on trust
    #slope_s =1.3  #investment on belief
    
    intercept_b = 50*(1-slope_b)
    intercept_s = 75-slope_s*50

    slope_calc = slope_b*slope_s  
    intercept_calc = intercept_s+slope_s*intercept_b

    #panel(a)
    x = np.arange(0,100)
    y = slope_b * x + intercept_b 
    z = x

    plt.figure(figsize= (10,5))
    ax = plt.subplot(1,3,1)
    plt.axis([-10, 110, -10, 150])
    plt.plot(x,y)
    plt.plot(x,z)

    #panel(b)
    x_b = np.arange(0,100)
    y_b = slope_calc*x_b + intercept_calc
    #z_b = slope_s*x_b + intercept_s
    plt.subplot(132, sharex = ax, sharey = ax)
    plt.axis([-10, 110, -10, 150])
    plt.plot(x_b, y_b, ':', color = 'red')

    #ploc(c)
    x_c = np.arange(0,100)
    y_c = slope_s*x_c + intercept_s
    #z_c = slope_calc*x_c + intercept_calc
    plt.subplot(133, sharex = ax, sharey = ax)
    plt.axis([-10, 110, -10, 150])
    plt.plot(x_c, y_c, color = 'green')
    
    return ax

def fig2_bar(df, y):
    '''To generate bar plot based on regression

    Args: 
        df (dataframe)
        y  (string)
    Return:
        ax (matplotlib Axes)

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

    ax = sns.barplot(x = "group_id", y = "coeff", data = result)
    return ax



#2 : "b_ave", "u_ave"
#4 : "math", "engl"
def figure2_4(df_control, df_treat, subj):
    '''To draw graphs and fill in between them
    *axis labeling must be added
    Args:
        df_control (dataframe)
        df_treat (dataframe)
        sub (string)
    Return
        ax (matplotlib Axies)
    '''

    df_control["treat"] =0
    df_treat["treat"] =1
    df = pd.concat([df1,df2])
    
    df["mean"] = (df["lower"] + df["upper"]) / 2 
    
    x = df.loc[(df["subj"]==subj)&(df["treat"]==0), "x"]
    lb = df.loc[(df["subj"]==subj)&(df["treat"]==0), "lower"]
    ub = df.loc[(df["subj"]==subj)&(df["treat"]==0), "upper"]
    m = df.loc[(df["subj"]==subj)&(df["treat"]==0), "mean"]


    x2 = df.loc[(df["subj"]==subj)&(df["treat"]==1), "x"]
    lb2 = df.loc[(df["subj"]==subj)&(df["treat"]==1), "lower"]
    ub2 = df.loc[(df["subj"]==subj)&(df["treat"]==1), "upper"]
    m2 = df.loc[(df["subj"]==subj)&(df["treat"]==1), "mean"]

    fig, ax = plt.subplots()
    ax.plot(x, lb, color = "gray")
    ax.plot(x, ub, color = "gray")
    ax.fill_between(x,lb,ub, color="xkcd:light gray")
    ax.plot(x, m, ":", color = "green")
    

    ax.plot(x2, lb2, color = "gray")
    ax.plot(x2, ub2, color = "gray")
    ax.fill_between(x2,lb2,ub2, color="xkcd:gray")
    ax.plot(x2, m2, color = "blue")
    
    return ax