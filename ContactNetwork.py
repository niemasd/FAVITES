#! /usr/bin/env python
'''
Niema Moshiri 2016

"ContactNetwork" module
'''
from abc import ABCMeta, abstractmethod # for abstraction

class ContactNetwork:
    '''
    Abstract class defining a ``ContactNetwork`` object

    Attributes
    ----------
    None

    Methods
    -------
    edges_iter()
        perform an iteration over the edges in this ``ContactNetwork``
    nodes_iter()
        Perform an iteration over the nodes in this ``ContactNetwork``
    num_nodes()
        Return the number of nodes in this ``ContactNetwork``
    num_edges()
        Return the number of edges in this ``ContactNetwork``

    '''
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, edge_list):
        '''
        Construct a new ``ContactNetwork`` object

        Parameters
        ----------
        edge_list : list of str
            The Contact Network from which to create this ``ContactNetwork``
            object, where each line is a single edge in the specified edge-list
            input format (see framework README)

        '''
        pass

    @abstractmethod
    def num_nodes(self):
        '''
        Return the number of nodes in this `ContactNetwork`

        Returns
        -------
        num_nodes : int
            The number of nodes in this `ContactNetwork`

        '''
        pass

    @abstractmethod
    def num_edges(self):
        '''
        Return the number of edges in this `ContactNetwork`

        Returns
        -------
        num_edges : int
            The number of edges in this `ContactNetwork`

        '''
        pass

    @abstractmethod
    def nodes_iter(self):
        '''
        Perform an iteration over the nodes in this ``ContactNetwork``

        Returns
        -------
        :py:class:`collections.Iterator` [|NetworkNode|]
            An iterator yielding nodes in this `ContactNetwork`

        '''
        pass

    @abstractmethod
    def edges_iter(self):
        '''
        Perform an iteration over the edges in this ``ContactNetwork``

        Returns
        -------
        :py:class:`collections.Iterator` [|NetworkEdge|]
            An iterator yielding edges in this `ContactNetwork`

        '''
        pass

def check():
    '''
    Check all ContactNetwork classes for validity
    '''
    pass

if __name__ == '__main__':
    '''
    This function is just used for testing purposes. It has no actual function
    in the simulator tool.
    '''
    check()