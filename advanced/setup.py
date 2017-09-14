# NOTE: This is copied in three different places (bad software practice).
import setuptools
import Cython.Build


def main():
    extension = Cython.Build.cythonize('repro.pyx')
    setuptools.setup(
        ext_modules=extension,
    )


if __name__ == '__main__':
    main()
