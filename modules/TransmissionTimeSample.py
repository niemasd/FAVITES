#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionTimeSample" module
'''
import abc

class TransmissionTimeSample(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``TransmissionTimeSample`` module

    Methods
    -------
    cite()
        Return citation string (or None)
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
    def sample_time():
        '''
        Returns the time of the next transmission event

        Returns
        -------
        time : float
            Time of the transmission event (in seconds from time = 0)
        '''
        pass