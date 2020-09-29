FROM gigantum/python3-data-science:b4b4d267e0-2020-06-29
LABEL maintainer="Gigantum <support@gigantum.com>"

# ADD Stata16Linux64.tar.gz /tmp
# Note - I extracted these from the above tar.gz file, uncompressed, then gzip'd them:
# Also note that --chown doesn't work for tar file extraction, so we change owner below
ADD stata16/unix/linux64p/ado.tar.gz /usr/local/stata16
ADD stata16/unix/linux64p/base.tar.gz /usr/local/stata16
ADD stata16/unix/linux64p/bins.tar.gz /usr/local/stata16
ADD stata16/unix/linux64p/docs.tar.gz /usr/local/stata16
# COPY stata16/unix/linux64p/inst2 /usr/local/stata16
COPY stata16/unix/linux64p/setrwxp /usr/local/stata16

WORKDIR /usr/local/stata16

RUN chown --recursive root:root *
RUN ./setrwxp now

RUN apt-get install -yqq --no-install-recommends libpng16-16

ENV PATH /usr/local/stata16:$PATH
RUN pip install stata_kernel
RUN python -m stata_kernel.install

# We return our WORKDIR to the standard Gigantum setting
WORKDIR $GIGANTUM_WORKDIR
