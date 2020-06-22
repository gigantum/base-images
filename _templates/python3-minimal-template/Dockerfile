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
        curl \
        bzip2 \
        ca-certificates \
        gcc \
        g++ \
        make \
        locales \
        fonts-liberation \
        gosu \
        tzdata \
        # Enable `make install` for git w/ openssl
        dh-autoreconf \
        openssl \
        libz-dev \
        libexpat1-dev \
        libcurl4-openssl-dev \
    && apt-get clean

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen

# Build Git from source with OpenSSL
RUN mkdir /tmp/gitbuild && cd /tmp/gitbuild && \
    # Get the latest git tarball
    git_tarball_url="https://www.github.com$(curl 'https://github.com/git/git/tags' | grep -o "/git/git/archive/v2\..*\.tar\.gz" | sort -r | head -1 | tr -d '\n')" && \
    curl -L --retry 5 "${git_tarball_url}" --output git-source.tar.gz && \
    tar -xf git-source.tar.gz --strip 1 && \
    rm git-source.tar.gz && \
    make configure && \
    # Configure the custom git build to use openSSL for better enterprise network support.
    NO_PERL=1 NO_TCLTK=1 NO_GETTEXT=1 ./configure --prefix=/usr/local --with-openssl && \
    make -j2 && \
    make install && \
    cd ~ && \
    rm -rf /tmp/gitbuild

# Get the latest git LFS binary
RUN mkdir /tmp/lfs_install && cd /tmp/lfs_install && \
    git_lfs_tarball_url="https://www.github.com$(curl 'https://github.com/git-lfs/git-lfs/releases' | grep -o "/git-lfs/git-lfs/releases/download/v2..*/git-lfs-linux-amd64-v2..*.tar.gz" | sort -r | head -1 | tr -d '\n')" && \
    curl -L --retry 5 "${git_lfs_tarball_url}" --output git-lfs.tar.gz && \
    tar -xf git-lfs.tar.gz git-lfs && \
    cp ./git-lfs /usr/local/bin/git-lfs && \
    chmod 755 /usr/local/bin/git-lfs && \
    # We'll need to run `git-lfs install` for the user at Project launch
    cd ~ && \
    rm -rf /tmp/lfs_install

# Setup environment variables
ENV CONDA_DIR=/opt/conda \
    GIGANTUM_SHARE=/mnt/share \
    GIGANTUM_WORKDIR=/mnt/labbook \
    SHELL=/bin/bash \
    MINICONDA_VERSION=py37_4.8.3 \
    MINICONDA_MD5=751786b92c00b1aeae3f017b781018df \
    GIGANTUM_NODE_VERSION=12.16.1
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8
# Now we can use the variables defined above
ENV PATH=$CONDA_DIR/bin:$PATH \
    JUPYTER_RUNTIME_DIR=$GIGANTUM_SHARE/jupyter/runtime \
    # We use the future location of the mounted project - we need to ensure we delete this directory below
    XDG_CACHE_HOME=$GIGANTUM_WORKDIR/code/untracked/.cache

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
    # Recommended by conda-forge
    conda config --set channel_priority strict && \
    conda config --system --set auto_update_conda false && \
    conda config --system --set show_channel_urls true && \
    # We update conda explicitly to get any gains in performance, etc.
    # Be sure to check the version of requests installed by conda and update the yaml files!
    conda update --quiet --yes conda && \
    conda update --all --quiet --yes && \
    # Now installing nbresuse via conda - it's not working via pip for some reason
    conda install --quiet --yes -c conda-forge \
      jupyterlab=2.1 \
      notebook=6.0 \
      numpydoc=0.9 \
      nbresuse \
      # Pip is installed by default by conda, but it's mission
      # critical so we make it explicit
      pip \
      # We pin the version of nodejs so we can be sure to re-install the same
      # version later - avoiding jupyterlab extension rebuilds and generally
      # improving compatability
      nodejs==$GIGANTUM_NODE_VERSION && \
    jupyter labextension install @jupyterlab/toc && \
    npm cache clean --force && \
    rm -rf $CONDA_DIR/share/jupyter/lab/staging && \
    # XDG_CACHE_DIR is currently located in the mounted project / workdir, so we delete the whole thing
    rm -rf $GIGANTUM_WORKDIR && \
    rm -rf /root/.node-gyp && \
    conda remove --quiet --yes nodejs && \
    conda clean --all

# Do some minor configuration of Jupyterlab for our Dockerized environment
# Currently just disabling the extension manager (which doesn't make sense for Gigantum AND is broken without nodejs)
COPY page_config.json /opt/conda/share/jupyter/lab/settings

# Expose port for jupyterlab
EXPOSE 8888

# Set working dir
WORKDIR $GIGANTUM_WORKDIR

# CMD may be updated during final image assembly, but this keeps a container alive.
CMD ["tail", "-f", "/dev/null"]
