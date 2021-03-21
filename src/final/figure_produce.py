import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import econtools.metrics as mt
import seaborn as sns
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import data_management.figures_management
import data_management.tables_management
import analysis.tables_analysis
import analysis.figures_analysis
import final.table_produce

def figure_fill(subject, xlabel, ylabel, title, label1 = "x-axis:believed score", label2 =  "x-axis:true score" ):
    '''
    a common function in plotting each figures
    Args:
        subject (list)
        xlabel (string)
        ylabel (string)
        title (string)
    Returns:
        fig (figure)
    '''
    fig, ax= plt.subplots()
    i = 0
    for x in subject:
        ax.plot(x[0], x[1])
        ax.plot(x[0], x[2])
        ax.fill_between(x[0], x[1],x[2], color="xkcd:light gray")
        if i == 0:
            ax.plot(x[0], x[3], "-", label = label1)
            i = i+1
        else:
            ax.plot(x[0], x[3],":" ,label = label2)
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
        
    return fig


def figure1(slope_b, slope_s):
    '''Draw linear graphs about beliefs, trust and investment
    Args:
        slope_b (float)
        slope_S (float)
    Returns:
        fig (figure)
    '''
    
    intercept_b = 50*(1-slope_b)
    intercept_s = 75-slope_s*50

    slope_calc = slope_b*slope_s  
    intercept_calc = intercept_s+slope_s*intercept_b
    
    ran = [-10, 110, -10, 150]

    #panel(a)
    x = np.arange(0,100)
    y = slope_b * x + intercept_b 
    z = x

    fig = plt.figure(figsize= (20,5))
    ax = plt.subplot(1,3,1)
    plt.axis(ran)
    plt.plot(x,y)
    plt.plot(x,z)
    plt.title("PanelA. Beliefs maybe \ninaccurate on true performance", loc = 'left')

    #panel(b)
    x_b = np.arange(0,100)
    y_b = slope_calc*x_b + intercept_calc
    plt.subplot(132, sharex = ax, sharey = ax)
    plt.axis(ran)
    plt.plot(x_b, y_b, ':', color = 'red')
    plt.title("PanelB. Parents choose their investments \nbased on their (inaccurate)beliefs", loc = 'left')

    #ploc(c)
    x_c = np.arange(0,100)
    y_c = slope_s*x_c + intercept_s
    plt.subplot(133, sharex = ax, sharey = ax)
    plt.axis(ran)
    plt.plot(x_c, y_c, color = 'green')
    plt.title("PanelC. The slope of investments on true \nperformance may thus be attenuated relative \nto the slope on beliefs", loc = 'left')
    
    return fig


def figure2_AB(df_reg, x = None, y = "Absolute value \n (true scoore - baseline beliefs)", t = "PanelA. Gap between true test scores last term \n and baseline beliefs about last term"):
    '''
    Barplot comparing difference in belief values between control and treat group
    
    Args:
        df_reg (dataframe)
        x,y,t (strings)
    Returns:
        fig (figure)
    '''

    fig = sns.barplot(x = "group_id", y = "coeff", data = df_reg)
    fig.set(xlabel = x, ylabel= y, title = t)
    fig = fig.get_figure()
    return fig

