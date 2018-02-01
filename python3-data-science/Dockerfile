# Copyright (c) Gigantum

# Note, some docker commands taken from/inspired by the standard docker-stacks maintained
# by the Jupyter team: https://github.com/jupyter/docker-stacks/
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

FROM gigantum/python3-minimal
LABEL maintainer="Gigantum <hello@gigantum.io>"

# Install Python packages
# Remove pyqt and qt pulled in for matplotlib since we're only ever going to
# use notebook-friendly backends in these images
RUN conda install --quiet --yes nodejs && \
    conda install --quiet --yes \
    'nomkl' \
    'pandas=0.22*' \
    'numexpr=2.6*' \
    'matplotlib=2.1*' \
    'plotly=2.2*' \
    'scipy=1.0*' \
    'seaborn=0.7*' \
    'scikit-learn=0.19*' \
    'scikit-image=0.13*' \
    'sympy=1.0*' \
    'cython=0.27*' \
    'patsy=0.4*' \
    'statsmodels=0.8*' \
    'cloudpickle=0.2*' \
    'dill=0.2*' \
    'numba=0.36*' \
    'bokeh=0.12*' \
    'sqlalchemy=1.1*' \
    'hdf5=1.8.17' \
    'h5py=2.6*' \
    'vincent=0.4.*' \
    'beautifulsoup4=4.5.*' \
    'protobuf=3.*' \
    'xlrd=1.1*'  && \
    'xarray=0.10*'  && \
    jupyter labextension install @jupyterlab/plotly-extension jupyterlab_bokeh && \
    jupyter labextension install jupyterlab_bokeh && \
    conda remove --quiet --yes --force qt pyqt && \
    conda clean -tipsy && \
    npm cache --force clean && \
    rm -rf $CONDA_DIR/share/jupyter/lab/staging

# Import matplotlib the first time to build the font cache.
ENV XDG_CACHE_HOME /opt/matplotlib/.cache/
RUN MPLBACKEND=Agg python -c "import matplotlib.pyplot"
