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
    select_seed_nodes(n, contact_network)
        Select ``n'' nodes in ``contact_network'' to use as seed nodes
    '''

    @abc.abstractmethod
    def select_seed_nodes(n, contact_network):
        '''
        Select ``n'' nodes in ``contact_network'' to use as seed nodes

        Parameters
        ----------
        n : int
            Number of seed nodes desired
        contact_network : ContactNetwork
            ``ContactNetwork'' object from which to choose seed nodes

        Returns
        -------
        seed_nodes : list of ContactNetworkNode
            The nodes of the contact network to use as seeds (``n'' total)

        '''
        pass