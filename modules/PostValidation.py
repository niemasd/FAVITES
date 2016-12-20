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
    score_phylogenetic_tree(tree)
        Score phylogenetic tree ``tree''
    score_sequences(seqs)
        Score sequence data ``seqs''
    score_transmission_network()
        Score the transmission network
    '''

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