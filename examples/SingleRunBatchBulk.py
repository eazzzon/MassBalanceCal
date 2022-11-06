# import python modules
import pandas as pd
import matplotlib.pyplot as plt
import os, sys
if not os.path.exists('massbalance') and os.path.exists('../massbalance'):    # hack to allow scripts to be placed in subdirectories next to pyAp
    sys.path.insert(1, os.path.abspath('..'))
from massbalance.mb_tools import MassBalance  # this is the core class of the mb calculation
"""
Script for one single run, with batch bulk compositions given
"""

cmpnts = ['SiO2','Al2O3', 'TiO2', 'MgO', 'FeO', 'MnO',  'CaO', 'Na2O', 'K2O', 'P2O5', 'Cr2O3']  # change your desired elements for mass balance calculation

# loda data
nat_comp = pd.ExcelFile("input_comp.xlsx")
# prepare mb class
mb_cal = MassBalance(
    input_comp=nat_comp,
    comp_col=cmpnts,
    match_column="Run_no",
    bulk_sheet="bulk",
    index_sheet="run_index",
    normalize=True,
)
res_dict = mb_cal.compute(mc=None, exportFiles=True, batch_bulk=True, method='nnl')

print('Calculations complete!')
