# Note, some docker commands taken from/inspired by the standard docker-stacks maintained
# by the Jupyter team: https://github.com/jupyter/docker-stacks/
# which are Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

FROM gigantum/python3-minimal:87c90e7834-2019-07-19
LABEL maintainer="Gigantum <support@gigantum.com>"


RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
        # These are needed by some conda-installed packages, such as opencv
        # Note that since our R bases use apt, this gets taken care of
        # automatically there
        libxrender1 \
        libxext6 \
        libgl1-mesa-glx \
    && apt-get clean

# Install Python packages

# nodejs is for jupyter lab extensions below
# It's pinned to match python3-minimal, to avoid the need to rebuild extensions
RUN conda install --quiet --yes nodejs=10.15.3 && \
    conda install --quiet --yes \
        'blas=*=openblas' \
        'bokeh=1.2' \
        'cloudpickle=1.2' \
        'cython=0.29' \
        # This is a dependency of other packages - may as well list explicitly
        # Some not currently explicit, but maybe "data science" are fastcache and pyparsing
        'dask-core=2.1' \
        'dill=0.3' \
        'h5py=2.9' \
        'hdf5=1.10' \
        'ipywidgets=7.5' \
        'matplotlib=3.1' \
        # Another dependency made explicit
        'networkx=2.3' \
        'numba=0.44' \
        'numexpr=2.6' \
        'numpy=1.16' \
        'pandas=0.25' \
        'patsy=0.5' \
        'plotly=4.0' \
        # Another dependency made explicit
        'pywavelets=1.0' \
        # Another dependency made explicit
        'pyyaml=5.1' \
        'scikit-image=0.15' \
        'scikit-learn=0.21' \
        'scipy=1.3' \
        'seaborn=0.9' \
        'sqlalchemy=1.3' \
        'statsmodels=0.10' \
        'sympy=1.4' \
        'xarray=0.12' \
        'xlrd=1.2'  \
    # Remove pyqt and qt pulled in for matplotlib since we're only ever going to
    # use notebook-friendly backends in these images
    && conda remove --quiet --yes --force qt pyqt && \
    conda clean --all

# Set up additional widgets
RUN jupyter labextension install jupyterlab_bokeh && \
    jupyter labextension install @jupyterlab/geojson-extension && \
    jupyter labextension install @jupyterlab/plotly-extension && \
    # Activate ipywidgets for notebook server just in case
    jupyter nbextension enable --py widgetsnbextension --sys-prefix && \
    # Activate ipywidgets extensions for JupyterLab
    jupyter labextension install @jupyter-widgets/jupyterlab-manager && \
    npm cache clean --force && \
    rm -rf $CONDA_DIR/share/jupyter/lab/staging && \
    rm -rf /root/.cache/yarn && \
    rm -rf /root/.node-gyp


# Import matplotlib the first time to build the font cache.
ENV XDG_CACHE_HOME /opt/matplotlib/.cache/
RUN MPLBACKEND=Agg python -c "import matplotlib.pyplot"
