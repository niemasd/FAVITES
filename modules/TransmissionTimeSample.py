#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionTimeSample" module
'''
import abc # for abstraction

class TransmissionTimeSample(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``TransmissionTimeSample`` module

    Methods
    -------
    init()
        Initialize the module (if need be)
    sample_time()
        Returns the time of the next transmission event
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
    def sample_time():
        '''
        Returns the time of the next transmission event

        Returns
        -------
        time : float
            Time of the transmission event (in seconds from time = 0)
        '''
        pass