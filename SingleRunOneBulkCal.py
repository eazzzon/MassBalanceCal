# import python modules
import pandas as pd
import matplotlib.pyplot as plt
from MassBalance.mb_tools import MassBalance  # this is the core object of the mb calculation

"""
Script for one single run, with one bulk composition given
"""

cmpnts = ['SiO2','Al2O3', 'TiO2', 'MgO', 'FeO', 'MnO',  'CaO', 'Na2O', 'K2O', 'P2O5', 'Cr2O3']  # change your desired elements for mass balance calculation

# loda data
nat_comp = pd.ExcelFile("input_comp_oneBulk.xlsx")
# prepare mb class
mb_cal = MassBalance(
    input_comp=nat_comp,
    comp_col=cmpnts,
    match_column="Run_no",
    bulk_sheet="bulk",
    index_sheet="run_index",
    normalize=True,
)
res_dict = mb_cal.compute(mc=None, exportFiles=True, batch_bulk=None, method='nnl')

print('Calculations complete!')
