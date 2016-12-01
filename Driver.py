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
    run()
        Run the simulation
    '''

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