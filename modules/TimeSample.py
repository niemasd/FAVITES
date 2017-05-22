#! /usr/bin/env python3
'''
Niema Moshiri 2017

"TimeSample" module
'''
import abc

class TimeSample(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``TimeSample`` module

    Methods
    -------
    init()
        Initialize the module (if need be)
    sample_times(node, num_times)
        Return a list of times at which the given node was sampled
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
    def sample_times(node, num_times):
        '''
        Return a list of times at which the given node was sampled

        Parameters
        ----------
        node : ContactNetworkNode
            The ``ContactNetworkNode'' we want to get sample times for
        num_times : int
            The number of sample times we want to get

        Returns
        -------
        times : list of float
            A list of times at which the given node was sampled
        '''
        pass