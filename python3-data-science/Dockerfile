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
RUN conda install --quiet --yes nodejs=12.16.1 && \
    conda install --quiet --yes \
        'blas=*=openblas' \
        'bokeh=2.0' \
        'cloudpickle=1.3' \
        'cython=0.29' \
        'dask-core=2.14' \
        'dill=0.3' \
        'h5py=2.10' \
        'hdf5=1.10' \
        'ipywidgets=7.5' \
        'matplotlib=3.2' \
        'networkx=2.4' \
        'numba=0.48' \
        'numexpr=2.7' \
        'numpy=1.18' \
        'pandas=1.0' \
        'patsy=0.5' \
        'pillow=7.1' \
        'psutil=5.7' \
        'pywavelets=1.1' \
        'pyyaml=5.3' \
        'scikit-image=0.16' \
        'scikit-learn=0.22' \
        'scipy=1.4' \
        'seaborn=0.10' \
        'sqlalchemy=1.3' \
        'statsmodels=0.11' \
        'sympy=1.5' \
        'xarray=0.15' \
        'xlrd=1.2'  \
    && conda install --quiet --yes -c plotly 'plotly=4.6' 'plotly-orca=1.3' \
    # Note - we used to remove pyqt and qt since we are mostly browser-based, but the conda solver pulls it in as part
    # of any subsequent installation, so it's better to just leave it installed to save space and time
    && conda clean --all

# Set up additional widgets
RUN export NODE_OPTIONS=--max-old-space-size=4096 && \
    jupyter labextension install jupyterlab_bokeh --no-build && \
    jupyter labextension install @jupyterlab/geojson-extension --no-build && \
    # Activate ipywidgets extensions for JupyterLab
    jupyter labextension install @jupyter-widgets/jupyterlab-manager@1.1 --no-build && \
    jupyter labextension install plotlywidget@1.4.0 --no-build && \
    jupyter labextension install jupyterlab-plotly@1.4.0 --no-build && \
    # Build all of the above
    jupyter lab build && \
    # unset just in case
    unset NODE_OPTIONS && \
    # Activate ipywidgets for notebook server just in case
    jupyter nbextension enable --py widgetsnbextension --sys-prefix && \
    npm cache clean --force && \
    rm -rf $CONDA_DIR/share/jupyter/lab/staging && \
    rm -rf /root/.cache/yarn && \
    rm -rf /root/.node-gyp

# Give numba a location for JIT compiled files
ENV NUMBA_CACHE_DIR /tmp

# Import matplotlib the first time to build the font cache.
ENV XDG_CACHE_HOME /var/local/cache/
RUN MPLBACKEND=Agg python -c "import matplotlib.pyplot"
