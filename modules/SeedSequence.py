#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSequence" module
'''
import abc

class SeedSequence(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``SeedSequence`` module

    Methods
    -------
    cite()
        Return citation string (or None)
    init()
        Initialize the module (if need be)
    merge_trees()
        Merge cluster trees with seed tree (if need be)
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
    def cite():
        '''
        Return citation string (or None)

        Returns
        -------
        citation : str
            The citation string (or None)
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

    @staticmethod
    @abc.abstractmethod
    def merge_trees():
        '''
        Merge cluster trees with seed tree (if need be)

        Returns
        -------
        trees : set of str
            The merged tree(s) (set to allow for multiple trees)
        '''
        pass
