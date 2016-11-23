#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSelection" module
'''
import abc # for abstraction

class SeedSelection:
    '''
    Abstract class defining a ``SeedSelection`` object

    Attributes
    ----------
    None

    Methods
    -------
    edges_iter()
        perform an iteration over the edges in this ``ContactNetwork``

    '''
    __metaclass__ = abc.ABCMeta