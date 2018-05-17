# Copyright (c) Gigantum

FROM gigantum/python3-minimal:latest
LABEL maintainer="Gigantum <hello@gigantum.io>"

# Install apt packages
RUN apt-get -y update && apt-get -y install libfontconfig1 libxext6 libxrender1 && \
    conda install numpy=1.14.1 osmnx=0.7.2 pillow=5.0.0 scikit-learn=0.19.1 scipy=1.0.0 wkhtmltopdf=0.12.4 && \
    pip install Jinja2==2.10 imgkit==1.0.1 overpy==0.4 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    conda clean -tipsy
