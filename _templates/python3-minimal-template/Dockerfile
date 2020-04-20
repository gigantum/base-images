# Note, some docker commands taken from/inspired by the standard docker-stacks maintained
# by the Jupyter team: https://github.com/jupyter/docker-stacks/
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Template arguments
ARG BASE_IMAGE

# We do multi-stage build so we can re-use our custom git across bases (multiple CUDA plus the standard python3-minimal)
FROM ubuntu:18.04 as git-builder

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -yq update && \
    # Install all apt packages
    apt-get -yq --no-install-recommends install curl ca-certificates make dh-autoreconf libexpat1-dev \
        libz-dev openssl libcurl4-openssl-dev gcc

# Get Git source
RUN mkdir /opt/gitbuild && cd /opt/gitbuild && \
    # Get the latest git tarball
    git_tarball_url="https://www.github.com$(curl 'https://github.com/git/git/tags' | grep -o "/git/git/archive/v2\..*\.tar\.gz" | sort -r | head -1 | tr -d '\n')" && \
    curl -L --retry 5 "${git_tarball_url}" --output git-source.tar.gz && \
    tar -xf git-source.tar.gz --strip 1 && \
    rm git-source.tar.gz

# Build Git
RUN cd /opt/gitbuild && \
    make configure && \
    # Configure the custom git build to use openSSL for better enterprise network support.
    NO_PERL=1 NO_TCLTK=1 NO_GETTEXT=1 ./configure --prefix=/usr/local --with-openssl && \
    make -j2

# Get the latest git LFS binary
RUN mkdir /opt/lfs_install && cd /opt/lfs_install && \
    git_lfs_tarball_url="https://www.github.com$(curl 'https://github.com/git-lfs/git-lfs/releases' | grep -o "/git-lfs/git-lfs/releases/download/v2..*/git-lfs-linux-amd64-v2..*.tar.gz" | sort -r | head -1 | tr -d '\n')" && \
    curl -L --retry 5 "${git_lfs_tarball_url}" --output git-lfs.tar.gz && \
    tar -xf git-lfs.tar.gz git-lfs && \
    rm git-lfs.tar.gz

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
        # At least some of these three is needed for `make install` to succeed for git
        libz-dev \
        libexpat1-dev \
        libcurl4-openssl-dev \
    && apt-get clean

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen

# We don't bother deleting the results of these COPYs below, as it won't free up space
COPY --from=git-builder /opt/gitbuild /opt/gitbuild

RUN cd /opt/gitbuild && \
    NO_PERL=1 NO_TCLTK=1 NO_GETTEXT=1 make install

COPY --from=git-builder /opt/lfs_install /opt/lfs_install

RUN cd /opt/lfs_install && \
    # Configure Git-LFS
    cp ./git-lfs /usr/local/bin/git-lfs && \
    chmod 755 /usr/local/bin/git-lfs && \
    git lfs install

# Setup environment variables
ENV CONDA_DIR=/opt/conda \
    GIGANTUM_SHARE=/mnt/share \
    GIGANTUM_WORKDIR=/mnt/labbook \
    SHELL=/bin/bash \
    MINICONDA_VERSION=py37_4.8.2 \
    MINICONDA_MD5=87e77f097f6ebb5127c77662dfc3165e \
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
    # Recommended by conda-forge
    conda config --set channel_priority strict && \
    conda config --system --set auto_update_conda false && \
    conda config --system --set show_channel_urls true && \
    # We update conda explicitly to get any gains in performance, etc.
    conda update --quiet --yes conda && \
    conda update --all --quiet --yes && \
    conda install --quiet --yes -c conda-forge jupyterlab=2.0.2 'notebook>=6.0,<6.1' && \
    # This is currently installed by default by conda, but it's mission
    # critical so we make it explicit
    conda install pip && \
    # We pin the version of nodejs so we can be sure to re-install the same
    # version later - avoiding jupyterlab extension rebuilds and generally
    # improving compatability
    conda install --quiet --yes nodejs==12.16.1 && \
    # enable memory usage reporting in the statusbar (now installed by default)
    pip install nbresuse[resources] && \
    # XXX DJWC - Yuvi says you don't need to do this anymore - will delete after verifying
    # jupyter serverextension enable --py nbresuse && \
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
