#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSequence" module
'''
import abc # for abstraction

class SeedSequence(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``SeedSequence`` module

    Methods
    -------
    evolve(node)
        Evolve a phylogeny and sequences on ``node''
    '''

    @abc.abstractmethod
    def evolve(node):
        '''
        Evolve a phylogeny and sequences on ``node''

        Parameters
        ----------
        node : ContactNetworkNode
            ``ContactNetworkNode'' object on which to evolve phylogeny and
            sequences

        '''
        pass