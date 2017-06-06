#! /usr/bin/env python3
'''
Niema Moshiri 2017

"NumTimeSample" module
'''
import abc

class NumTimeSample(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``NumTimeSample`` module

    Methods
    -------
    cite()
        Return citation string (or None)
    init()
        Initialize the module (if need be)
    sample_num_times(node)
        Sample a number of sampling events the given individual will undergo
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
    def sample_num_times(node):
        '''
        Sample a number of sampling events the given individual will undergo

        Parameters
        ----------
        node : ContactNetworkNode
            The ``ContactNetworkNode'' for which we want to get a number of
            viruses to sample

        Returns
        -------
        num_times : int
            The number of samplig events the given individual will undergo
        '''
        pass