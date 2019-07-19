# Copyright (c) Gigantum

# The below is a relatively straightforward adaptation of directions at
# https://cran.r-project.org/bin/linux/ubuntu/README.html

FROM gigantum/r-tidyverse:87c90e7834-2019-07-19
LABEL maintainer="Gigantum <support@gigantum.com>"

# Install system level dependencies
RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
        # RStudio requirements for notebooks
        r-cran-catools \
        r-cran-bitops \
        # For some reason not in the dependencies for RStudio, but it is required
        libssl1.0.0 \
    && apt-get clean

# downloading the GPG key for RStudio is problematic, so we use the md5 hash
# There are numerous potential issues with gpg, including firewalls that block
# all but web ports, and broken ipv6

# Using variables mostly to make it obvious what needs to be updated in future
ENV RSTUDIO_MD5=4e9ee8bad6b8a88ea57caa80106cd388 \
    RSTUDIO_VER=1.2.1335

RUN wget https://download2.rstudio.org/server/trusty/amd64/rstudio-server-${RSTUDIO_VER}-amd64.deb \
    && echo $RSTUDIO_MD5 rstudio-server-${RSTUDIO_VER}-amd64.deb | md5sum -c \
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
