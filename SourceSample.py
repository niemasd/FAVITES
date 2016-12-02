#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SourceSample" module
'''
import abc # for abstraction

class SourceSample(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``SourceSample`` module

    Methods
    -------
    sample_virus(node)
        Samples a virus (or viruses) from ``node'' at FAVITES_Global.time.
    '''

    @staticmethod
    @abc.abstractmethod
    def sample_virus(node):
        '''
        Samples a virus (or viruses) from ``node'' at FAVITES_Global.time.

        Parameters
        ----------
        node : ContactNetworkNode
            The node that is to be sampled

        Returns
        -------
        NOT SURE WHAT TO RETURN!!!!
        '''
        pass