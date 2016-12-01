#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Tree" module
'''
import abc # for abstraction

class Tree(metaclass=abc.ABCMeta): # TODO: Everything (define all functions)
    '''
    Abstract class defining a ``Tree`` object

    Methods
    -------
    get_end_time()
        Return the end time to which this ``Tree'' has been evolved. In other
        words, return the height of the tree in unit of time

    '''

    @abc.abstractmethod
    def __init__(self):
        '''
        Construct a new ``Tree`` object
        '''
        pass

    @abc.abstractmethod
    def get_end_time():
        '''
        Return the end time to which this ``Tree'' has been evolved. In other
        words, return the height of the tree in unit of time

        Returns
        -------
        end_time : int
            The end time to which this ``Tree'' has been evolved
        '''
        pass