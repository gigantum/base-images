# Copyright (c) Gigantum

# Note, some docker commands taken from/inspired by the standard docker-stacks maintained
# by the Jupyter team: https://github.com/jupyter/docker-stacks/
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

FROM ubuntu:18.04
LABEL maintainer="Gigantum <hello@gigantum.com>"

# Install system level dependencies
RUN apt-get update && \
    apt-get install -yq --no-install-recommends wget bzip2 ca-certificates sudo locales fonts-liberation gosu git \
    libfontconfig1 libxext6 libxrender1 && \
    apt-get clean 

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen

# Setup environment variables
ENV CONDA_DIR=/opt/conda \
    GIGANTUM_SHARE=/mnt/share \
    GIGANTUM_WORKDIR=/mnt/labbook \
    SHELL=/bin/bash \
    MINICONDA_VERSION=4.5.1 \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8
ENV PATH=$CONDA_DIR/bin:$PATH \
    JUPYTER_RUNTIME_DIR=$GIGANTUM_SHARE/jupyter/runtime

# Install conda, python, and jupyter
RUN cd /tmp && wget --quiet https://repo.continuum.io/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh && \
    echo "0c28787e3126238df24c5d4858bd0744 *Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh" | md5sum -c - && \
    /bin/bash Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh -f -b -p $CONDA_DIR && \
    rm Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh && \
    conda config --system --prepend channels conda-forge && \
    conda config --system --set auto_update_conda false && \
    conda config --system --set show_channel_urls true && \
    conda update --all --quiet --yes && \
    conda install --quiet --yes -c conda-forge 'blas=*=openblas' \
    jupyterlab=0.32.* notebook=5.5.* numpy=1.14.1 osmnx=0.7.2 pillow=5.0.0 \
    scikit-learn=0.19.1 scipy=1.0.0 wkhtmltopdf=0.12.4 && \
    pip install Jinja2==2.10 imgkit==1.0.1 overpy==0.4 && \
    conda remove --quiet --yes --force qt pyqt && \
    conda clean --all

# Import matplotlib the first time to build the font cache.
ENV XDG_CACHE_HOME /opt/matplotlib/.cache/
RUN MPLBACKEND=Agg python -c "import matplotlib.pyplot"

# Expose port for jupyterlab
EXPOSE 8888

# Set working dir
WORKDIR $GIGANTUM_WORKDIR

# CMD may be updated during final image assembly, but this keeps a container alive.
CMD ["tail -f /dev/null"]
