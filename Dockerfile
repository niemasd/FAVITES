# FAVITES minimal docker image using Alpine base
FROM alpine:latest
MAINTAINER Niema Moshiri <niemamoshiri@gmail.com>

# Set up environment
RUN apk update
RUN apk upgrade

# Set up R and packages
RUN apk add --no-cache R R-dev R-doc curl libressl-dev curl-dev libxml2-dev gcc g++ git coreutils bash ncurses
RUN Rscript -e "install.packages('devtools', repos = 'https://cloud.r-project.org/')"
RUN Rscript -e "library(devtools); install_github('olli0601/PANGEA.HIV.sim')"

# Set up Python 3 and modules
RUN apk add --no-cache libstdc++ lapack-dev && \
    apk add --no-cache \
        --virtual=.build-dependencies \
        g++ gfortran musl-dev \
        python3-dev && \
    ln -s locale.h /usr/include/xlocale.h
RUN pip install dendropy
RUN pip install networkx
RUN pip install numpy
RUN pip install pyvolve

# Clean up (Python 3)
RUN find /usr/lib/python3.*/ -name 'tests' -exec rm -r '{}' +
RUN rm /usr/include/xlocale.h
RUN rm -rf /root/.cache
RUN apk del .build-dependencies

# Clean up (R)
RUN rm -rf httpuv /tmp/*
