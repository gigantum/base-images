# Copyright (c) Gigantum

# Note, some docker commands taken from/inspired by the standard docker-stacks maintained
# by the Jupyter team: https://github.com/jupyter/docker-stacks/
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

FROM ubuntu:18.04
LABEL maintainer="Gigantum <hello@gigantum.com>"

# This is needed for tzdata to proceed, but seems generally right
ENV DEBIAN_FRONTEND=noninteractive

# Install system level dependencies
RUN apt-get update \ 
    && apt-get install -yq --no-install-recommends \
        wget \
        bzip2 \
        ca-certificates \
        # dirmngr \
        locales \
        fonts-liberation \
        gosu \
        # Various libraries break without the Olson database included here
        tzdata \
        git \
        # Enables add-apt-repository
        software-properties-common \
        # These two packages required to import keys into apt
        gpg \
        gpg-agent \
    # Should we make this more robust? - can break because of docker networking
    # e.g., on Windows. See r-tidyverse base for an alternative.
    && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9 \
    && echo "deb https://cloud.r-project.org/bin/linux/ubuntu bionic-cran35/" > /etc/apt/sources.list.d/cran.list \
    # This also triggers an update as of 18.04/bionic
    && add-apt-repository ppa:marutter/c2d4u3.5 \
    && apt-get install -yq --no-install-recommends \
        r-base \
        # We get our compilers here
        r-base-dev \
        r-recommended \
        r-cran-tidyverse \
        r-cran-data.table \
        r-cran-devtools \
        # TODO: There's not a cran package for 3.5 and RcppGSL, so we may build
        # it if needed. But it MAY be in the c2d4u3.5 PPA...
        # libgsl-dev \
        # OpenBLAS makes R much faster - it will be default upon install
        libopenblas-base \
        libopenblas-dev \
    && echo 'options(repos = c(CRAN = "https://cloud.r-project.org/"))' >> /etc/R/Rprofile.site \
    # RStudio requirements - keeping separate with thoughts of a refactor
    && apt-get install -yq --no-install-recommends \
        psmisc \
        libapparmor1 \
        libedit2 \
        lsb-release \
        libssl1.0.0 \
    && apt-get clean

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen

# Setup environment variables
ENV GIGANTUM_SHARE=/mnt/share \
    GIGANTUM_WORKDIR=/mnt/labbook \
    SHELL=/bin/bash \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8

# No conda for now
# ENV CONDA_DIR=/opt/conda \
#     MINICONDA_VERSION=4.5.1 \
#     PATH=$CONDA_DIR/bin:$PATH \

# Nor even Jupyter
# ENV JUPYTER_RUNTIME_DIR=$GIGANTUM_SHARE/jupyter/runtime

# downloading the GPG key for RStudio is problematic, so we use the md5 hashe
# There are numerous potential issues with gpg, including firewalls that block
# all but web ports, and broken ipv6

# Using variables mostly to make it obvious what needs to be updated in future
ENV RSTUDIO_MD5=ea77929e40eac30baee9e336e26a1dd5 \
    RSTUDIO_VER=1.1.456

RUN wget https://download2.rstudio.org/rstudio-server-${RSTUDIO_VER}-amd64.deb \
    && echo $RSTUDIO_MD5 rstudio-server-${RSTUDIO_VER}-amd64.deb | md5sum -c \
    && dpkg -i rstudio-server-*-amd64.deb \
    && rm rstudio-server-*-amd64.deb

# Expose port for jupyterlab
EXPOSE 8787

# Set working dir
WORKDIR $GIGANTUM_WORKDIR

# CMD may be updated during final image assembly, but this keeps a container alive.
CMD ["tail -f /dev/null"]
