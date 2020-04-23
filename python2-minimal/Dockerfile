# Copyright (c) Gigantum

# Note, some docker commands taken from/inspired by the standard docker-stacks maintained
# by the Jupyter team: https://github.com/jupyter/docker-stacks/
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

FROM ubuntu:18.04
LABEL maintainer="Gigantum <support@gigantum.com>"
ENV DEBIAN_FRONTEND noninteractive

# Install system level dependencies
RUN apt-get update && \
    apt-get install -yq --no-install-recommends \
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
    git && \
    apt-get clean

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen

# Setup environment variables
ENV CONDA_DIR=/opt/conda \
    GIGANTUM_SHARE=/mnt/share \
    GIGANTUM_WORKDIR=/mnt/labbook \
    SHELL=/bin/bash \
    MINICONDA_VERSION=4.7.12.1 \
    MINICONDA_MD5=23bf3acd6aead6e91fb936fc185b033e \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8
ENV PATH=$CONDA_DIR/bin:$PATH \
    JUPYTER_RUNTIME_DIR=$GIGANTUM_SHARE/jupyter/runtime \
    # We use the future location of the mounted project - we need to ensure we delete this directory below
    XDG_CACHE_HOME=$GIGANTUM_WORKDIR/code/untracked/.cache

# Install conda and python
RUN cd /tmp && wget --quiet https://repo.continuum.io/miniconda/Miniconda2-${MINICONDA_VERSION}-Linux-x86_64.sh && \
    echo "$MINICONDA_MD5 *Miniconda2-${MINICONDA_VERSION}-Linux-x86_64.sh" | md5sum -c - && \
    /bin/bash Miniconda2-${MINICONDA_VERSION}-Linux-x86_64.sh -f -b -p $CONDA_DIR && \
    rm Miniconda2-${MINICONDA_VERSION}-Linux-x86_64.sh && \
    conda config --system --prepend channels conda-forge && \
    # We don't want the `r` channel
    conda config --system --remove channels defaults && \
    conda config --system --append channels anaconda && \
    # Recommended by conda-forge
    conda config --set channel_priority strict && \
    conda config --system --set auto_update_conda false && \
    conda config --system --set show_channel_urls true && \
    conda update --quiet --yes conda && \
    conda update --all --quiet --yes && \
    # notebook 5.3 through 5.7.1 have security holes
    # jupyterlab 0.33 is the final version that supports python 2.7
    conda install --quiet --yes -c conda-forge \
      jupyterlab=0.33 \
      'notebook>=5.7.2,<5.8' \
      pip && \
    conda clean --all

# Expose port for jupyterlab
EXPOSE 8888

# Set working dir
WORKDIR $GIGANTUM_WORKDIR

# CMD may be updated during final image assembly, but this keeps a container alive.
CMD ["tail -f /dev/null"]
