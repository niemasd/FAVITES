# FAVITES minimal docker image using Alpine base
FROM alpine:latest
MAINTAINER Niema Moshiri <niemamoshiri@gmail.com>

# Update distro
RUN apk update
RUN apk upgrade

# Install Python 3 and modules
RUN apk add --no-cache libstdc++ lapack-dev
RUN apk add --no-cache --virtual=.build-dependencies g++ gfortran musl-dev python3-dev
RUN ln -s locale.h /usr/include/xlocale.h
RUN pip3 install dendropy
RUN pip3 install networkx
RUN pip3 install numpy
RUN pip3 install pyvolve

# Install R and packages
RUN apk add --no-cache R R-dev R-doc curl libressl-dev curl-dev libxml2-dev gcc g++ git coreutils bash ncurses
RUN echo "r <- getOption('repos'); r['CRAN'] <- 'http://cran.us.r-project.org'; options(repos = r);" > ~/.Rprofile
RUN Rscript -e "install.packages('devtools')"
RUN Rscript -e "library(devtools); install_github('olli0601/PANGEA.HIV.sim')"

# Clear cache at very end
RUN rm -r /root/.cache
find /usr/lib/python3.*/ -name 'tests' -exec rm -r '{}' +
rm /usr/include/xlocale.h
apk del .build-dependencies
