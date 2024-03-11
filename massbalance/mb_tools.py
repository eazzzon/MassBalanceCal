# Yishen Zhang 06 NOV. 2022

from scipy.optimize import nnls
import pandas as pd
import numpy as np
from numpy.linalg import svd


def _norm_phases(comp_df, comp_col):
    """
    Normalization for compositional dataframe
    """
    norm_df = (
        100
        * comp_df[comp_col]
        .fillna(0)
        .div(comp_df[comp_col].fillna(0).sum(axis=1), axis=0)
        .fillna(0)
        .copy()
    )
    return norm_df


def _dict_mass_balance(
    exp_dict,
    comp_col,
    comp_std_col,
    massBalance_phase,
    match_index,
    match_column,
    normalize=True,
):
    """
    Method to parse pandas.ExcelFile into compositions and stds dictionary

    """

    exp_mb_dict = {}  # collect normalized, matched expts phases
    exp_mb_std = {}  # collect matched expts phases std

    for idx, val in enumerate(massBalance_phase):
        match_phase = match_index.merge(exp_dict[val], on=match_column, how="left")
        if normalize:
            norm_phase = _norm_phases(match_phase, comp_col)
            exp_mb_dict[val] = norm_phase
            if comp_std_col:
                exp_mb_std[val] = match_phase[comp_std_col].fillna(0)
            else:
                pass
        else:
            exp_mb_dict[val] = match_phase[comp_col].fillna(0)
            if comp_std_col:
                exp_mb_std[val] = match_phase[comp_std_col].fillna(0)
            else:
                pass
    return exp_mb_dict, exp_mb_std


def _svd_mb(phase, bulk):
    """
    svd solve for matrix
    """
    list_idx = [
        idx for idx, x in enumerate(phase) if x.sum() > 0
    ]  # remove empty matrix, thus no phase composition
    a_matrix = [phase[i] for i in list_idx]  # index to existing phases
    A_matrix = np.array(
        a_matrix
    ).T.tolist()  #  convert the matrix to row as chemical oxides, col as phases
    u, sigma, v = svd(A_matrix)  # svd, decomposite the matrix to u, sigma and v
    sigma_reciprocal = (
        1 / sigma[sigma != 0]
    )  # take repciprocal of all non-zero elements in sigma,
    sigma_fill = np.zeros(
        (np.shape(A_matrix)[1], np.shape(A_matrix)[0])
    )  # create a sigma_plus with a n * m dimension (A_matrix in m*n)
    np.fill_diagonal(
        sigma_fill, sigma_reciprocal, wrap=True
    )  # fill the diagonal of sigma_fill with reciprocal results
    a_matrix_plus = v.T.dot(
        sigma_fill.dot(u.T)
    )  # compute the pseudoinverse of matrix A
    res = a_matrix_plus.dot(bulk)  # calculate proportions
    empt_arr = np.zeros(
        len(phase)
    )  # create empty list with the same dimension as the number of phases
    empt_arr[list_idx] = res  # index the existing phase back to origin position
    return empt_arr


def _exportFiles(restore_dict, filename = 'output'):
    """
    export files to xlsx
    """
    # save results in output.xlsx, each sheet represents the results for each expt run, each run will have mc times mb calculation
    writer = pd.ExcelWriter(filename+".xlsx")
    for key in restore_dict:
        restore_dict[key].to_excel(writer, sheet_name=str(key))
    writer.close()

    writer = pd.ExcelWriter(filename+"_mean_median_std.xlsx")
    for key in restore_dict:
        restore_dict[key].agg(["mean", "median", "std"]).to_excel(
            writer, sheet_name=str(key)
        )
    writer.close()


