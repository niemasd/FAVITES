#! /usr/bin/env python3
'''
Niema Moshiri 2016

"NodeSample" module
'''
import abc # for abstraction

class NodeSample(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``NodeSample`` module

    Methods
    -------
    subsample_transmission_network()
        Return a subsampled list of (u,v,time) transmission events
    '''

    @staticmethod
    @abc.abstractmethod
    def subsample_transmission_network():
        '''
        Return a set of subsampled nodes from the transmission network

        Returns
        -------
        nodes : set of ContactNetworkNode
            A set of subsampled nodes from the transmission network
        '''
        pass