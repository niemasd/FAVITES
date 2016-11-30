#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworEdge" module
'''
import abc # for abstraction

class ContactNetworkEdge(metaclass=abc.ABCMeta):
    '''
    Abstract class defining a ``ContactNetworkEdge'' object

    Methods
    -------
    get_attribute()
        Return the attribute(s) of this ``ContactNetworkEdge'' object
    get_from()
        Return the ``ContactNetworkNode'' object from which this edge is leaving
    get_to()
        Return the ``ContactNetworkNode'' object to which this edge is going

    '''

    @abc.abstractmethod
    def get_attribute(self):
        '''
        Return the attribute(s) of this ``ContactNetworkEdge'' object

        Returns
        -------
        attribute : str
            The attribute(s) of this ``ContactNetworkEdge'' object
        '''
        pass

    @abc.abstractmethod
    def get_from(self):
        '''
        Return the ``ContactNetworkNode'' object from which this edge is leaving

        Returns
        -------
        from : ContactNetworkNode
            The ``ContactNetworkNode'' object from which this edge is leaving
        '''
        pass

    @abc.abstractmethod
    def get_to(self):
        '''
        Return the ``ContactNetworkNode'' object to which this edge is going

        Returns
        -------
        to : ContactNetworkNode
            The ``ContactNetworkNode'' object to which this edge is going
        '''
        pass