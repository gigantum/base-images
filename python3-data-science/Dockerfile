# Note, some docker commands taken from/inspired by the standard docker-stacks maintained
# by the Jupyter team: https://github.com/jupyter/docker-stacks/
# which are Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

FROM gigantum/python3-minimal:f415d5dff3-2021-04-29
LABEL maintainer="Gigantum <support@gigantum.com>"

RUN apt-get update && \
    apt-get install -yq --no-install-recommends \
        # These are needed by some conda-installed packages, such as opencv
        # Note that since our R bases use apt, this gets taken care of
        # automatically there
        libxrender1 libxext6 libgl1-mesa-glx \
        # ffmpeg for matplotlib anim & dvipng+cm-super for latex labels
        ffmpeg dvipng cm-super && \
    apt-get clean

# Install Python packages
RUN conda install --quiet --yes nodejs=15.14.0 && \
    conda install --quiet --yes \
        'beautifulsoup4=4.9.*' \
        'conda-forge::blas=*=openblas' \
        'bokeh=2.3.*' \
        'bottleneck=1.3.*' \
        'cloudpickle=1.6.*' \
        'cython=0.29.*' \
        'dask=2021.4.*' \
        'dill=0.3.*' \
        'h5py=3.1.*' \
        'ipywidgets=7.6.*' \
        'ipympl=0.7.*'\
        'matplotlib-base=3.4.*' \
        'networkx=2.5.*' \
        'numba=0.53.*' \
        'numexpr=2.7.*' \
        'pandas=1.2.*' \
        'patsy=0.5.*' \
        'pillow=8.1.*' \
        'plotly=4.14.*' \
        'python-kaleido=0.2.*' \
        'protobuf=3.15.*' \
        'pytables=3.6.*' \
        'pyyaml=5.4.*' \
        'scikit-image=0.18.*' \
        'scikit-learn=0.24.*' \
        'scipy=1.6.*' \
        'seaborn=0.11.*' \
        'sqlalchemy=1.4.*' \
        'statsmodels=0.12.*' \
        'sympy=1.7.*' \
        'vincent=0.4.*' \
        'widgetsnbextension=3.5.*'\
        'xarray=0.17.*' \
        'xlrd=2.0.*' && \
    # Note - we used to remove pyqt and qt since we are mostly browser-based, but the conda solver pulls it in as part
    # of any subsequent installation, so it's better to just leave it installed to save space and time
    conda clean --all -f -y

# Set up additional widgets
RUN pip install jupyterlab-geojson jupyter_bokeh dask-labextension && \
    export NODE_OPTIONS=--max-old-space-size=4096 \
    && jupyter labextension install jupyterlab-plotly@4.14.3 \
    # unset just in case
    && unset NODE_OPTIONS \
    && npm cache clean --force \
    && rm -rf $CONDA_DIR/share/jupyter/lab/staging \
    # We remove the GIGANTUM_WORKDIR because that's where we currently have our XDG_CACHE_DIR
    && rm -rf $GIGANTUM_WORKDIR \
    && rm -rf /root/.node-gyp
