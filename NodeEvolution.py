#! /usr/bin/env python3
'''
Niema Moshiri 2016

"NodeEvolution" module
'''
import abc # for abstraction

class NodeEvolution(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``NodeEvolution`` module

    Methods
    -------
    evolve(node)
        Simulate phylogeny evolution on ``node''
    '''

    @abc.abstractmethod
    def evolve(node, module_Tree):
        '''
        Simulate phylogeny evolution on ``node''

        Parameters
        ----------
        node : ContactNetworkNode
            ``ContactNetworkNode'' object to evolve
        '''
        pass