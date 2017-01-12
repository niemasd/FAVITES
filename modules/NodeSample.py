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
    init()
        Initialize the module (if need be)
    subsample_nodes()
        Return a subsampled list of nodes
    '''

    @staticmethod
    @abc.abstractmethod
    def init():
        '''
        Initialize the module (if need be)
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    def subsample_transmission_network():
        '''
        Return a subsampled list of nodes

        Returns
        -------
        nodes : list of ``ContactNetworkNode''
            A subsampled list of nodes
        '''
        pass