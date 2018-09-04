# Copyright (c) Gigantum

# The below is a relatively straightforward adaptation of directions at
# https://cran.r-project.org/bin/linux/ubuntu/README.html

FROM gigantum/python3-minimal:latest
LABEL maintainer="Gigantum <support@gigantum.com>"

# I downloaded this key using
# gpg --keyserver keyserver.ubuntu.com --recv-key 0x51716619e084dab9
# gpg -a --export 0x51716619e084dab9 > rutter-cran-key.txt
# Could also directly do: apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 0x51716619e084dab9
# gpg and gpg-agent are required in any case
COPY rutter-cran-key.txt /tmp/

# Install system level dependencies
RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
        # Enables add-apt-repository
        software-properties-common \
        # These two packages required to import keys into apt
        gpg \
        gpg-agent \
    && apt-key add /tmp/rutter-cran-key.txt \
    && echo "deb https://cloud.r-project.org/bin/linux/ubuntu bionic-cran35/" > /etc/apt/sources.list.d/cran.list \
    # This also triggers an update as of 18.04/bionic
    && add-apt-repository ppa:marutter/c2d4u3.5 \
    && apt-get install -yq --no-install-recommends \
        r-base \
        # We get any remaining needed compilers here
        r-base-dev \
        r-recommended \
        r-cran-tidyverse \
        r-cran-data.table \
        r-cran-devtools \
        # Needed by IRkernel
        r-cran-repr \
        # OpenBLAS makes R much faster - it will be default upon install
        libopenblas-base \
        libopenblas-dev \
    && apt-get clean

# XXX Maybe we should use MRAN? It would certainly make subsequent projects
# more reproducible, but is not in line with how we're using pip, conda,
# etc. e.g.:
# options(repos=c(CRAN="https://cran.microsoft.com/snapshot/2018-07-23/"))
RUN echo 'options(repos = c(CRAN = "https://cloud.r-project.org/"))' >> /etc/R/Rprofile.site

# NOTE the most efficient approach to installing R package (e.g. foo) from
# source is to do this first:
# sudo apt-get build-dep r-cran-foo

# Install IRkernal and set up the installed R interpreter in Jupyter
RUN R -e "devtools::install_github('IRkernel/IRkernel'); IRkernel::installspec()"
