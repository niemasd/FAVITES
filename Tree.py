#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Tree" module
'''
import abc # for abstraction

class Tree:
    '''
    Abstract class defining a ``Tree`` object

    Attributes
    ----------
    None

    Methods
    -------
    None

    '''
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        '''
        Construct a new ``Tree`` object
        '''
        pass