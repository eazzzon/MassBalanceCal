.. MassBalanceCal documentation master file, created by
   sphinx-quickstart on Mon Nov  7 10:18:10 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to MassBalanceCal's documentation!
==========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   about
   data preparation
   tutorials
   license

INSTALLATION & USE
##################
1. No pip or conda installation is planned, you can install by calling the ``setup.py`` file in the unzipped downloaded file (directory name supposedly as MassBalanceCal-main). Run the line below in any terminal like app (terminal in Mac, or Anaconda prompt in Win):

.. code-block:: python

   pip install .

or quicker install from the lastest github release (v0.1.7) as:

.. code-block:: python

   pip install git+https://github.com/eazzzon/MassBalanceCal.git@v0.1.7


2. If you don't want to install the module, you can still either run the scripts/notebook file within the example directory, or relative import the module as:

.. code-block:: python

   sys.path.append(filepath of massbalance folder in your system)

3. Uninstallatiion as:

.. code-block:: python

   pip uninstall massbalance

DATA PREPARATION
##################

1. Load your phase compositions in the ``input excel files``, use sheets store different phases, free to change sheet names and orders **BUT NOT** ``bulk`` and ``run_index`` sheets (they should always stay as the last two), ``bulk`` sheet should give the bulk composition(s), ``run_index`` should give the entire experimental run numbers ± expts conditions, sample numbers or rock ids for natural samples, which are then used for indexing and matching during calculation.

2. If you only have one bulk composition, you can use `input_comp_oneBulk.xlsx`, or `input_comp.xlsx` but overwrite the bulk sheet.

3. If you change the element in the header, you should also change the definition of element list in the script for consistency.

4. If you didn't install the module, **DO NOT** change the structure of the directory.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
