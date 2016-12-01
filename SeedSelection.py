#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSelection" module
'''
import abc # for abstraction

class SeedSelection(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``SeedSelection`` module

    Methods
    -------
    select_seed_nodes(user_input, contact_network)
        Select nodes in ``contact_network'' to use as seed nodes
    '''

    @staticmethod
    @abc.abstractmethod
    def select_seed_nodes():
        '''
        Select nodes in ``contact_network'' to use as seed nodes. Will probably
        want to use FAVITES_Global.num_seeds and FAVITES_Global.contact_network.

        Returns
        -------
        seed_nodes : list of ContactNetworkNode
            The nodes of the contact network to use as seeds
        '''
        pass