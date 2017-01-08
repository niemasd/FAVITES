#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Sequencing" module
'''
import abc # for abstraction

class Sequencing(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``Sequencing`` module

    Methods
    -------
    init()
        Initialize the module (if need be)
    introduce_sequencing_error(node)
        Return a FASTQ format string representing realistic sequencing reads
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
    def introduce_sequencing_error(node):
        '''
        Return a FASTQ format string representing realistic sequencing reads

        Parameters
        ----------
        node : ContactNetworkNode
            Individual from which you will sample sequencing data

        Returns
        -------
        reads : str
            A FASTQ format string representing realistic sequencing reads
        '''
        pass