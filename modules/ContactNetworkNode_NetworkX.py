#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkNode" module, implemented with NetworkX
'''
from ContactNetworkNode import ContactNetworkNode # abstract ContactNetworkNode class
import FAVITES_GlobalContext as GC
import modules.FAVITES_ModuleFactory as MF
from networkx import DiGraph                              # to validate graph

class ContactNetworkNode_NetworkX(ContactNetworkNode):
    '''
    Implement the ``ContactNetworkNode`` abstract class using NetworkX

    Attributes
    ----------
    graph : DiGraph
        The NetworkX DiGraph in which this node exists
    infected : bool
        True if this node is infected, otherwise False
    name : str
        The name of this node
    num : int
        The number of this node
    '''
    
    def init():
        pass

    def __init__(self, graph, name, num):
        '''
        Construct a new ``ContactNetworkNode_NetworkX`` object

        Parameters
        ----------
        graph : Graph
            The NetworkX graph in which this node exists
        node : Node
            The NetworkX node encapsulated by this object
        '''
        assert isinstance(graph, DiGraph), "graph is not a NetworkX DiGraph"
        assert isinstance(name, str), "name is not a string"
        assert isinstance(num, int), "num is not an integer"
        self.graph = graph
        self.name = name
        self.num = num
        self.infected = False
        if not hasattr(GC, 'viruses'):
            GC.viruses = {}
        GC.viruses[self.num] = set()

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_attribute(self):
        return self.graph.node[self.num]['attribute']

    def get_infections(self):
        return self.graph.node[self.num]['infections']

    def num_infections(self):
        return len(self.get_infections())

    def infect(self, time, virus):
        assert isinstance(time, float)
        assert isinstance(virus, MF.module_abstract_classes['TreeNode'])
        assert time == virus.get_time(), "Virus time and transmission time do not match!"
        TreeNode = MF.modules['TreeNode']
        self.graph.node[self.num]['infections'].append((time, virus))
        virus.set_contact_network_node(self)
        GC.viruses[self.num].add(virus)
        self.infected = True

    def is_infected(self):
        return self.infected

    def add_virus(self, virus):
        assert virus.get_contact_network_node() == self, "Cannot add a virus to a node it's not in"
        GC.viruses[self.num].add(virus)

    def remove_virus(self, virus):
        assert virus.get_contact_network_node() == self, "Cannot remove a virus from a node it's not in"
        GC.viruses[self.num].remove(virus)

    def viruses(self):
        for virus in GC.viruses[self.num]:
            yield virus

if __name__ == '__main__':
    '''
    This function is just used for testing purposes. It has no actual function
    in the simulator tool.
    '''
    pass