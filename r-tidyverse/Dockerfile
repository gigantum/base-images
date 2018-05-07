# Copyright (c) Gigantum

# Note, some docker commands taken from/inspired by the standard docker-stacks maintained
# by the Jupyter team: https://github.com/jupyter/docker-stacks/
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

FROM ubuntu:16.04
LABEL maintainer="Gigantum <hello@gigantum.io>"

# Install system level dependencies
RUN apt-get update && apt-get -yq dist-upgrade && \
    apt-get install -yq --no-install-recommends \
    wget \
    bzip2 \
    ca-certificates \
    sudo \
    locales \
    fonts-liberation \
    gosu \
    git && \
    apt-get clean 

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen

# Setup environment variables
ENV CONDA_DIR=/opt/conda \
    GIGANTUM_SHARE=/mnt/share \
    GIGANTUM_WORKDIR=/mnt/labbook \
    SHELL=/bin/bash \
    MINICONDA_VERSION=4.3.31 \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8
ENV PATH=$CONDA_DIR/bin:$PATH \
    JUPYTER_RUNTIME_DIR=$GIGANTUM_SHARE/jupyter/runtime

# Install conda and python
RUN cd /tmp && wget --quiet https://repo.continuum.io/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh && \
    echo "7fe70b214bee1143e3e3f0467b71453c *Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh" | md5sum -c - && \
    /bin/bash Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh -f -b -p $CONDA_DIR && \
    rm Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh && \
    # For now, we use the MS R Open packaged by Anaconda, so disabling conda-forge
    # This is currently the only difference from python3-minimal - and indeed,
    # perhaps we should 
    # conda config --system --prepend channels conda-forge && \
    conda config --system --set auto_update_conda false && \
    conda config --system --set show_channel_urls true && \
    conda update --all --quiet --yes 

# Install and configure JupyterLab
RUN conda install --quiet --yes -c conda-forge \
    # Also bumped versions here as compared to python3-minimal
    'jupyterlab=0.32.*' \
    'notebook=5.4.*' && \
    conda clean -tipsy && \
    rm -rf $CONDA_DIR/share/jupyter/lab/staging
EXPOSE 8888

# Set working dir
WORKDIR $GIGANTUM_WORKDIR

# Install Python packages
# Remove pyqt and qt pulled in for matplotlib since we're only ever going to
# use notebook-friendly backends in these images
RUN conda install --quiet --yes nodejs && \
    conda install --quiet --yes \
    nomkl \
    'mro-base=3.4.*' \
    # We might want to break this up ourselves...
    r-tidyverse \
    # Currently r-tidyverse=1.2.1=mro343h889e2dd_0 expands to:
    # mro-base
    # r-broom >=0.4.2
    # r-cli >=1.0.0
    # r-crayon >=1.3.4
    # r-dbplyr >=1.1.0
    # r-dplyr >=0.7.4
    # r-forcats >=0.2.0
    # r-ggplot2 >=2.2.1
    # r-haven >=1.1.0
    # r-hms >=0.3
    # r-httr >=1.3.1
    # r-jsonlite >=1.5
    # r-lubridate >=1.7.1
    # r-magrittr >=1.5
    # r-modelr >=0.1.1
    # r-purrr >=0.2.4
    # r-readr >=1.1.1
    # r-readxl >=1.0.0
    # r-reprex >=0.1.1
    # r-rlang >=0.1.4
    # r-rstudioapi >=0.7
    # r-rvest >=0.3.2
    # r-stringr >=1.2.0
    # r-tibble >=1.3.4
    # r-tidyr >=0.7.2
    # r-xml2 >=1.1.1
    #
    # People also like this, kind of like a lower-level dplyr
    r-dt \
    r-irkernel \
    conda remove --quiet --yes --force qt pyqt && \
    conda clean -tipsy && \
    npm cache --force clean && \
    rm -rf $CONDA_DIR/share/jupyter/lab/staging

# CMD may be updated during final image assembly, but this keeps a container alive.
CMD ["tail -f /dev/null"]
