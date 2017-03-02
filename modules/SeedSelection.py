#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSelection" module
'''
import abc

class SeedSelection(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``SeedSelection`` module

    Methods
    -------
    init()
        Initialize the module (if need be)
    select_seed_nodes()
        Select nodes to use as seed nodes
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
    def select_seeds():
        '''
        Select nodes in ``contact_network'' to use as seed nodes. Will probably
        want to use FAVITES_Global.num_seeds and FAVITES_Global.contact_network.

        Returns
        -------
        seed_nodes : list of ContactNetworkNode
            The nodes of the contact network to use as seeds
        '''
        pass