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
    def generate(node):
        '''
        Generate an initial seed sequence(s). Will probably want to use
        FAVITES_Global.seed_sequence_length.
        '''
        pass