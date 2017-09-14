# [Memoryview][1] Issue

This is a basic reproduction of an issue with concurrent usage of
`is_c_contig()` and `is_f_contig()`. It has been [reported][2]
previously, but the discussion ended.

The gist of the issue:

> Cython seems to think (for some reason) that the second
> function is the same as the first and omits the definition.

To reproduce I have two functions, one that uses **only**
`is_f_contig()` (called "simple") and one that uses both
`is_c_contig()` and `is_f_contig()` (called "advanced").

## `advanced`

When "advanced" is used alone, the **problem manifests**:

```
$ cd advanced/
$ python setup.py build_ext --inplace
Compiling repro.pyx because it changed.
[1/1] Cythonizing repro.pyx
...
repro.c: In function ‘__pyx_pf_5repro_advanced_copy_fortran’:
repro.c:2008:18: warning: implicit declaration of function ‘__pyx_memviewslice_is_f_contig2’ [-Wimplicit-function-declaration]
     __pyx_t_11 = __pyx_memviewslice_is_f_contig2(__pyx_v_mat); if (unlikely(__pyx_t_11 == -1)) __PYX_ERR(0, 15, __pyx_L1_error)
                  ^
...
$
$ python test_it.py
Traceback (most recent call last):
  File "test_it.py", line 6, in <module>
    import repro
ImportError: .../repro....so: undefined symbol: __pyx_memviewslice_is_f_contig2
```

## `simple`

When "simple" is used alone, it **works just fine**:

```
$ cd simple/
$ python setup.py build_ext --inplace
$
$ python test_it.py
------------------------------------------------------------
mat =
[[ 2.  0.]
 [ 1.  3.]]

    mat F-contiguous? False

new_mat F-contiguous? True
 all(new_mat == mat)? True
     new_mat is mat ? False
------------------------------------------------------------
mat =
[[ 5.5 -1. ]
 [ 2.   0. ]]

    mat F-contiguous? True

new_mat F-contiguous? True
 all(new_mat == mat)? True
     new_mat is mat ? True
------------------------------------------------------------
mat =
[[ 7.  2.]]

    mat F-contiguous? True

new_mat F-contiguous? True
 all(new_mat == mat)? True
     new_mat is mat ? False
------------------------------------------------------------
mat =
[[ 11.]
 [ 12.]
 [ 10.]]

    mat F-contiguous? True

new_mat F-contiguous? True
 all(new_mat == mat)? True
     new_mat is mat ? False
```

## `both`

When both "simple" and "advanced" are used, it **works just fine**
(this is because `simple_copy_fortran` pulls in the definition
of `is_f_contig`).

```
$ cd both/
$ python setup.py build_ext --inplace
$
$ python test_it.py
------------------------------------------------------------
mat =
[[ 2.  0.]
 [ 1.  3.]]

    mat F-contiguous? False

                     SIMPLE | ADVANCED
----------------------------+----------
new_mat F-contiguous? True  | True
 all(new_mat == mat)? True  | True
     new_mat is mat ? False | False
------------------------------------------------------------
mat =
[[ 5.5 -1. ]
 [ 2.   0. ]]

    mat F-contiguous? True

                     SIMPLE | ADVANCED
----------------------------+----------
new_mat F-contiguous? True  | True
 all(new_mat == mat)? True  | True
     new_mat is mat ? True  | True
------------------------------------------------------------
mat =
[[ 7.  2.]]

    mat F-contiguous? True

                     SIMPLE | ADVANCED
----------------------------+----------
new_mat F-contiguous? True  | True
 all(new_mat == mat)? True  | True
     new_mat is mat ? False | True
------------------------------------------------------------
mat =
[[ 11.]
 [ 12.]
 [ 10.]]

    mat F-contiguous? True

                     SIMPLE | ADVANCED
----------------------------+----------
new_mat F-contiguous? True  | True
 all(new_mat == mat)? True  | True
     new_mat is mat ? False | True
```


[1]: http://cython.readthedocs.io/en/latest/src/userguide/memoryviews.html
[2]: https://mail.python.org/pipermail/cython-devel/2013-February/003345.html
