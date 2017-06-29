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
