#! /usr/bin/env python3
'''
Niema Moshiri 2016

"EndCriteria" module
'''
import abc # for abstraction

class EndCriteria(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``EndCriteria`` module

    Methods
    -------
    done()
        Returns True if this simulation is done, or False otherwise
    finalize_time()
        Finalize the global time
    not_done()
        Returns True if this simulation is not done, or False otherwise
    '''

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