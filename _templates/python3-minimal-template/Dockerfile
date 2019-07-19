# Copyright (c) Gigantum

# Note, some docker commands taken from/inspired by the standard docker-stacks maintained
# by the Jupyter team: https://github.com/jupyter/docker-stacks/
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Template arguments
ARG BASE_IMAGE

# Start Image Def
FROM $BASE_IMAGE
LABEL maintainer="Gigantum <support@gigantum.com>"
ENV DEBIAN_FRONTEND noninteractive

# Install system level dependencies
RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
        wget \
        bzip2 \
        ca-certificates \
        gcc \
        g++ \
        make \
        locales \
        fonts-liberation \
        gosu \
        tzdata \
        git \
    && apt-get clean

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen

# Setup environment variables
ENV CONDA_DIR=/opt/conda \
    GIGANTUM_SHARE=/mnt/share \
    GIGANTUM_WORKDIR=/mnt/labbook \
    SHELL=/bin/bash \
    MINICONDA_VERSION=4.6.14 \
    MINICONDA_MD5=718259965f234088d785cad1fbd7de03 \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8
ENV PATH=$CONDA_DIR/bin:$PATH \
    JUPYTER_RUNTIME_DIR=$GIGANTUM_SHARE/jupyter/runtime

# Install conda, python, and jupyter
RUN cd /tmp && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh && \
    echo "$MINICONDA_MD5 *Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh" | md5sum -c - && \
    /bin/bash Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh -f -b -p $CONDA_DIR && \
    rm Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh && \
    conda config --system --prepend channels conda-forge && \
    # We don't want the `r` channel
    conda config --system --remove channels defaults && \
    conda config --system --append channels anaconda && \
    conda config --system --set auto_update_conda false && \
    conda config --system --set show_channel_urls true && \
    # We update conda explicitly to get any gains in performance, etc.
    conda update --quiet --yes conda && \
    conda update --all --quiet --yes && \
    # notebook 5.3 through 5.7.1 have security holes
    conda install --quiet --yes -c conda-forge jupyterlab=1.0.2 'notebook>=6.0,<6.1' && \
    # This is currently installed by default by conda, but it's mission
    # critical so we make it explicit
    conda install pip && \
    # We pin the version of nodejs so we can be sure to re-install the same
    # version later - avoiding jupyterlab extension rebuilds and generally
    # improving compatability
    conda install --quiet --yes nodejs==10.15.3 && \
    pip install nbresuse && \
    # enable memory usage reporting in the statusbar (now installed by default)
    jupyter serverextension enable --py nbresuse && \
    jupyter labextension install @jupyterlab/toc && \
    npm cache clean --force && \
    rm -rf $CONDA_DIR/share/jupyter/lab/staging && \
    rm -rf /root/.cache/yarn && \
    rm -rf /root/.node-gyp && \
    conda remove --quiet --yes nodejs && \
    conda clean --all

# Expose port for jupyterlab
EXPOSE 8888

# Set working dir
WORKDIR $GIGANTUM_WORKDIR

# CMD may be updated during final image assembly, but this keeps a container alive.
CMD ["tail", "-f", "/dev/null"]
