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

class ContactNetwork_NetworkX(ContactNetwork):
    '''
    Implement the ``ContactNetwork`` abstract class using NetworkX
    '''
    def __init__(self, edge_list):
        # set up NetworkX and graph
        import networkx as nx
        self.contact_network = nx.Graph()
        self.name_to_num = {}
        self.num_to_name = []

        # read in Contact Network as edge list
        for line in edge_list:
            u,v = line.split('\t')
            if u not in self.name_to_num:
                self.contact_network.add_node(len(self.num_to_name))
                self.name_to_num[u] = len(self.num_to_name)
                self.num_to_name.append(u)
            if v not in self.name_to_num:
                self.contact_network.add_node(len(self.num_to_name))
                self.name_to_num[v] = len(self.num_to_name)
                self.num_to_name.append(v)
            self.contact_network.add_edge(self.name_to_num[u],self.name_to_num[v])

    def num_nodes(self):
        return self.contact_network.number_of_nodes()

    def num_edges(self):
        return self.contact_network.number_of_edges()

    def nodes_iter(self):
        return self.contact_network.nodes()

    def edges_iter(self):
        return self.contact_network.edges()

def check():
    '''
    Check all ``ContactNetwork`` classes for validity
    '''
    print("--- Testing ContactNetwork Module ---")

    # Test ContactNetwork_NetworkX class
    print("ContactNetwork_NetworkX class: "),
    g = ContactNetwork_NetworkX(['A\tB','A\tC','B\tC','A\tD','C\tD'])
    status = "Success"
    if not isinstance(g, ContactNetwork):
        status = "Failure"
    elif g.num_nodes() != 4:
        status = "Failure"
    elif g.num_edges() != 5:
        status = "Failure"
    print(status)

if __name__ == '__main__':
    '''
    This function is just used for testing purposes. It has no actual function
    in the simulator tool.
    '''
    check()