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
    infect(node)
        Infect ``node'' with an initial seed sequence(s)
    '''

    @staticmethod
    @abc.abstractmethod
    def generate(node):
        '''
        Generate an initial seed sequence(s). Will probably want to use
        FAVITES_Global.seed_sequence_length.
        '''
        pass