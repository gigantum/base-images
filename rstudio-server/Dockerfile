# Copyright (c) Gigantum

FROM gigantum/r-tidyverse:07619444b6-2021-05-05
LABEL maintainer="Gigantum <support@gigantum.com>"

# downloading GPG keys is problematic, so we use the sha256 hash
# There are numerous potential issues with gpg in Docker, including firewalls
# that block all but web ports, and broken ipv6

# Using variables mostly to make it obvious what needs to be updated in future
# Check here for latest version: https://rstudio.com/products/rstudio/download/#download
ENV RSTUDIO_SHA256=47022541152d0b586c810ab23c36ee2fc0d7e0d1b69c554dfcd7fe00d0fb571b \
    RSTUDIO_VER=1.3.1093

RUN cd /tmp && \
    curl --silent --show-error --location --output rstudio-server-${RSTUDIO_VER}-amd64.deb \
         https://download2.rstudio.org/server/bionic/amd64/rstudio-server-${RSTUDIO_VER}-amd64.deb && \
    echo $RSTUDIO_SHA256 rstudio-server-${RSTUDIO_VER}-amd64.deb | sha256sum -c && \
    apt-get update && apt-get install -yq gdebi-core && \
    gdebi -n ./rstudio-server-*-amd64.deb && \
    apt-get clean && \
    rm ./rstudio-server-*-amd64.deb

# Install system level dependencies
RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
        # RStudio requirements for notebooks
        r-cran-catools \
        r-cran-bitops \
    && apt-get clean

# Expose port for RStudio
EXPOSE 8787

# It's best to have COPYs at the end so you can change them without a massive
# rebuild
COPY rserver.conf /etc/rstudio/rserver.conf
COPY rstudio-prefs.json /etc/rstudio/rstudio-prefs.json
# This will get copied out at Project Container creation
# Note: this file is deprecated and will be removed in the future! 
#       use rstudio-prefs.json if you want to change anything.
COPY user-settings /tmp
