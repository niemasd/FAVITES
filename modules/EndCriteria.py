#! /usr/bin/env python3
'''
Niema Moshiri 2016

"EndCriteria" module
'''
import abc

class EndCriteria(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``EndCriteria`` module

    Methods
    -------
    cite()
        Return citation string (or None)
    done()
        Returns True if this simulation is done, or False otherwise
    finalize_time()
        Finalize the global time
    init()
        Initialize the module (if need be)
    not_done()
        Returns True if this simulation is not done, or False otherwise
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
    def done():
        '''
        Returns True if this simulation is done, or False otherwise

        Returns
        -------
        done : bool
            True if this simulation is done, or False otherwise
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    def finalize_time():
        '''
        Finalize the global time
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    def not_done():
        '''
        Returns True if this simulation is not done, or False otherwise

        Returns
        -------
        done : bool
            True if this simulation is not done, or False otherwise
        '''
        pass