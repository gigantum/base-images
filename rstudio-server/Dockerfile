# Copyright (c) Gigantum

FROM gigantum/r-tidyverse:b4b4d267e0-2020-06-29
LABEL maintainer="Gigantum <support@gigantum.com>"

# downloading GPG keys is problematic, so we use the sha256 hash
# There are numerous potential issues with gpg in Docker, including firewalls
# that block all but web ports, and broken ipv6

# Using variables mostly to make it obvious what needs to be updated in future
ENV RSTUDIO_SHA256=187af05cab1221282487fdc33f4b161484c3228eaade3d6697b1d41c206ee6d9 \
    RSTUDIO_VER=1.3.959

RUN curl --silent --show-error --location \
         --output rstudio-server-${RSTUDIO_VER}-amd64.deb \
         https://download2.rstudio.org/server/bionic/amd64/rstudio-server-${RSTUDIO_VER}-amd64.deb \
    && echo $RSTUDIO_SHA256 rstudio-server-${RSTUDIO_VER}-amd64.deb | sha256sum -c \
    && apt-get install -yq ./rstudio-server-*-amd64.deb \
    && apt-get clean \
    && rm rstudio-server-*-amd64.deb

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
# This will get copied out at Project Container creation
COPY user-settings /tmp
