# Gigantum Official Base Docker Image Repository

A repository to maintain Gigantum authored Base Docker Images for LabBook
environments. During development, this repository will generally be checked out
as a submodule of [gtm](https://github.com/gigantum/gtm). High-level
instructions are available in that repository.

## Images

### python3-minimal

A minimal Base containing Python 3.6 and JupyterLab with no additional
packages. Python and JupyterLab are installed via conda. The `conda-forge`
channel is prepended to the conda channel configuration by default.

### python3-data-science

A Base built from `python3-minimal` with additional common data science
packages pre-installed.

#### Pre-Installed Packages

- Via `conda`
  - nomkl
  - pandas
  - numexpr
  - matplotlib
  - plotly
  - scipy
  - seaborn
  - scikit-learn
  - scikit-image
  - sympy
  - cython
  - patsy
  - statsmodels
  - cloudpickle
  - dill
  - numba
  - bokeh
  - sqlalchemy
  - hdf5
  - h5py
  - vincent
  - beautifulsoup4
  - protobuf
  - xlrd
  - xarray


### python2-minimal

A minimal Base containing Python 2.7 and JupyterLab with no additional
packages. Python and JupyterLab are installed via conda. The `conda-forge`
channel is prepended to the conda channel configuration by default.

### r-tidyverse

An R image managed by conda, based on the python3-minimal image. The IRkernel
is installed for interaction with R via notebooks in JupyterLab.

#### Directly installed packages

Conda contains two metapackages that provide a large array of packages. As
such, the directly specified packages are relatively minimal:

- r-essentials
- r-tidyverse
- r-irkernel

## Contributing

Gigantum uses the [Developer Certificate of Origin](https://developercertificate.org/). 
This is lightweight approach that doesn't require submission and review of a
separate contributor agreement.  Code is signed directly by the developer using
facilities built into git.

Please see [`docs/contributing.md`  in the gtm
repository](https://github.com/gigantum/gtm/tree/integration/docs/contributing.md).

## Credits

TODO
