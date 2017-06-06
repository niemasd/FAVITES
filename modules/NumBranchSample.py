#! /usr/bin/env python3
'''
Niema Moshiri 2017

"NumBranchSample" module
'''
import abc

class NumBranchSample(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``NumBranchSample`` module

    Methods
    -------
    cite()
        Return citation string (or None)
    init()
        Initialize the module (if need be)
    sample_num_branches(node, time)
        Sample a number of viral branches to sample during an individual's
        virus sampling at a given time
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
    def sample_num_branches(node, time):
        '''
        Sample a number of viral branches to sample during an individual's
        virus sampling

        Parameters
        ----------
        node : ContactNetworkNode
            The ``ContactNetworkNode'' for which we want to get a number of
            viruses to sample
        time : float
            The time at which the individual is being sampled

        Returns
        -------
        num_branches : int
            The number of viruses (i.e., phylogeny branches) to sample
        '''
        pass