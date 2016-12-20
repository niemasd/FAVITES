#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SequenceEvolution" module
'''
import abc # for abstraction

class SequenceEvolution(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``SequenceEvolution`` module

    Methods
    -------
    evolve_to_current_time(node)
        Simulate sequence evolution on ``node''
    '''

    @staticmethod
    @abc.abstractmethod
    def evolve_to_current_time(node):
        '''
        Simulate phylogeny evolution on ``node'' until FAVITES_Global.time.

        Should be able to be run in a continuing manner. In other words, if I
        first call ``evolve_to_current_time(node)'' on a node that has not been
        evolved yet, the resulting tree(s) should be from time 0 (root) to the
        current time (i.e., the tree height should be the current time). Then,
        on the same node, if I later call ``evolve_to_current_time(node)'', the
        node's tree(s) should continue from where they left off last time and
        evolve until the current time.

        Parameters
        ----------
        node : ContactNetworkNode
            ``ContactNetworkNode'' object to evolve
        '''
        pass