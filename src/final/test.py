import pandas as pd
import numpy as np
import econtools.metrics as mt
from itertools import *
from pandas.testing import assert_frame_equal
from pandas.testing import assert_series_equal
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import data_management.figures_management
import data_management.tables_management
import analysis.tables_analysis
import analysis.figures_analysis
import table_produce


def create_inputs():
    df = pd.read_stata("../src/original_data/Ability_Clean_2.dta")
    panelA = ["tot_kids", "one_par", "educ_ave", "any_secondary"]
    type_list = ["ave","math", "engl", "chich", "math_engl", "ave_12"]
    return df, panelA, type_list

def test_table1():
    df, panelA, type_list = create_inputs()
    
    columns = [("Full Sample", "Mean"),("Full Sample", "SD")]
    columns = pd.MultiIndex.from_tuple(columns)
    expected_table1 = pd.DataFrame({("Full Sample", "Mean"): [5.13, 0.19, 4.66, 0.18], ("Full Sample", "SD"): [1.74, 0.39, 3.25, 0.38]})
    calc_table1 = table1(df, panelA)
    assert_series_equal(calc_table1[("Full Sample", "Mean")], expected_table1[("Full Sample", "Mean")])


def test_table4():
    df, panelA, type_list = create_inputs()
    expected_table4A = pd.DataFrame(data =[
        [0.014888, 0.017410, 0.013885, 0.010363, 0.012622, 0.017846],
        [0.262965, 0.129024, 0.226430, 0.212143, 0.083819, 0.314682],
        [-0.434949, -0.831751, -0.046859, -0.234546, -0.661042, 0.096866]
    ], columns = ["ave", "math", "engl", "chich", "math_engl", "ave_12"],
    index = ["score_used_educ", "score_used", "educ_used"])
    calc_table4A = table4_PanelA(df, type_list)
    assert_frame_equal(calc_table4A, expected_table4A)




