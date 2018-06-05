# Copyright (c) Gigantum

# Note, some docker commands taken from/inspired by the standard docker-stacks maintained
# by the Jupyter team: https://github.com/jupyter/docker-stacks/
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

FROM gigantum/python3-minimal:latest
LABEL maintainer="Gigantum <hello@gigantum.io>"


# Install system level dependencies
RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    # The following two are required for a functional R
    # There is little harm in including them in our python image as well - so
    # they could be refactored into a core base image
    # https://github.com/ContinuumIO/anaconda-issues/issues/4656
    # Note that if you run in the console, R still complains about R_X11.so / libSM
    libxrender1 \
    libxext6 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /var/log/dpkg.log

# Install R packages
# For R, the Anaconda "official" packages seem better than conda-forge
RUN conda install --quiet --yes --override-channels --channel defaults \
    # These install a lot of stuff. We'll write them broken out in the manifest
    # in environment-components
    'r-essentials=3.4.*' \
    'r-tidyverse=1.2.*' \
    # This makes Jupyter work
    'r-irkernel=0.8.*' \
    # data.table is included in the above
    # This is a nice javascript viz for tables called "DataTables", not relevant until we have shiny
    # r-dt=0.2 \
    && conda clean --all
