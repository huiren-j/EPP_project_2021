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
    '''This is plotting figure1 which is about investment on belief and
    relationship between belief and true value of children's academic ability'''

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
    
    return plt.show()