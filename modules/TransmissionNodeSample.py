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
    sampleNodes(time)
        Returns two nodes to be involved in a transmission event at ``time''
    '''

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