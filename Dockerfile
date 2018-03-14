# FAVITES minimal docker image using Ubuntu base
FROM ubuntu:latest
MAINTAINER Niema Moshiri <niemamoshiri@gmail.com>

# Set up environment
RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y autoconf curl default-jre git gsl-bin libcurl4-openssl-dev libgsl0-dev libssl-dev wget

# Set up R and packages
RUN echo "deb http://cran.rstudio.com/bin/linux/ubuntu xenial/" >> /etc/apt/sources.list && \
    gpg --keyserver keyserver.ubuntu.com --recv-key E084DAB9 && \
    gpg -a --export E084DAB9 | apt-key add - && \
    apt-get update && apt-get install -y r-base r-base-dev && \
    git clone https://github.com/ropensci/git2r.git && \
    R CMD INSTALL --configure-args="--with-libssl-include=/usr/lib/" git2r && \
    rm -rf git2r /tmp/* && \
    Rscript -e "install.packages(c('ape','data.table','devtools','distr','gamlss','phytools','reshape2','RColorBrewer','ggplot2'), repos='https://cloud.r-project.org/')" && \
    Rscript -e "library(devtools); install_github('niemasd/PANGEA.HIV.sim')"
RUN Rscript -e "library(devtools); install_github('niemasd/PANGEA.HIV.sim')"

# Set up Python 3 and modules
RUN apt-get install -y python3 python3-pip && \
    pip3 install --upgrade pip && \
    pip3 install dendropy && \
    pip3 install networkx && \
    pip3 install numpy && \
    pip3 install scipy && \
    pip3 install pyvolve

# Set up ART (MountRainier-2016-06-05)
RUN curl https://www.niehs.nih.gov/research/resources/assets/docs/artsrcmountrainier20160605linuxtgz.tgz | tar xz && \
    cd art_src_MountRainier_Linux && make && mv art_* /usr/local/bin && cd .. && rm -rf art_src_MountRainier_Linux

# Set up DWGSIM
RUN git clone --recursive https://github.com/nh13/DWGSIM.git && \
    cd DWGSIM && make && mv dwgsim* /usr/local/bin && cd .. && rm -rf DWGSIM

# Set up GEMF
RUN git clone https://github.com/niemasd/GEMF.git && \
    cd GEMF && make && mv GEMF /usr/local/bin && cd .. && rm -rf GEMF

# Set up Grinder
RUN wget -qO- https://tenet.dl.sourceforge.net/project/biogrinder/biogrinder/Grinder-0.5.4/Grinder-0.5.4.tar.gz | tar -xz && \
    cd Grinder* && perl Makefile.PL && make && make install && cd .. && rm -rf Grinder*

# Set up HMMER
RUN curl http://eddylab.org/software/hmmer3/3.1b2/hmmer-3.1b2-linux-intel-x86_64.tar.gz | tar xz && \
    mv hmmer*/binaries/* /usr/local/bin && rm -rf hmmer*

# Set up Seq-Gen
RUN git clone https://github.com/rambaut/Seq-Gen.git && \
    cd Seq-Gen/source && make && mv seq-gen /usr/local/bin && cd ../.. && rm -rf Seq-Gen

# Set up Dual-Birth Simulator
RUN git clone https://github.com/niemasd/Dual-Birth-Simulator.git && \
    cd Dual-Birth-Simulator && make && mv dualbirth /usr/local/bin && mv yule /usr/local/bin && cd .. && rm -rf Dual-Birth-Simulator

# Set up Newick Utilities
RUN curl http://cegg.unige.ch/pub/newick-utils-1.6-Linux-x86_64-disabled-extra.tar.gz | tar xz && \
    mv newick-utils*/src/nw_* /usr/local/bin && rm -rf newick-utils*

# Set up FAVITES
RUN git clone https://github.com/niemasd/FAVITES.git
ENV PATH="/FAVITES:${PATH}"
ENV FAVITES_DOCKER=TRUE

# Clean up
RUN find /usr/lib/python3.*/ -name 'tests' -exec rm -r '{}' + && \
    rm -rf /root/.cache && \
    rm -rf /tmp/*

# Run FAVITES
ENTRYPOINT ["/bin/bash", "-c", "run_favites.py"]
