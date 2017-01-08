#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Driver" module
'''
import abc # for abstraction

class Driver(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``Driver`` module

    Methods
    -------
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