class MassBalance:
    """
    Class to perfrom mass balance calculation.

    Paramters:
    ---------------------
    input_comp : :class:`pandas.ExcelFile`
        input pandas ExcelFile

    comp_col : :class:`list`
        element list of composition

    comp_std_col : :class:`list`
        element std list of composition

    match_column : :class:`string`
        Column saves your expts run no., sample id, or rock id.

    bulk_sheet :class:`string`
        sheet name of your bulk composition(s)

    index_sheet :class:`string`
        sheet name of your entire expts info, or sample id info, this should cover all run no. sample id in your calculation

    normalize : :class:`boolean`
        choose if you want to normalize your data to 100 before mass balance calculation
    """

    def __init__(
        self,
        input_comp,
        comp_col,
        comp_std_col=None,
        match_column="Run_no",
        bulk_sheet="bulk",
        index_sheet="run_index",
        normalize=True,
    ):
        self.exp_dict = (
            {}
        )  # crate dictionary to collect compositions of different phases
        self.phases = (
            []
        )  # create list to save all phases in the calculation. Note bulk will be the bulk compsition, run_index will be your sample number, or rock id . etc
        for sheet_name in input_comp.sheet_names:
            self.phases.append(sheet_name)
            self.exp_dict[sheet_name] = input_comp.parse(sheet_name)
        self.bulk_comp = self.exp_dict[bulk_sheet]  # keep your bulk composition here
        self.match_index = self.exp_dict[
            index_sheet
        ]  # keep your sample index here, will be used for matching expts runs later
        self.match_column = match_column
        self.massBalance_phase = self.phases[
            :-2
        ]  # this keep all expts phase you have, by excluding bulk and run index
        self.comp_col = comp_col
        self.comp_std_col = comp_std_col
        self.exp_mb_dict, self.exp_mb_std = _dict_mass_balance(
            self.exp_dict,
            self.comp_col,
            self.comp_std_col,
            self.massBalance_phase,
            self.match_index,
            self.match_column,
            normalize=normalize,
        )

    def compute(self, mc=None, exportFiles=True, filename='output', batch_bulk=True, method="nnl"):
        """
        Non-negative algrithom for mass balance calculation.

        Parameters:
        ---------------------
        mc : :class:`float, int`
            Monte Carlo calculation numbers, default is None
        exportFiles: :class:`boolean`
            Choose if you would like to export results in excel files
        batch_bulk: :class:`boolean`
            Define if you have a batch bulk composition you want to match, or single one bulk comp, default is True
        method : :class:`string
            Use 'nnl' as non-negative algrithom, 'svd' for matrix decomposition.


        Returns:
        ---------------------
        res_dict: :class:`dictionary`
            Dictionary stores mass balance results, each key saves each run no., sample id or rock id.
        """


        prop_array = []  # collect phase proportions for all mc runs
        prop_r2 = (
            []
        )  # collect r2 for all mc runs, note r2**2, which is the normalized r2 is the residuals
        run_numbers = len(self.match_index)  # save your run numbers
        res_dict = {}
        restore_dict = {}
        if (method != "nnl") and (method != "svd"):
            print('Wrong method string, should be either "nnl" or "svd"')
        if method == "nnl":
            if mc:
                for num in range(mc):
                    phases_matrix = (
                        []
                    )  # collect phase matrix for mass balance calculation
                    for i in range(run_numbers):
                        phase_mb = []  # collect phase array in each iteration
                        for idx, phase in enumerate(self.massBalance_phase):
                            exp_std = (
                                np.random.normal(0, 1, len(self.comp_std_col))
                                * self.exp_mb_std[phase].iloc[i].values
                            )
                            phase_mb.append(
                                self.exp_mb_dict[phase].iloc[i].values + exp_std,
                            )
                        phases_matrix.append(phase_mb)
                    phase_prop = []  # collect phase proportions in each mc iteration
                    phase_prop_r = []  # collect r2 in each mc iteration
                    if batch_bulk:
                        for i in range(len(phases_matrix)):
                            bulk_std = (
                                np.random.normal(0, 1, len(self.comp_std_col))
                                * self.bulk_comp[self.comp_std_col].iloc[i]
                            )
                            phase_prop_iter, phase_prop_iter_r = nnls(
                                np.array(phases_matrix[i]).T,
                                bulk_std.values
                                + self.bulk_comp[self.comp_col].iloc[i].values,
                            )
                            phase_prop.append(phase_prop_iter)
                            phase_prop_r.append(phase_prop_iter_r)
                        prop_array.append(phase_prop)
                        prop_r2.append(phase_prop_r)
                    else:
                        for i in range(len(phases_matrix)):
                            bulk_std = (
                                np.random.normal(0, 1, len(self.comp_std_col))
                                * self.bulk_comp[self.comp_std_col].values[0]
                            )
                            phase_prop_iter, phase_prop_iter_r = nnls(
                                np.array(phases_matrix[i]).T,
                                bulk_std + self.bulk_comp[self.comp_col].values[0],
                            )
                            phase_prop.append(phase_prop_iter)
                            phase_prop_r.append(phase_prop_iter_r)
                        prop_array.append(phase_prop)
                        prop_r2.append(phase_prop_r)
            else:
                phases_matrix = []  # collect phase matrix for mass balance calculation
                for i in range(run_numbers):
                    phase_mb = []  # collect phase array in each iteration
                    for idx, phase in enumerate(self.massBalance_phase):

                        phase_mb.append(
                            self.exp_mb_dict[phase].iloc[i].values,
                        )
                    phases_matrix.append(phase_mb)
                phase_prop = []  # collect phase proportions in each mc iteration
                phase_prop_r = []  # collect r2 in each mc iteration
                if batch_bulk:
                    for i in range(len(phases_matrix)):
                        phase_prop_iter, phase_prop_iter_r = nnls(
                            np.array(phases_matrix[i]).T,
                            self.bulk_comp[self.comp_col].iloc[i].values,
                        )
                        phase_prop.append(phase_prop_iter)
                        phase_prop_r.append(phase_prop_iter_r)
                    prop_array.append(phase_prop)
                    prop_r2.append(phase_prop_r)
                else:
                    for i in range(len(phases_matrix)):
                        phase_prop_iter, phase_prop_iter_r = nnls(
                            np.array(phases_matrix[i]).T,
                            self.bulk_comp[self.comp_col].values[0],
                        )
                        phase_prop.append(phase_prop_iter)
                        phase_prop_r.append(phase_prop_iter_r)
                    prop_array.append(phase_prop)
                    prop_r2.append(phase_prop_r)

            for i in range(run_numbers):
                restore_df = pd.DataFrame([])
                for idx, val in enumerate(self.massBalance_phase):
                    restore_df[val] = [x[i][idx] for x in prop_array]
                restore_df["r2"] = [x[i] for x in prop_r2]
                restore_df["residues"] = restore_df["r2"] ** 2
                restore_dict[i] = restore_df

            for key, val in zip(
                self.match_index[self.match_column], restore_dict.values()
            ):
                res_dict[key] = val
            if exportFiles:
                _exportFiles(res_dict, filename)
            # return res_dict

        elif method == "svd":
            if mc:
                for num in range(mc):
                    phases_matrix = (
                        []
                    )  # collect phase matrix for mass balance calculation
                    for i in range(run_numbers):
                        phase_mb = []  # collect phase array in each iteration
                        for idx, phase in enumerate(self.massBalance_phase):
                            exp_std = (
                                np.random.normal(0, 1, len(self.comp_std_col))
                                * self.exp_mb_std[phase].iloc[i].values
                            )
                            phase_mb.append(
                                self.exp_mb_dict[phase].iloc[i].values + exp_std,
                            )
                        phases_matrix.append(phase_mb)
                    phase_prop = []  # collect phase proportions in each mc iteration
                    phase_prop_r = []  # collect r2 in each mc iteration
                    if batch_bulk:
                        for i in range(len(phases_matrix)):
                            bulk_std = (
                                np.random.normal(0, 1, len(self.comp_std_col))
                                * self.bulk_comp[self.comp_std_col].iloc[i]
                            )
                            phase_prop_iter = _svd_mb(
                                phases_matrix[i],
                                bulk_std.values
                                + self.bulk_comp[self.comp_col].iloc[i].values,
                            )
                            phase_prop_iter_r = np.sum(
                                (
                                    np.sum(
                                        (
                                            phases_matrix[i]
                                            * phase_prop_iter.reshape(
                                                len(phase_prop_iter), 1
                                            )
                                        ),
                                        axis=0,
                                    )
                                    - (
                                        bulk_std.values
                                        + self.bulk_comp[self.comp_col].iloc[i].values,
                                    )
                                )
                                ** 2
                            )
                            phase_prop.append(phase_prop_iter)
                            phase_prop_r.append(phase_prop_iter_r)
                        prop_array.append(phase_prop)
                        prop_r2.append(phase_prop_r)
                    else:
                        for i in range(len(phases_matrix)):
                            bulk_std = (
                                np.random.normal(0, 1, len(self.comp_std_col))
                                * self.bulk_comp[self.comp_std_col].values[0]
                            )
                            phase_prop_iter = _svd_mb(
                                phases_matrix[i],
                                bulk_std + self.bulk_comp[self.comp_col].values[0],
                            )
                            phase_prop_iter_r = np.sum(
                                (
                                    np.sum(
                                        (
                                            phases_matrix[i]
                                            * phase_prop_iter.reshape(
                                                len(phase_prop_iter), 1
                                            )
                                        ),
                                        axis=0,
                                    )
                                    - (
                                        # bulk_std
                                        +self.bulk_comp[self.comp_col].values[0]
                                    )
                                )
                                ** 2
                            )
                            phase_prop.append(phase_prop_iter)
                            phase_prop_r.append(phase_prop_iter_r)
                        prop_array.append(phase_prop)
                        prop_r2.append(phase_prop_r)

            else:
                phases_matrix = []  # collect phase matrix for mass balance calculation
                for i in range(run_numbers):
                    phase_mb = []  # collect phase array in each iteration
                    for idx, phase in enumerate(self.massBalance_phase):

                        phase_mb.append(
                            self.exp_mb_dict[phase].iloc[i].values,
                        )
                    phases_matrix.append(phase_mb)
                phase_prop = []  # collect phase proportions in each mc iteration
                phase_prop_r = []  # collect r2 in each mc iteration
                if batch_bulk:
                    for i in range(len(phases_matrix)):
                        phase_prop_iter = _svd_mb(
                            phases_matrix[i],
                            self.bulk_comp[self.comp_col].iloc[i].values,
                        )
                        phase_prop_iter_r = np.sum(
                            (
                                np.sum(
                                    (
                                        phases_matrix[i]
                                        * phase_prop_iter.reshape(
                                            len(phase_prop_iter), 1
                                        )
                                    ),
                                    axis=0,
                                )
                                - (self.bulk_comp[self.comp_col].iloc[i].values)
                            )
                            ** 2
                        )
                        phase_prop.append(phase_prop_iter)
                        phase_prop_r.append(phase_prop_iter_r)
                    prop_array.append(phase_prop)
                    prop_r2.append(phase_prop_r)
                else:
                    for i in range(len(phases_matrix)):
                        phase_prop_iter = _svd_mb(
                            phases_matrix[i], self.bulk_comp[self.comp_col].values[0]
                        )
                        phase_prop_iter_r = np.sum(
                            (
                                np.sum(
                                    (
                                        phases_matrix[i]
                                        * phase_prop_iter.reshape(
                                            len(phase_prop_iter), 1
                                        )
                                    ),
                                    axis=0,
                                )
                                - (self.bulk_comp[self.comp_col].values[0])
                            )
                            ** 2
                        )
                        phase_prop.append(phase_prop_iter)
                        phase_prop_r.append(phase_prop_iter_r)
                    prop_array.append(phase_prop)
                    prop_r2.append(phase_prop_r)
                # restore_dict = {}
            for i in range(run_numbers):
                restore_df = pd.DataFrame([])
                for idx, val in enumerate(self.massBalance_phase):
                    restore_df[val] = [x[i][idx] for x in prop_array]
                restore_df["residues"] = [x[i] for x in prop_r2]
                restore_df["r2"] = restore_df["residues"] ** 0.5
                restore_dict[i] = restore_df
            # res_dict = {}
            for key, val in zip(
                self.match_index[self.match_column], restore_dict.values()
            ):
                res_dict[key] = val
            if exportFiles:
                _exportFiles(res_dict, filename)
        return res_dict
