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
    infect(user_input, node)
        Infect ``node'' with an initial seed sequence(s)
    '''

    @abc.abstractmethod
    def infect(user_input, node):
        '''
        Infect ``node'' with an initial seed sequence(s)

        Parameters
        ----------
        user_input : dict
            ``user_input'' parsed by ``Driver''
        node : ContactNetworkNode
            ``ContactNetworkNode'' object to infect with seed sequence(s)

        '''
        pass