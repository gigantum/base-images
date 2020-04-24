# Copyright (c) Gigantum

FROM gigantum/r-tidyverse:ac8dce36e8-2020-04-24
LABEL maintainer="Gigantum <support@gigantum.com>"

# Install system level dependencies
RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
        # RStudio requirements for notebooks
        r-cran-catools \
        r-cran-bitops \
    && apt-get clean

# downloading GPG keys is problematic, so we use the sha256 hash
# There are numerous potential issues with gpg in Docker, including firewalls
# that block all but web ports, and broken ipv6

# Using variables mostly to make it obvious what needs to be updated in future
ENV RSTUDIO_SHA256=ed4f765d85165c78967892f65c1b167059d9fd4977e273126e946e45db0372f8 \
    RSTUDIO_VER=1.2.5042

RUN wget https://download2.rstudio.org/server/bionic/amd64/rstudio-server-${RSTUDIO_VER}-amd64.deb \
    && echo $RSTUDIO_SHA256 rstudio-server-${RSTUDIO_VER}-amd64.deb | sha256sum -c \
    && apt-get install -yq --no-install-recommends ./rstudio-server-*-amd64.deb \
    && apt-get clean \
    && rm rstudio-server-*-amd64.deb

# Expose port for RStudio
EXPOSE 8787

# It's best to have COPYs at the end so you can change them without a massive
# rebuild
COPY rserver.conf /etc/rstudio/rserver.conf
# This will get copied out at Project Container creation
COPY user-settings /tmp
