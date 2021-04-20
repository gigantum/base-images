# Copyright (c) Gigantum

FROM gigantum/r-tidyverse:a349a41d8b-2021-04-20
LABEL maintainer="Gigantum <support@gigantum.com>"

# downloading GPG keys is problematic, so we use the sha256 hash
# There are numerous potential issues with gpg in Docker, including firewalls
# that block all but web ports, and broken ipv6

# Using variables mostly to make it obvious what needs to be updated in future
# Check here for latest version: https://rstudio.com/products/rstudio/download/#download
ENV RSTUDIO_SHA256=a46bbfbcb468e7af6aa12280adb830056f4a10e3457fd2f5969bb31d4d476939 \
    RSTUDIO_VER=1.4.1106

RUN curl --silent --show-error --location --output rstudio-server-${RSTUDIO_VER}-amd64.deb \
         https://download2.rstudio.org/server/bionic/amd64/rstudio-server-${RSTUDIO_VER}-amd64.deb && \
    echo $RSTUDIO_SHA256 rstudio-server-${RSTUDIO_VER}-amd64.deb | sha256sum -c && \
    apt-get update && apt-get install -yq gdebi-core && \
    gdebi ./rstudio-server-*-amd64.deb && \
    apt-get remove -qq -y gdebi-core && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    rm ./rstudio-server-*-amd64.deb

# Install system level dependencies
RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
        # RStudio requirements for notebooks
        r-cran-catools \
        r-cran-bitops \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

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
