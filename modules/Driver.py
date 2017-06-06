#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Driver" module
'''
import abc

class Driver(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``Driver`` module

    Methods
    -------
    cite()
        Return citation string (or None)
    init()
        Initialize the module (if need be)
    run()
        Run the simulation
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
    def run():
        '''
        Run the simulation. Will probably want to make use of FAVITES_Global
        variables.

        Parameters
        ----------
        node : ContactNetworkNode
            ``ContactNetworkNode'' object to evolve
        '''
        pass