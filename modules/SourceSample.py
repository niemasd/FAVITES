#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SourceSample" module
'''
import abc

class SourceSample(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``SourceSample`` module

    Methods
    -------
    cite()
        Return citation string (or None)
    init()
        Initialize the module (if need be)
    sample_virus(node)
        Samples a virus (or viruses) from ``node`` at
        ``FAVITES_GlobalContext.time``.
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
    def sample_virus(node):
        '''
        Samples a virus (or viruses) from ``node`` at
        ``FAVITES_GlobalContext.time``.

        Parameters
        ----------
        node : ContactNetworkNode
            The node that is to be sampled

        Returns
        -------
        virus : TreeNode
            A ``TreeNode`` object representing the virus sampled from ``node``
            at ``FAVITES_GlobalContext.time``.
        '''
        pass