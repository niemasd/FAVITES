#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetwork" module, which will contain the Transmission Network information
'''
import abc

class ContactNetwork(metaclass=abc.ABCMeta):
    '''
    Abstract class defining a ``ContactNetwork'' object

    Methods
    -------
    add_to_infected(node)
        Remove ``node'' from the uninfected nodes and add it to the infected
        nodes
    add_transmission(u,v,time)
        Add transmission event (u,v,time) to this ``ContactNetwork''
    cite()
        Return citation string (or None)
    edges_iter()
        Perform an iteration over the edges in this ``ContactNetwork''
    get_edges_from(node)
        Return a list of edges leaving ``node''
    get_edges_to(node)
        Return a list of edges entering ``node''
    get_infected_nodes()
        Return a set of all infected nodes in this ``ContactNetwork''
    get_node(name)
        Return the node with the given name (or None if ``name'' is None)
    get_nodes()
        Return a set of all nodes in this ``ContactNetwork''
    get_uninfected_nodes()
        Return a set of all uninfected nodes in this ``ContactNetwork''
    get_transmissions()
        Return a list of (u,v,time) transmission events that have happened
    init()
        Initialize the module (if need be)
    nodes_iter()
        Perform an iteration over the nodes in this ``ContactNetwork''
    num_edges()
        Return the number of edges in this ``ContactNetwork''
    num_infected_nodes()
        Return the number of infected nodes in this ``ContactNetwork''
    num_nodes()
        Return the number of nodes in this ``ContactNetwork''
    num_transmissions()
        Return the number of transmission events that have happened thus far
    num_uninfected_nodes()
        Return the number of uninfected nodes in this ``ContactNetwork''
    remove_from_infected(node)
        Remove ``node'' from the infected nodes and add it to the uninfected
        nodes
    '''

    @abc.abstractmethod
    def __init__(self, edge_list=None):
        '''
        Construct a new ``ContactNetwork'' object

        Parameters
        ----------
        edge_list : list of str
            The Contact Network from which to create this ``ContactNetwork''
            object, where each element is a single edge in the specified
            edge-list input format (see framework README)
        '''
        pass

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
    def get_node(self, name):
        '''
        Return the node with the given name (or None if ``name'' is None)

        Returns
        -------
        node : ContactNetworkNode
            The node with the given name (or None if ``name'' is None)
        '''
        pass

    @abc.abstractmethod
    def get_nodes(self):
        '''
        Return a set of all nodes in this `ContactNetwork`

        Returns
        -------
        nodes : set of ContactNetworkNode
            A set of all nodes in this `ContactNetwork`
        '''
        pass

    @abc.abstractmethod
    def num_nodes(self):
        '''
        Return the number of nodes in this `ContactNetwork`

        Returns
        -------
        num_nodes : int
            The number of nodes in this `ContactNetwork`
        '''
        pass

    @abc.abstractmethod
    def num_infected_nodes(self):
        '''
        Return the number of infected nodes in this `ContactNetwork`

        Returns
        -------
        num_infected_nodes : int
            The number of infected nodes in this `ContactNetwork`
        '''
        pass

    @abc.abstractmethod
    def get_infected_nodes(self):
        '''
        Return a set of all infected nodes in this `ContactNetwork`

        Returns
        -------
        infected_nodes : set of ContactNetworkNode
            A set of all infected nodes in this `ContactNetwork`
        '''
        pass

    @abc.abstractmethod
    def num_uninfected_nodes(self):
        '''
        Return the number of uninfected nodes in this `ContactNetwork`

        Returns
        -------
        num_uninfected_nodes : int
            The number of uninfected nodes in this `ContactNetwork`
        '''
        pass

    @abc.abstractmethod
    def get_uninfected_nodes(self):
        '''
        Return a set of all uninfected nodes in this `ContactNetwork`

        Returns
        -------
        uninfected_nodes : set of ContactNetworkNode
            A set of all uninfected nodes in this `ContactNetwork`
        '''
        pass

    @abc.abstractmethod
    def num_edges(self):
        '''
        Return the number of edges in this `ContactNetwork`

        Returns
        -------
        num_edges : int
            The number of edges in this `ContactNetwork`
        '''
        pass

    @abc.abstractmethod
    def get_edges_from(self, node):
        '''
        Return a list of edges leaving ``node''

        Returns
        -------
        edges : list of ContactNetworkEdge
            A list of edges leaving ``node''
        '''
        pass

    @abc.abstractmethod
    def get_edges_to(self, node):
        '''
        Return a list of edges entering ``node''

        Returns
        -------
        edges : list of ContactNetworkEdge
            A list of edges entering ``node''
        '''
        pass

    @abc.abstractmethod
    def add_transmission(self,u,v,time):
        '''
        Add transmission event (u,v,time) to this ``ContactNetwork''

        Parameters
        ----------
        u : ContactNetworkNode
            The source of this transmission event
        v : ContactNetworkNode
            The target of this transmission event
        time : float
            Time of the transmission event (in seconds from time = 0)
        '''
        pass

    @abc.abstractmethod
    def num_transmissions(self):
        '''
        Return the number of transmission events that have happened thus far

        Returns
        -------
        num_transmissions : int
            The number of transmission events that have happened thus far
        '''
        pass

    @abc.abstractmethod
    def get_transmissions(self):
        '''
        Return a list of (u,v,time) transmission events that have happened

        Returns
        -------
        transmissions : list of (int,int,float) tuples
            A list of (u,v,time) transmission events that have happened
        '''
        pass

    @abc.abstractmethod
    def nodes_iter(self):
        '''
        Perform an iteration over the nodes in this ``ContactNetwork''

        Returns
        -------
        :py:class:`collections.Iterator` [|NetworkNode|]
            An iterator yielding nodes in this `ContactNetwork`
        '''
        pass

    @abc.abstractmethod
    def edges_iter(self):
        '''
        Perform an iteration over the edges in this ``ContactNetwork''

        Returns
        -------
        :py:class:`collections.Iterator` [|NetworkEdge|]
            An iterator yielding edges in this `ContactNetwork`
        '''
        pass

    @abc.abstractmethod
    def add_to_infected(self, node):
        '''
        Remove ``node'' from the uninfected nodes and add it to the infected
        nodes

        Parameters
        ----------
        node : ContactNetworkNode
            The node to move
        '''
        pass

    @abc.abstractmethod
    def remove_from_infected(self, node):
        '''
        Remove ``node'' from the infected nodes and add it to the uninfected
        nodes

        Parameters
        ----------
        node : ContactNetworkNode
            The node to move
        '''
        pass