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

    @abc.abstractmethod
    def select_seed_nodes(user_input, contact_network):
        '''
        Select nodes in ``contact_network'' to use as seed nodes

        Parameters
        ----------
        user_input : dict
            ``user_input'' parsed by ``Driver''
        contact_network : ContactNetwork
            ``ContactNetwork'' object from which to choose seed nodes

        Returns
        -------
        seed_nodes : list of ContactNetworkNode
            The nodes of the contact network to use as seeds

        '''
        pass