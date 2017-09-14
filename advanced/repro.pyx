#!python
# NOTE: These functions are copied verbatim from ``../simple`` and
#       ``../advanced`` (bad software practice).

import numpy as np


def advanced_copy_fortran(double[:, :] mat):
    cdef int rows, cols

    rows, cols = np.shape(mat)

    if rows == 1 or cols == 1:
        # C- or F- contiguous just means "contiguous".
        if mat.is_c_contig() or mat.is_f_contig():
            return mat.base
        else:
            return np.asarray(mat.copy_fortran())
    elif mat.is_f_contig():
        return mat.base
    else:
        return np.asarray(mat.copy_fortran())
