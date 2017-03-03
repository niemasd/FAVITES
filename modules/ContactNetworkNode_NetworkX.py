#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkNode" module, implemented with NetworkX
'''
from ContactNetworkNode import ContactNetworkNode
from ContactNetwork import ContactNetwork
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class ContactNetworkNode_NetworkX(ContactNetworkNode):
    '''
    Implement the ``ContactNetworkNode`` abstract class using NetworkX

    Attributes
    ----------
    contact_network : ContactNetwork
        The ``ContactNetwork'' object this node is in
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

    def __init__(self, cn, name, num):
        '''
        Construct a new ``ContactNetworkNode_NetworkX`` object

        Parameters
        ----------
        graph : Graph
            The NetworkX graph in which this node exists
        node : Node
            The NetworkX node encapsulated by this object
        '''
        assert isinstance(cn, ContactNetwork), "graph is not a ContactNetwork_NetworkX object"
        assert isinstance(name, str), "name is not a string"
        assert isinstance(num, int), "num is not an integer"
        self.contact_network = cn
        self.name = name
        self.num = num
        if not hasattr(GC, 'viruses'):
            GC.viruses = {}
        if self.num not in GC.viruses:
            GC.viruses[self.num] = set()

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other.name

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_attribute(self):
        return self.contact_network.contact_network.node[self.num]['attribute']

    def get_contact_network(self):
        return self.contact_network

    def get_infections(self):
        return self.contact_network.contact_network.node[self.num]['infections']

    def num_infections(self):
        return len(self.get_infections())

    def infect(self, time, virus):
        assert isinstance(time, float)
        assert isinstance(virus, MF.module_abstract_classes['TreeNode'])
        assert time == virus.get_time(), "Virus time and transmission time do not match!"
        self.contact_network.contact_network.node[self.num]['infections'].append((time, virus))
        virus.set_contact_network_node(self)
        self.add_virus(virus)
        self.contact_network.add_to_infected(self)

    def is_infected(self):
        return len(GC.viruses[self.num]) != 0

    def add_virus(self, virus):
        assert virus.get_contact_network_node() == self, "Cannot add a virus to a node it's not in"
        GC.viruses[self.num].add(virus.get_label())

    def remove_virus(self, virus):
        assert virus.get_contact_network_node() == self, "Cannot remove a virus from a node it's not in"
        GC.viruses[self.num].remove(virus.get_label())

    def viruses(self):
        for virus in GC.viruses[self.num]:
            yield GC.label_to_node[virus]

if __name__ == '__main__':
    '''
    This function is just used for testing purposes. It has no actual function
    in the simulator tool.
    '''
    pass