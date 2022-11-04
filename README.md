# Mass Balance Calculation
## INFOS

This repository stores the current avaiable mass balance algorithms for experimental petrology, with MCMC for propagating errors on phases and bulk compositions, including 

1) Non-negative least square algorithm
2) Matrix decomposition algorithm of [Li et al. (2020)](https://www.sciencedirect.com/science/article/pii/S0009281920300301?casa_token=frTdwy-tVF8AAAAA:z0pcHfcNB3LP4bGdEwWsgbzbauDBsoTKbbit5SnIiEH9htp6Y4zgRZjQttzSVGA34ZXiM-Sne45I). 
3) Algorithm of [Albarede and Provost (1977)](https://www.sciencedirect.com/science/article/pii/0098300477900073) (future update?)

Please contact me at yishen.zhang@kuleuven.be or drop `issue`,  `PR` for bug reporting or contribution

## HOW TO USE?

Before start, you may have to install python, from [Anaconda for Win](https://docs.anaconda.com/anaconda/install/windows/), [Anaconda for Mac](https://docs.anaconda.com/anaconda/install/mac-os/), or [Miniforge](https://github.com/conda-forge/miniforge).

To use, download the entire github files, you should have MassBalance and benchmark directories, 4 python scripts, 2 excel input files, 1 readme file and 1 tutorial notebook file.

**DO NOT** change the structure of the directory, as this code currently doesn't constain a setup file (will see if it's necessary to do). If you do, you will need relative import for the package.

Highly recommend to run through the tutorial notebook file, which gives general information of the code. Python scripts are also avaiable covering examples for different cases.

Three ways to run the scripts, see **PREPARATION** below for data preparation:

1) simply call python with the script name in your terminal, such as: ``python MCBatchBulk.py``

2) run through IDEs integrated with python (VS Code, Spyder. Etc)

3) use the jupyter notebook file


## LIBRARY REQUIREMENT

``numpy, pandas, scipy``

## PREPARATION

1. Load your phase compositions in the input excel files, different sheets store different phases, free to change sheet names and orders **BUT NOT** `bulk` and `run_index` sheets (they should always stay as the last two), `bulk` sheet saves the bulk composition(s), `run_index` saves the entire experimental run numbers ± expts conditions, sample numbers or rock ids for natural samples, which are then used for indexing and matching during calculation. 
2. If you only have one bulk composition, you can use `input_comp_oneBulk.xlsx`, or `input_comp.xlsx` but overwrite the bulk sheet.
3. **DO NOT** change column names.
4. **DO NOT** change the structure of the directory

## HOW TO CITE?

My paper using these methods is under review, but you may cite my [AGU abstract](https://ui.adsabs.harvard.edu/abs/2021AGUFM.V25C0119Z/abstract) as:

Zhang Y, Namur O, Charlier B, 2020. Experimental liquid lines of descent and Silicate Liquid Immiscibility for low-Ti and high-Ti basalts of the Emeishan Large Igneous Province, SW China. AGU Fall Meeting 2021.

Also need to cite the papers for these excellent algorithms:

For non-negative algorithm:

Lawson C., Hanson R.J., (1987) Solving Least Squares Problems, SIAM

For matrix decomposition:

Li, X., Zhang, C., Almeev, R.R. and Holtz, F., 2020. GeoBalance: An Excel VBA program for mass balance calculation in geosciences. *Geochemistry*, *80*(2), p.125629

Ghiorso, M.S., 1983. LSEQIEQ: A FORTRAN IV subroutine package for the analysis of multiple linear regression problems with possibly deficient pseudorank and linear equality and inequality constraints. *Computers & Geosciences*, *9*(3), pp.391-416.

