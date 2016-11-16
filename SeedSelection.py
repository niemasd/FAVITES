'''
Niema Moshiri 2016

"SeedSelection" module
'''
from abc import ABCMeta, abstractmethod # for abstraction

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
    __metaclass__ = ABCMeta