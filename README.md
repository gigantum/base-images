# Gigantum Official Base Docker Image Repository

A repository to maintain Gigantum authored Base Docker Images for LabBook environments


## Images

### python3-minimal

A minimal Base containing Python 3.6 and JupyterLab with no additional packages. Python and JupyterLab
are installed via conda. The `conda-forge` channel is prepended to the conda channel configuration by
default.

### python3-data-science

A Base built from `python3-minimal` with additional common data science packages pre-installed.

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

A minimal Base containing Python 2.7 and JupyterLab with no additional packages. Python and JupyterLab
are installed via conda. The `conda-forge` channel is prepended to the conda channel configuration by
default.

## Contributing
TODO

## Credits
TODO

