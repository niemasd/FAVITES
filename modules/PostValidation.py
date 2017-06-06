#! /usr/bin/env python3
'''
Niema Moshiri 2016

"PostValidation" module
'''
import abc

class PostValidation(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``PostValidation`` module

    Methods
    -------
    cite()
        Return citation string (or None)
    init()
        Initialize the module (if need be)
    score_phylogenetic_tree(tree)
        Score phylogenetic tree ``tree''
    score_sequences(seqs)
        Score sequence data ``seqs''
    score_transmission_network()
        Score the transmission network
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

    @abc.abstractmethod
    def score_transmission_network():
        '''
        Score the transmission network

        Returns
        -------
        score : float
            Score of ``network''
        '''
        pass

    @abc.abstractmethod
    def score_phylogenetic_tree(tree):
        '''
        Score phylogenetic tree ``tree''

        Parameters
        ----------
        tree : str
            Phylogenetic tree as a Newick string

        Returns
        -------
        score : float
            Score of ``tree''
        '''
        pass

    @abc.abstractmethod
    def score_sequences(seqs):
        '''
        Score sequence data ``seqs''

        Parameters
        ----------
        seqs : list of str
            Sequence data to score

        Returns
        -------
        score : float
            Score of ``tree''
        '''
        pass