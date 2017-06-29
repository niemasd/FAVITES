# Set up Ubuntu environment
FROM ubuntu:17.10
RUN apt-get update

# Install Python 3 and modules
RUN apt-get -y install python3
RUN pip3 install dendropy
pip3 install networkx
pip3 install numpy
pip3 install pyvolve
