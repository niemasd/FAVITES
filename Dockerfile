# Set up Ubuntu environment
FROM ubuntu:17.10
RUN apt-get update

# Install Python 3 and modules
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
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
