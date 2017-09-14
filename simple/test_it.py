# NOTE: Most of this is copied in 3 places (bad software practice).
from __future__ import print_function

import numpy as np

import repro


SEPARATOR = '-' * 60
TEMPLATE = """\
mat =
{}

    mat F-contiguous? {}

new_mat F-contiguous? {!r:5}
 all(new_mat == mat)? {!r:5}
     new_mat is mat ? {!r:5}
"""


def main():
    mat1 = np.array([
        [2.0, 0.0],
        [1.0, 3.0],
    ], order='C')
    mat2 = np.array([
        [5.5, -1.0],
        [2.0, 0.0],
    ], order='F')
    mat3 = np.array([
        [7.0, 2.0],
    ], order='F')
    mat4 = np.array([
        [11.0],
        [12.0],
        [10.0],
    ], order='F')

    mats = (mat1, mat2, mat3, mat4)

    for mat in mats:
        print(SEPARATOR)
        new_mat = repro.simple_copy_fortran(mat)
        msg = TEMPLATE.format(
            mat, mat.flags.f_contiguous,
            new_mat.flags.f_contiguous,
            np.all(mat == new_mat),
            mat is new_mat)
        print(msg, end='')


if __name__ == '__main__':
    main()
