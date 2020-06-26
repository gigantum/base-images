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
        curl \
        bzip2 \
        ca-certificates \
        gcc \
        g++ \
        make \
        locales \
        fonts-liberation \
        gosu \
        tzdata && \
    apt-get clean

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen

# Build Git from source with OpenSSL
RUN apt-get update \
    # These packages enable `make install` for git w/ openssl
    && apt-get install -yqq \
        dh-autoreconf \
        openssl \
        libz-dev \
        libexpat1-dev \
        libcurl4-openssl-dev \
    && mkdir /tmp/gitbuild && cd /tmp/gitbuild \
    # Get the latest git tarball
    && git_tarball_url=https://www.github.com$(curl 'https://github.com/git/git/tags' | grep -o "/git/git/archive/v2\..*\.tar\.gz" | sort -r | head -1 | tr -d '\n') \
    && curl -L --retry 5 $git_tarball_url --output git-source.tar.gz \
    && tar -xf git-source.tar.gz --strip 1 \
    && rm git-source.tar.gz \
    && make configure \
    # Configure the custom git build to use openSSL for better enterprise network support.
    && NO_PERL=1 NO_TCLTK=1 NO_GETTEXT=1 ./configure --prefix=/usr/local --with-openssl \
    && make -j2 \
    && make install \
    && cd ~ \
    && rm -rf /tmp/gitbuild \
    && apt-get -qq -y remove dh-autoreconf \
    && apt-get -qq -y autoremove \
    && apt-get clean

# Get the latest git LFS binary
RUN mkdir /tmp/lfs_install && cd /tmp/lfs_install && \
    git_lfs_tarball_url=https://www.github.com$(curl 'https://github.com/git-lfs/git-lfs/releases' | grep -o "/git-lfs/git-lfs/releases/download/v2..*/git-lfs-linux-amd64-v2..*.tar.gz" | sort -r | head -1 | tr -d '\n') && \
    curl -L --retry 5 $git_lfs_tarball_url --output git-lfs.tar.gz && \
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
    MINICONDA_VERSION=py27_4.8.3 \
    MINICONDA_MD5=19ce7d0039ab349914d928e7f32b1c1b \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8
ENV PATH=$CONDA_DIR/bin:$PATH \
    JUPYTER_RUNTIME_DIR=$GIGANTUM_SHARE/jupyter/runtime \
    # We use the future location of the mounted project - we need to ensure we delete this directory below
    XDG_CACHE_HOME=$GIGANTUM_WORKDIR/code/untracked/.cache

# Install conda and python
RUN cd /tmp && \
    curl --silent --show-error --location --output Miniconda2-${MINICONDA_VERSION}-Linux-x86_64.sh \
        https://repo.continuum.io/miniconda/Miniconda2-${MINICONDA_VERSION}-Linux-x86_64.sh && \
    echo "$MINICONDA_MD5 *Miniconda2-${MINICONDA_VERSION}-Linux-x86_64.sh" | md5sum -c - && \
    /bin/bash Miniconda2-${MINICONDA_VERSION}-Linux-x86_64.sh -f -b -p $CONDA_DIR && \
    rm Miniconda2-${MINICONDA_VERSION}-Linux-x86_64.sh && \
    conda install --quiet --yes \
      # jupyterlab 0.33 is the final version that supports python 2.7
      jupyterlab=0.33 \
      # notebook 5.7.9 patches a security hole in the old version of jQuery
      # It's only available from Anaconda, Inc's channel
      notebook==5.7.9 && \
    # We don't want the `r` channel
    conda config --system --remove channels defaults && \
    conda config --system --append channels pkgs/main && \
    # Now that we changed channel order, this will be the same as if we included conda-forge, but it'll be faster
    conda update --quiet --yes conda && \
    conda config --system --append channels conda-forge && \
    # Recommended by conda-forge
    conda config --set channel_priority strict && \
    conda config --system --set auto_update_conda false && \
    conda config --system --set show_channel_urls true && \
    # This is now a no-op
    conda update --all --quiet --yes && \
    conda clean --all

# Expose port for jupyterlab
EXPOSE 8888

# Set working dir
WORKDIR $GIGANTUM_WORKDIR

# CMD may be updated during final image assembly, but this keeps a container alive.
CMD ["tail -f /dev/null"]
