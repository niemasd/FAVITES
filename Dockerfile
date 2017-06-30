# FAVITES minimal docker image using Alpine base
FROM alpine:latest
MAINTAINER Niema Moshiri <niemamoshiri@gmail.com>

# Set up environment
RUN apk update
RUN apk upgrade
RUN apk add --virtual=.build-dependencies --no-cache bash coreutils curl curl-dev g++ gcc gfortran git gsl gsl-dev libressl-dev libstdc++ libxml2-dev musl-dev ncurses openblas openssl

# Set up R and packages
RUN apk add --no-cache --virtual=.build-dependencies R R-dev R-doc
RUN git clone https://github.com/ropensci/git2r.git &&\
  R CMD INSTALL --configure-args="--with-libssl-include=/usr/lib/" git2r &&\
  rm -rf git2r /tmp/*
RUN Rscript -e "install.packages(c('ape','data.table','devtools','distr','gamlss','phytools'), repos='https://cloud.r-project.org/')"
RUN Rscript -e "library(devtools); install_github('olli0601/PANGEA.HIV.sim'); library(PANGEA.HIV.sim)"

# Set up Python 3 and modules
RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi
RUN pip3 install dendropy
RUN pip3 install networkx
RUN pip3 install numpy
RUN pip3 install pyvolve

# Clean up (Python 3)
RUN find /usr/lib/python3.*/ -name 'tests' -exec rm -r '{}' +
RUN rm /usr/include/xlocale.h
RUN rm -rf /root/.cache
RUN apk del .build-dependencies

# Clean up (R)
RUN rm -rf /tmp/*
