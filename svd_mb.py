import pandas as pd
import numpy as np
from numpy.linalg import svd

def svd_mb(phase, exp_sc):
    list_idx = [idx for idx, x in enumerate(phase) if x.sum()>0]  # remove empty matrix, thus no phase composition
    a_matrix = [phase[i] for i in list_idx]  # index to existing phases
    A_matrix = np.array(a_matrix).T.tolist()  #  convert the matrix to row as chemical oxides, col as phases
    u, sigma, v = svd(A_matrix)  # svd, decomposite the matrix to u, sigma and v
    sigma_reciprocal = 1 / sigma[sigma !=0]  # take repciprocal of all non-zero elements in sigma,
    sigma_fill = np.zeros((np.shape(A_matrix)[1], np.shape(A_matrix)[0]))  # create a sigma_plus with a n * m dimension (A_matrix in m*n)
    np.fill_diagonal(sigma_fill,sigma_reciprocal, wrap=True)  # fill the diagonal of sigma_fill with reciprocal results
    a_matrix_plus = v.T.dot(sigma_fill.dot(u.T))  # compute the pseudoinverse of matrix A
    res = a_matrix_plus.dot(exp_sc.to_numpy())  # calculate proportions
    empt_arr = np.zeros(len(phase))  # create empty list with the same dimension as the number of phases
    empt_arr[list_idx] = res  # index the existing phase back to origin position
    return empt_arr
