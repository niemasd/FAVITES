# FAVITES minimal docker image using Ubuntu base
FROM ubuntu:18.04
MAINTAINER Niema Moshiri <niemamoshiri@gmail.com>

# Set up environment
RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y autoconf curl default-jre git gsl-bin libcurl4-openssl-dev libgsl0-dev libmodule-install-perl libncurses5-dev libncursesw5-dev libssl-dev python python-pip python3 python3-pip unzip wget zlib1g-dev

# Set up Python 3 and modules
RUN pip3 install dendropy && \
    pip3 install treeswift && \
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
RUN wget --no-check-certificate -qO- https://tenet.dl.sourceforge.net/project/biogrinder/biogrinder/Grinder-0.5.4/Grinder-0.5.4.tar.gz | tar -xz && \
    cd Grinder* && echo -e "y\n" | perl Makefile.PL && echo -e "yes\n" | make && make install && cd .. && rm -rf Grinder*

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

# Set up msms
RUN wget http://www.mabs.at/ewing/msms/msms3.2rc-b163.zip && unzip msms3.2rc-b163.zip && \
    mv msms/lib/* /usr/local/lib && mv msms/bin/* /usr/local/bin && chmod a+x /usr/local/bin/msms && rm -rf msms*

# Set up FAVITES
RUN git clone https://github.com/niemasd/FAVITES.git
ENV PATH="/FAVITES:${PATH}"
ENV FAVITES_DOCKER=TRUE
RUN mkdir -p /FAVITES_MOUNT

# Clean up
RUN find /usr/lib/python3.*/ -name 'tests' -exec rm -r '{}' + && \
    rm -rf /root/.cache && \
    rm -rf /tmp/*

# Run FAVITES
ENTRYPOINT ["/bin/bash", "-c", "run_favites.py"]
