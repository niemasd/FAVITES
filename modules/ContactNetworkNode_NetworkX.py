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
    first_time : float
        The first time this node was infected
    graph : DiGraph
        The NetworkX DiGraph in which this node exists
    name : str
        The name of this node
    num : int
        The number of this node
    '''

    def cite():
        return GC.CITATION_NETWORKX

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
        if not hasattr(GC, 'first_times'):
            GC.first_times = {}
        if self.num not in GC.first_times:
            GC.first_times[self.num] = None

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.name == other.name

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self.name < other.name

    def __gt__(self, other):
        return self.name > other.name

    def __le__(self, other):
        return self.name <= other.name

    def __ge__(self, other):
        return self.name >= other.name

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    def get_attribute(self):
        return self.contact_network.contact_network.nodes[self.num]['attribute']

    def get_contact_network(self):
        return self.contact_network

    def get_first_infection_time(self):
        return GC.first_times[self.num]

    def get_infections_from(self):
        return self.contact_network.contact_network.nodes[self.num]['infections_from']

    def get_infections_to(self):
        return self.contact_network.contact_network.nodes[self.num]['infections_to']

    def num_infections(self):
        return len(self.get_infections())

    def infect(self, time, virus):
        assert isinstance(time, float)
        assert isinstance(virus, MF.module_abstract_classes['TreeNode'])
        assert time == virus.get_time(), "Virus time and transmission time do not match!"
        if GC.first_times[self.num] is None:
            GC.first_times[self.num] = time
        self.contact_network.contact_network.nodes[self.num]['infections_to'].append((time, virus))
        source = virus.get_contact_network_node()
        self.contact_network.contact_network.nodes[source.num]['infections_from'].append((time, self))
        virus.set_contact_network_node(self)
        GC.virus_history[virus.get_label()].append((time,self))
        self.add_virus(virus)
        self.contact_network.add_to_infected(self)

    def is_infected(self):
        return len(GC.viruses[self.num]) != 0

    def add_virus(self, virus):
        assert virus.get_contact_network_node() == self, "Cannot add a virus to a node it's not in"
        GC.viruses[self.num].add(virus.get_label())
        self.contact_network.add_to_infected(self)

    def remove_virus(self, virus):
        assert virus.get_contact_network_node() == self, "Cannot remove a virus from a node it's not in"
        GC.viruses[self.num].remove(virus.get_label())
        if len(GC.viruses[self.num]) == 0:
            self.contact_network.remove_from_infected(self)

    def viruses(self):
        for virus in GC.viruses[self.num]:
            yield GC.label_to_node[virus]

    def uninfect(self):
        GC.viruses[self.num] = set()
        self.contact_network.remove_from_infected(self)

if __name__ == '__main__':
    '''
    This function is just used for testing purposes. It has no actual function
    in the simulator tool.
    '''
    pass
