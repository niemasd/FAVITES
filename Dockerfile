# FAVITES minimal docker image using Alpine base
FROM alpine:latest
MAINTAINER Niema Moshiri <niemamoshiri@gmail.com>

# Set up environment
RUN apk update
RUN apk upgrade
RUN apk add --virtual=.build-dependencies --no-cache bash coreutils curl curl-dev g++ gcc gfortran git gsl gsl-dev libressl-dev libstdc++ libxml2-dev make musl-dev ncurses ncurses-dev openblas openssl perl perl-dev wget

# Set up R and packages
RUN apk add --no-cache --virtual=.build-dependencies R R-dev R-doc
RUN git clone https://github.com/ropensci/git2r.git &&\
  R CMD INSTALL --configure-args="--with-libssl-include=/usr/lib/" git2r &&\
  rm -rf git2r /tmp/*
RUN Rscript -e "install.packages(c('ape','data.table','devtools','distr','gamlss','phytools'), repos='https://cloud.r-project.org/')"
RUN Rscript -e "library(devtools); install_github('olli0601/PANGEA.HIV.sim'); library(PANGEA.HIV.sim)"

# Set up Python 3 and modules
RUN apk add --no-cache python3 python3-dev && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi
RUN pip3 install dendropy
RUN pip3 install networkx
RUN pip3 install numpy
RUN pip3 install pyvolve

# Set up ART (MountRainier-2016-06-05)
RUN curl https://www.niehs.nih.gov/research/resources/assets/docs/artsrcmountrainier20160605linuxtgz.tgz | tar xz
RUN cd art_src_MountRainier_Linux && make && mv art_* /usr/local/bin && cd .. && rm -rf art_src_MountRainier_Linux

# Set up DWGSIM
RUN git clone --recursive https://github.com/nh13/DWGSIM.git
RUN cd DWGSIM && make && mv dwgsim* /usr/local/bin && cd .. && rm -rf DWGSIM

# Set up GEMF
RUN git clone https://github.com/niemasd/GEMF.git
RUN cd GEMF && make && mv GEMF /usr/local/bin && cd .. && rm -rf GEMF

# Set up Grinder
RUN wget -qO- https://sourceforge.net/projects/biogrinder/files/latest/download | tar -xz
RUN cd Grinder* && perl Makefile.PL && make && make install && cd .. && rm -rf Grinder*

# Set up HMMER
RUN curl http://eddylab.org/software/hmmer3/3.1b2/hmmer-3.1b2-linux-intel-x86_64.tar.gz | tar xz
RUN mv hmmer*/binaries/* /usr/local/bin && rm -rf hmmer*

# Set up Seq-Gen
RUN git clone https://github.com/rambaut/Seq-Gen.git
RUN cd Seq-Gen/source && make && mv seq-gen /usr/local/bin && cd ../.. && rm -rf Seq-Gen

# Set up FAVITES
RUN git clone https://github.com/niemasd/FAVITES.git
ENV PATH="/FAVITES:${PATH}"

# Test FAVITES
RUN run_favites.py -c FAVITES/example/example_config.json
RUN rm -rf ~/FAVITES_output

# Clean up
RUN find /usr/lib/python3.*/ -name 'tests' -exec rm -r '{}' +
RUN rm -rf /root/.cache
RUN apk del .build-dependencies
RUN rm -rf /tmp/*
