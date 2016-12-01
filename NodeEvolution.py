#! /usr/bin/env python3
'''
Niema Moshiri 2016

"NodeEvolution" module
'''
import abc # for abstraction

class NodeEvolution(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``NodeEvolution`` module

    Methods
    -------
    evolve(node)
        Simulate phylogeny evolution on ``node''
    '''

    @staticmethod
    @abc.abstractmethod
    def evolve_to_time(node, time):
        '''
        Simulate phylogeny evolution on ``node'' until time ``time''.

        Should be able to be run in a continuing manner. In other words, if I
        first call ``evolve_to_time(node,t1)'' on a node that has not been
        evolved yet, the resulting tree(s) should be from time 0 (root) to time
        t1 (i.e., the tree height should be t1 in units of time). Then, on the
        same node, if I later call ``evolve_to_time(node,t2)'', the node's
        tree(s) should continue from where they left off (t1) and evolve until
        time t2 (i.e., the tree height should now be t1+t2 in units of time, and
        the subtree from time 0 to t1 should be unchanged).

        Parameters
        ----------
        node : ContactNetworkNode
            ``ContactNetworkNode'' object to evolve
        time : int
            Time until which the tree(s) in ``node'' should be evolved
        '''
        pass