import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import econtools.metrics as mt
import seaborn as sns

def figure_fill(subject, xlabel, ylabel, title, label1 = "x-axis:believed score", label2 =  "x-axis:true score" ):
    '''
    Common plot feature of figures
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
