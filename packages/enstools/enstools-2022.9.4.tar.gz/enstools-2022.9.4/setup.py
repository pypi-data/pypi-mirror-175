# Install the ensemble tools
from setuptools import setup, find_packages
import re
import sys
import os.path

# Use the Readme file as long description.
try:
    with open("README.md", "r") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ""


def get_version():
    """
    read version string from enstools package without importing it

    Returns
    -------
    str:
            version string
    """
    with open("enstools/core/__init__.py") as f:
        for line in f:
            match = re.search(r'__version__\s*=\s*"([a-zA-Z0-9_.]+)"', line)
            if match is not None:
                return match.group(1)

def find_enstools_packages():
    """
    Find the packages inside the enstools folder.
    """

    return [f'enstools.{p}' for p in (find_packages(f'{os.path.dirname(__file__)}/enstools'))]


# only print the version and exit?
if len(sys.argv) == 2 and sys.argv[1] == "--get-version":
    print(get_version())
    exit()

# perform the actual install operation
setup(name="enstools",
      version=get_version(),
      author="Robert Redl et al.",
      author_email="robert.redl@lmu.de",
      long_description=long_description,
      long_description_content_type='text/markdown',
      url="https://github.com/wavestoweather/enstools",
      packages=['enstools', *find_enstools_packages()],
      install_requires=[
          "appdirs",
          "numpy",
          "xarray",
          "cftime",
          "dask",
          "distributed",
          "cloudpickle",
          "colorama",
          "numba",
          "toolz",
          "pint",
          "cartopy",
          "matplotlib",
          "decorator",
          "multipledispatch",
          "cachey",
          "cffi",
          "pandas",
          "packaging",
          "h5netcdf",
          "h5py",
          "hdf5plugin",
          "numcodecs",
          "scikit-image",
          "scikit-learn",
          "scipy",
          "plotly",
          "bokeh",
          "statsmodels",
          "dataclasses",
      ],
      entry_points={
          'console_scripts': [
              'enstools-opendata=enstools.opendata.cli:main',
          ],
      },
      )
