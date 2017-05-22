#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetwork" module, using the PANGEA HIV Simulation Model
(https://github.com/olli0601/PANGEA.HIV.sim)
'''
from ContactNetwork import ContactNetwork
from ContactNetworkEdge_PANGEA import ContactNetworkEdge_PANGEA as Edge
from ContactNetworkNode_PANGEA import ContactNetworkNode_PANGEA as Node
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class ContactNetwork_PANGEA(ContactNetwork):
    def init():
        assert "ContactNetwork_PANGEA" in str(MF.modules['ContactNetwork']), "Must use ContactNetwork_PANGEA module"
        assert "ContactNetworkGenerator_PANGEA" in str(MF.modules['ContactNetworkGenerator']), "Must use ContactNetworkGenerator_PANGEA module"
        assert "EndCriteria_Instant" in str(MF.modules['EndCriteria']), "Must use EndCriteria_Instant module"
        assert "NodeEvolution_PANGEA" in str(MF.modules['NodeEvolution']), "Must use NodeEvolution_PANGEA module"
        assert "NodeSample_PANGEA" in str(MF.modules['NodeSample']), "Must use NodeSample_PANGEA module"
        assert "NumBranchSample_All" in str(MF.modules['NumBranchSample']), "Must use NumBranchSample_All module"
        assert "PostValidation_Dummy" in str(MF.modules['PostValidation']), "Must use PostValidation_Dummy module"
        assert "SeedSelection_PANGEA" in str(MF.modules['SeedSelection']), "Must use SeedSelection_PANGEA module"
        assert "SeedSequence_PANGEA" in str(MF.modules['SeedSequence']), "Must use SeedSequence_PANGEA module"
        assert "SequenceEvolution_PANGEA" in str(MF.modules['SequenceEvolution']), "Must use SequenceEvolution_PANGEA module"
        assert "SourceSample_PANGEA" in str(MF.modules['SourceSample']), "Must use SourceSample_PANGEA module"
        assert "TimeSample_PANGEA" in str(MF.modules['TimeSample']), "Must use TimeSample_PANGEA module"
        assert "TransmissionNodeSample_PANGEA" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_PANGEA module"
        assert "TransmissionTimeSample_PANGEA" in str(MF.modules['TransmissionTimeSample']), "Must use TransmissionTimeSample_PANGEA module"

    def __init__(self, edge_list=None):
        if hasattr(GC,'PANGEA_TRANSMISSION_NETWORK'):
            self.transmissions = [(Node(None,u,None), Node(None,v,None), float(t)) for u,v,t in GC.PANGEA_TRANSMISSION_NETWORK]
            self.nodes = set()
            for u,v,t in self.transmissions:
                self.nodes.add(u)
                self.nodes.add(v)
            tmp = {(u,v) for u,v,t in self.transmissions}
            self.edges = set()
            for u,v in tmp:
                self.edges.add(Edge(u,v,None))
                self.edges.add(Edge(v,u,None))

    def num_transmissions(self):
        return None

    def num_nodes(self):
        return None

    def get_nodes(self):
        return set()

    def get_node(self, name):
        return None

    def num_infected_nodes(self):
        return None

    def get_infected_nodes(self):
        return set()

    def num_uninfected_nodes(self):
        return None

    def get_uninfected_nodes(self):
        return set()

    def num_edges(self):
        return None

    def nodes_iter(self):
        for node in self.nodes:
            yield node

    def edges_iter(self):
        for edge in self.edges:
            yield edge

    def get_edges_from(self, node):
        return []

    def get_edges_to(self,node):
        return []

    def get_transmissions(self):
        return self.transmissions

    def add_transmission(self,u,v,time):
        pass

    def add_to_infected(self,node):
        pass

    def remove_from_infected(self,node):
        pass