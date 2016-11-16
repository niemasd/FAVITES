#! /usr/bin/env python
'''
Niema Moshiri 2016

"ContactNetwork" module, which will contain the Transmission Network information
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
    transmissions()
        Return a list of (u,v,time) transmission events that have happened
    num_edges()
        Return the number of edges in this ``ContactNetwork``
    num_infected_nodes()
        Return the number of infected nodes in this ``ContactNetwork``
    num_nodes()
        Return the number of nodes in this ``ContactNetwork``
    num_transmissions()
        Return the number of transmission events that have happened thus far
    num_uninfected_nodes()
        Return the number of uninfected nodes in this ``ContactNetwork``

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
    def num_infected_nodes(self):
        '''
        Return the number of infected nodes in this `ContactNetwork`

        Returns
        -------
        num_infected_nodes : int
            The number of infected nodes in this `ContactNetwork`

        '''
        pass

    @abstractmethod
    def num_uninfected_nodes(self):
        '''
        Return the number of uninfected nodes in this `ContactNetwork`

        Returns
        -------
        num_uninfected_nodes : int
            The number of uninfected nodes in this `ContactNetwork`

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
    def num_transmissions(self):
        '''
        Return the number of transmission events that have happened thus far

        Returns
        -------
        num_transmissions : int
            The number of transmission events that have happened thus far

        '''
        pass

    @abstractmethod
    def transmissions(self):
        '''
        Return a list of (u,v,time) transmission events that have happened

        Returns
        -------
        num_transmissions : list of (int,int,int) tuples
            A list of (u,v,time) transmission events that have happened

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
        self.name_to_num = {}       # map original node names to numbers
        self.num_to_name = []       # map numbers to original node names
        self.infected_nodes = set() # store numbers of infected nodes
        self.transmissions = []     # store u->v transmission as (u,v,time)

        # read in Contact Network as edge list
        for line in edge_list:
            u,v = line.split('\t') # TODO: PARSE u AND v FOR NODE ATTRIBUTES (e.g. MSM, etc.)
            if u not in self.name_to_num:
                self.contact_network.add_node(len(self.num_to_name))
                self.name_to_num[u] = len(self.num_to_name)
                self.num_to_name.append(u)
            if v not in self.name_to_num:
                self.contact_network.add_node(len(self.num_to_name))
                self.name_to_num[v] = len(self.num_to_name)
                self.num_to_name.append(v)
            self.contact_network.add_edge(self.name_to_num[u],self.name_to_num[v])

    def num_transmissions(self):
        return len(self.transmissions)

    def num_nodes(self):
        return self.contact_network.number_of_nodes()

    def num_infected_nodes(self):
        return len(self.infected_nodes)

    def num_uninfected_nodes(self):
        return self.contact_network.number_of_nodes() - len(self.infected_nodes)

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