# Set up Ubuntu environment
FROM ubuntu:17.10              # Ubuntu 17.10 as base
RUN apt-get update             # update Ubuntu
RUN apt-get -y install python3 # install python3
