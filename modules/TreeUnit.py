#! /usr/bin/env python3
'''
Niema Moshiri 2017

"TreeUnit" module
'''
import abc

class TreeUnit(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``TreeUnit`` module

    Methods
    -------
    cite()
        Return citation string (or None)
    init()
        Initialize the module (if need be)
    time_to_mutation_rate(tree)
        Convert the branches of ``tree`` to be in units of mutation rate instead
        of units of time
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
    def time_to_mutation_rate(tree):
        '''
        Convert the branches of ``tree`` to be in units of mutation rate instead
        of units of time

        Parameters
        ----------
        tree : str
            The tree to be converted (in Newick format)
        '''
        pass