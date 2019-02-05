# Note, some docker commands taken from/inspired by the standard docker-stacks maintained
# by the Jupyter team: https://github.com/jupyter/docker-stacks/
# which are Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

FROM gigantum/python3-minimal:a55419bd77-2019-01-03
LABEL maintainer="Gigantum <support@gigantum.com>"


RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
        # These are needed by some conda-installed packages, such as opencv
        libxrender1 \
        libxext6 \
        libgl1-mesa-glx \
    && apt-get clean

# Install Python packages
# Remove pyqt and qt pulled in for matplotlib since we're only ever going to
# use notebook-friendly backends in these images
# nodejs is for jupyter lab extensions below
RUN conda install --quiet --yes nodejs && \
    conda install --quiet --yes \
        'blas=*=openblas' \
        'bokeh=1.0' \
        'cloudpickle=0.6' \
        'cython=0.29' \
        'dill=0.2' \
        'h5py=2.7' \
        'hdf5=1.10' \
        'ipywidgets=7.4' \
        'matplotlib=2.2' \
        'numba=0.41' \
        'numexpr=2.6' \
        'pandas=0.23' \
        'patsy=0.5' \
        'plotly=3.4' \
        'scikit-image=0.14' \
        'scikit-learn=0.20' \
        'scipy=1.1' \
        'seaborn=0.9' \
        'sqlalchemy=1.2' \
        'statsmodels=0.9' \
        'sympy=1.3' \
        'xarray=0.11' \
        'xlrd=1.1'  \
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
