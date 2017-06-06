#! /usr/bin/env python3
'''
Niema Moshiri 2016

"NodeAvailability" module
'''
import abc

class NodeAvailability(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``NodeAvailability`` module

    Methods
    -------
    cite()
        Return citation string (or None)
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
    def cite():
        '''
        Return citation string (or None)

        Returns
        -------
        citation : str
            The citation string (or None)
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