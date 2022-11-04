# import python modules
import pandas as pd
import matplotlib.pyplot as plt
import os
if not os.path.exists('MassBalance') and os.path.exists('../MassBalance'):    # hack to allow scripts to be placed in subdirectories next to pyAp
    sys.path.insert(1, os.path.abspath('..'))
from MassBalance.mb_tools import MassBalance  # this is the core class of the mb calculation
"""
Script to run MC, with one bulk composition given
"""

#=======================
cmpnts = ['SiO2','Al2O3', 'TiO2', 'MgO', 'FeO', 'MnO',  'CaO', 'Na2O', 'K2O', 'P2O5', 'Cr2O3']  # change your desired elements for mass balance calculation
cmpnts_std =[x + '_std' for x in cmpnts]  # save columns for stdcmpnts_std =[x + '_std' for x in cmpnts]  # save columns for stdcmpnts_std =[x + '_std' for x in cmpnts]  # save columns for std
# loda data
nat_comp = pd.ExcelFile("input_comp_oneBulk.xlsx")
# prepare mb class
mb_cal = MassBalance(
    input_comp=nat_comp,
    comp_col=cmpnts,
    comp_std_col=cmpnts_std,
    match_column="Run_no",
    bulk_sheet="bulk",
    index_sheet="run_index",
    normalize=True,
)
res_dict = mb_cal.compute(mc=100, exportFiles=True, batch_bulk=None, method='nnl')

print('Calculations complete!')

for key in res_dict:
    fig, axes = plt.subplots(constrained_layout=True)
    axes.hist(res_dict[key]['gl'])  # plot glass data, change to your desired phases
    plt.savefig('MCOneBulk'+str(key)+'_gl.pdf', dpi=300)
    # plt.show()
