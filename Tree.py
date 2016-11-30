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
    None

    '''

    @abc.abstractmethod
    def __init__(self):
        '''
        Construct a new ``Tree`` object
        '''
        pass