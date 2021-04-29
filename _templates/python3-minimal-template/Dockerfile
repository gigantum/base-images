# Template arguments
ARG BASE_IMAGE

# Start Image Def
FROM $BASE_IMAGE
LABEL maintainer="Gigantum <support@gigantum.com>"

# Conda/Miniforge Arguments
ARG conda_version="4.10.0"
ARG miniforge_patch_number="0" 
ARG miniforge_version="${conda_version}-${miniforge_patch_number}" 
ARG miniforge_sha256="c56cc2da96043688c6bdb521d825de27754de0a342d5228ba3155cd94532ff75"

ENV DEBIAN_FRONTEND=noninteractive \
    GIT_VERSION=2.31.1

# Install system level dependencies
RUN apt-get update \
    && apt-get install -yqq --no-install-recommends \
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
        less \
        vim \
        wget \
    && apt-get clean

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen

# Build Git from source with OpenSSL
RUN apt-get update \
    # These packages enable `make install` for git w/ openssl
    && apt-get install -yqq \
        dh-autoreconf \
        openssl \
        libz-dev \
        libexpat1 libexpat1-dev \
        libcurl4 libcurl4-openssl-dev \
    && mkdir /tmp/gitbuild && cd /tmp/gitbuild \
    # Get the latest git tarball
    && curl -L --retry 5 "https://github.com/git/git/archive/refs/tags/v${GIT_VERSION}.tar.gz" --output git-source.tar.gz \
    && tar -xf git-source.tar.gz --strip 1 \
    && rm git-source.tar.gz \
    && make configure \
    # Configure the custom git build to use openSSL for better enterprise network support.
    && NO_PERL=1 NO_TCLTK=1 NO_GETTEXT=1 ./configure --prefix=/usr/local --with-openssl \
    && make -j2 \
    && make install \
    && cd ~ \
    && rm -rf /tmp/gitbuild \
    && apt-get -qq -y remove dh-autoreconf libz-dev libexpat1-dev libcurl4-openssl-dev \
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
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    CONDA_VERSION="${conda_version}" \
    MINIFORGE_VERSION="${miniforge_version}"

# Now we can use the variables defined above
ENV PATH=$CONDA_DIR/bin:$PATH \
    JUPYTER_RUNTIME_DIR=$GIGANTUM_SHARE/jupyter/runtime \
    # We use the future location of the mounted project - we need to ensure we delete this directory below
    XDG_CACHE_HOME=$GIGANTUM_WORKDIR/code/untracked/.cache

# Install conda, mamba, and jupyter
RUN cd /tmp && \
    echo "https://github.com/conda-forge/miniforge/releases/download/${miniforge_version}/Mambaforge-${miniforge_version}-Linux-x86_64.sh" && \
    wget --quiet "https://github.com/conda-forge/miniforge/releases/download/${miniforge_version}/Mambaforge-${miniforge_version}-Linux-x86_64.sh" && \
    echo "${miniforge_sha256} *Mambaforge-${miniforge_version}-Linux-x86_64.sh" | sha256sum -c - && \
    /bin/bash "Mambaforge-${miniforge_version}-Linux-x86_64.sh" -f -b -p $CONDA_DIR && \
    rm "Mambaforge-${miniforge_version}-Linux-x86_64.sh" && \
    echo "conda ${conda_version}" >> $CONDA_DIR/conda-meta/pinned && \
    # We don't want the `r` channel
    conda config --system --append channels anaconda && \
    # Recommended by conda-forge
    conda config --set channel_priority strict && \
    conda config --system --set auto_update_conda false && \
    conda config --system --set show_channel_urls true && \
    # We update conda explicitly to get any gains in performance, etc.
    # Be sure to check the version of requests installed by conda and update the yaml files!
    mamba update --all --quiet --yes && \
    # Now installing nbresuse via conda - it's not working via pip for some reason
    mamba install --quiet --yes -c conda-forge \
      jupyterlab=3.0.14 \
      notebook=6.2.0 \
      xeus-python=0.12.3 \
      jupyter-resource-usage \
      # Pip is installed by default by conda, but it's mission
      # critical so we make it explicit
      pip && \
    # Create settings directory for jupyterlab
    mkdir  /opt/conda/share/jupyter/lab/settings && \
    # XDG_CACHE_DIR is currently located in the mounted project / workdir, so we delete the whole thing
    rm -rf $GIGANTUM_WORKDIR && \
    conda clean --all

# Do some minor configuration of Jupyterlab for our Dockerized environment
# Currently just disabling the extension manager (which doesn't make sense for Gigantum AND is broken without nodejs)
# see https://jupyterlab.readthedocs.io/en/stable/user/extensions.html#settings
COPY overrides.json /opt/conda/share/jupyter/lab/settings/

# Expose port for jupyterlab
EXPOSE 8888

# Set working dir
WORKDIR $GIGANTUM_WORKDIR

# CMD may be updated during final image assembly, but this keeps a container alive.
CMD ["tail", "-f", "/dev/null"]
