# FAVITES minimal docker image using Alpine base
FROM alpine:latest
MAINTAINER Niema Moshiri <niemamoshiri@gmail.com>

# Set up environment
RUN apk update
RUN apk upgrade
RUN apk add --no-cache libstdc++ lapack-dev
RUN apk add --no-cache --virtual=.build-dependencies g++ gfortran musl-dev python3-dev
RUN ln -s locale.h /usr/include/xlocale.h

# Install Python 3 and modules
#RUN apk add --no-cache python3 && python3 -m ensurepip && rm -r /usr/lib/python*/ensurepip && pip3 install --upgrade pip setuptools && if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi
RUN pip3 install dendropy
RUN pip3 install networkx
RUN pip3 install numpy
RUN pip3 install pyvolve

# Install R and packages
RUN apt-get -y install r-base
RUN echo "r <- getOption('repos'); r['CRAN'] <- 'http://cran.us.r-project.org'; options(repos = r);" > ~/.Rprofile
RUN apt-get -y install libcurl4-gnutls-dev
RUN apt-get -y install libssl-dev
RUN Rscript -e "install.packages('devtools')"
RUN Rscript -e "library(devtools); install_github('olli0601/PANGEA.HIV.sim')"

# Clear cache at very end
RUN rm -r /root/.cache
find /usr/lib/python3.*/ -name 'tests' -exec rm -r '{}' +
rm /usr/include/xlocale.h
apk del .build-dependencies
