#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SequencingError" module
'''
import abc # for abstraction

class SequencingError(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``SequencingError`` module

    Methods
    -------
    introduce_sequencing_error(node)
        Return a FASTQ format string representing realistic sequencing reads
    '''

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