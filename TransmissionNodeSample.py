#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionNodeSample" module
'''
import abc # for abstraction

class TransmissionNodeSample(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``TransmissionNodeSample`` module

    Methods
    -------
    sampleNodes()
        Returns two nodes to be involved in a transmission event
    '''

    @staticmethod
    @abc.abstractmethod
    def sample_nodes():
        '''
        Returns two nodes to be involved in a transmission event

        Returns
        -------
        source : ContactNetworkNode
            The node that is the source of the transmission
        target : ContactNetworkNode
            The node that is the target of the transmission
        '''
        pass