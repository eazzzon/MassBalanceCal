# Mass Balance Calculation for Petrology
## INFORMATION

This repository stores mass balance algorithms for petrology in general, with MCMC for propagating errors on phases and bulk compositions, including: 

1) Non-negative least square algorithm
2) Matrix decomposition algorithm of [Li et al. (2020)](https://www.sciencedirect.com/science/article/pii/S0009281920300301?casa_token=frTdwy-tVF8AAAAA:z0pcHfcNB3LP4bGdEwWsgbzbauDBsoTKbbit5SnIiEH9htp6Y4zgRZjQttzSVGA34ZXiM-Sne45I). 
3) Algorithm of [Albarede and Provost (1977)](https://www.sciencedirect.com/science/article/pii/0098300477900073) (future update?)

Please contact me at yishen.zhang@kuleuven.be or drop `issue`,  `PR` for bug reporting, new feature requirement or contribution.

## INSTALLATION & USE

1. [Download](https://github.com/eazzzon/MassBalanceCal/releases/tag/v0.1) or clone the github files, compile python environment  from [Anaconda for Win](https://docs.anaconda.com/anaconda/install/windows/), [Anaconda for Mac](https://docs.anaconda.com/anaconda/install/mac-os/), or [Miniforge](https://github.com/conda-forge/miniforge).

2. Currently not plan to have a pip or conda installation, you can install by calling the `setup.py` file in the **unzipped downloaded file** (directory name supposedly as MassBalanceCal-main) from terminal like app (terminal in Mac, or Anaconda prompt in Win):

   ```python
   pip install .
   ```

3. If you don't want to install the module, you can still either run the scripts or notebook file within the example directory, or relative import the module before use:

   ```python
   sys.path.append(filepath of massbalance folder in your system)
   ```

4. To do the calculation, simply run the scripts or notebook file from IDEs (VS code, Spyder, Jupyterlab/Jupyter notebook). See **PREPARATION** first for data preparation.

5. Highly recommend to look through the tutorial notebook file (in the Tutorial directory), which gives general information of the code. Python scripts (example directory) are also avaiable covering examples for different cases.

6. Uninstallation as:

   ```python
   pip uninstall massbalance
   ```


## LIBRARY REQUIREMENT

``numpy, pandas, scipy``

## PREPARATION

1. Load your phase compositions in the **input excel files**, use sheets store different phases, free to change sheet names and orders **BUT NOT** `bulk` and `run_index` sheets (they should always stay as the last two), `bulk` sheet should give the bulk composition(s), `run_index` should give the entire experimental run numbers ± expts conditions, sample numbers or rock ids for natural samples, which are then used for indexing and matching during calculation. 
2. If you only have one bulk composition, you can use `input_comp_oneBulk.xlsx`, or `input_comp.xlsx` but overwrite the bulk sheet.
3. **DO NOT** change column names if not necessary.
4. If you didn't install the module, **DO NOT** change the structure of the directory.

## HOW TO CITE?

My paper using these methods is under review, but you may cite my [AGU abstract](https://ui.adsabs.harvard.edu/abs/2021AGUFM.V25C0119Z/abstract) as:

-- Zhang Y, Namur O, Charlier B, 2020. Experimental liquid lines of descent and Silicate Liquid Immiscibility for low-Ti and high-Ti basalts of the Emeishan Large Igneous Province, SW China. AGU Fall Meeting 2021.

Also need to cite the papers for these excellent algorithms:

For non-negative algorithm:

-- Lawson C., Hanson R.J., (1987) Solving Least Squares Problems, SIAM

For matrix decomposition:

-- Li, X., Zhang, C., Almeev, R.R. and Holtz, F., 2020. GeoBalance: An Excel VBA program for mass balance calculation in geosciences. *Geochemistry*, *80*(2), p.125629

-- Ghiorso, M.S., 1983. LSEQIEQ: A FORTRAN IV subroutine package for the analysis of multiple linear regression problems with possibly deficient pseudorank and linear equality and inequality constraints. *Computers & Geosciences*, *9*(3), pp.391-416.

