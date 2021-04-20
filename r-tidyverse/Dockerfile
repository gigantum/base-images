# Copyright (c) Gigantum

# The below is a relatively straightforward adaptation of directions at
# https://cran.r-project.org/bin/linux/ubuntu/README.html

FROM gigantum/python3-minimal:a349a41d8b-2021-04-19
LABEL maintainer="Gigantum <support@gigantum.com>"

# Install system level dependencies
RUN apt-get update && \
    # Enables add-apt-repository
    apt-get install -yq --no-install-recommends software-properties-common dirmngr \
            # These two packages required to import keys into apt
            gpg gpg-agent && \
    # import the signing key (by Michael Rutter) for these repo
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9 && \
    add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/" && \
    # This also triggers an update as of 18.04/bionic
    add-apt-repository ppa:c2d4u.team/c2d4u4.0+ && \
    apt-get update && \
    apt-get install -yq --no-install-recommends \
            r-base \
            # We get any remaining needed compilers here
            r-base-dev \
            r-recommended \
            r-cran-tidyverse \
            r-cran-data.table \
            r-cran-devtools \
            # Needed by IRkernel
            r-cran-repr \
            r-cran-pbdzmq \
            r-cran-uuid \
            # OpenBLAS makes R much faster - it will be default upon install
            libopenblas-base \
            libopenblas-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# TODO DC Maybe we should use MRAN? It would certainly make subsequent projects
# more reproducible, but is not in line with how we're using pip, conda,
# etc. e.g.:
# options(repos=c(CRAN="https://cran.microsoft.com/snapshot/2018-07-23/"))
RUN echo 'options(repos = c(CRAN = "https://cloud.r-project.org/"))\n' >> /etc/R/Rprofile.site && \
    # Also Install IRkernal and set up the installed R interpreter in Jupyter
    R -e "install.packages('IRkernel', upgrade_dependencies=FALSE); IRkernel::installspec(user=FALSE)"
    # The above will error out by attempting to use the IRkernel package.
    # An alternative is to ensure packages are installed as follows:
    # The below did not succeed even when biocLite() was run above
    # && R -e "stopifnot(all(c('IRkernel', 'BiocManager') %in% installed.packages()[, 'Package']))" \
    # The core of bioconductor is automatically installed by things like
    # neuroconductor. This will speed up one-off package installation for repos
    # that assume this as a pre-req:
    # BUT, it also seems to override numerous packages from CRAN... so skipping for now
    # && R -e 'source("https://bioconductor.org/biocLite.R"); biocLite()' \

# NOTE the most efficient approach to installing R package (e.g. foo) from
# source is to do this first:
# sudo apt-get build-dep r-cran-foo
