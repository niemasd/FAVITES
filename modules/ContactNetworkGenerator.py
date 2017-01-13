#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkGenerator" module
'''
import abc

class ContactNetworkGenerator(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``ContactNetworkGenerator`` module

    Methods
    -------
    get_edge_list()
        Return a contact network in the FAVITES-specified edge-list format
    init()
        Initialize the module (if need be)
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
    def get_edge_list():
        '''
        Return a contact network in the FAVITES-specified edge-list format

        Returns
        -------
        edge_list : list of str
            The Contact Network from which to create a ``ContactNetwork''
            object, where each element is a single edge in the specified
            edge-list input format (see framework README)
        '''
        pass