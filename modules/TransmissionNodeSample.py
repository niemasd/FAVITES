#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionNodeSample" module
'''
import abc

class TransmissionNodeSample(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``TransmissionNodeSample`` module

    Methods
    -------
    cite()
        Return citation string (or None)
    init()
        Initialize the module (if need be)
    sampleNodes(time)
        Returns two nodes to be involved in a transmission event at ``time''
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
    def check_contact_network(cn):
        '''
        Check if the given contact network is compatible

        Parameters
        ----------
        cn : ContactNetwork
            The contact network to check for compatibility with module
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    def sample_nodes(time):
        '''
        Returns two nodes to be involved in a transmission event at ``time''

        Parameters
        ----------
        time : float
            The time at which this transmission event will take place

        Returns
        -------
        source : ContactNetworkNode
            The node that is the source of the transmission
        target : ContactNetworkNode
            The node that is the target of the transmission
        '''
        pass