#!python

import numpy as np


def simple_copy_fortran(double[:, :] mat):
    if mat.is_f_contig():
        return mat.base
    else:
        return np.asarray(mat.copy_fortran())
