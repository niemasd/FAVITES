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
    subsample_transmission_network()
        Return a subsampled list of (u,v,time) transmission events
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
        Return a set of subsampled nodes from the transmission network

        Returns
        -------
        transmissions : list of (u,v,float) tuples
            A subsampled list of (u,v,time) transmission events
        '''
        pass