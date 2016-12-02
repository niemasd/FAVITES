#! /usr/bin/env python3
'''
Niema Moshiri 2016

"PostValidation" module
'''
import abc # for abstraction

class PostValidation(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``PostValidation`` module

    Methods
    -------
    score_transmission_network()
        Score the error-free transmission network
    '''

    @staticmethod
    @abc.abstractmethod
    def score_transmission_network():
        '''
        Score the error-free transmission network

        Returns
        -------
        score : float
            Score of the error-free transmission network
        '''
        pass