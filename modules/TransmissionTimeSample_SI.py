#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionTimeSample" module, where transmissions follow the SI model
'''
from TransmissionTimeSample import TransmissionTimeSample
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from random import choice

class TransmissionTimeSample_SI(TransmissionTimeSample):
    def cite():
        return GC.CITATION_NUMPY

    def init():
        try:
            global exponential
            from numpy.random import exponential
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading Numpy. Install with: pip3 install numpy"
        assert "TransmissionNodeSample_SI" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_SI module"
        GC.infection_rate = float(GC.infection_rate)
        assert GC.infection_rate > 0, "infection_rate must be positive"
        GC.trans_pq = None
        GC.trans_pq_v2trans = None

    def sample_time():
        # no more nodes to infect
        if GC.contact_network.num_uninfected_nodes() == 0:
            GC.next_trans = None
            GC.end_time = GC.time
            return None
        # create priority queue
        if GC.trans_pq is None:
            GC.trans_pq = GC.SortedLinkedList()
            GC.trans_pq_v2trans = dict()
            GC.trans_susceptible = set()
        # attempt to fill priority queue
        if len(GC.trans_pq) == 0:
            for node in GC.contact_network.get_infected_nodes():
                for edge in GC.contact_network.get_edges_from(node):
                    neighbor = edge.get_to()
                    if not neighbor.is_infected():
                        GC.trans_susceptible.add(neighbor)
            while len(GC.trans_susceptible) > 0:
                v = GC.trans_susceptible.pop()
                infected_neighbors = [edge.get_from() for edge in GC.contact_network.get_edges_to(v) if edge.get_from().is_infected()]
                if len(infected_neighbors) > 0:
                    u = choice(infected_neighbors)
                    t = GC.time + exponential(scale=1/(GC.infection_rate*len(infected_neighbors))) # min of exponentials is exponential with sum of rates
                    GC.trans_pq.put(v,t)
                    GC.trans_pq_v2trans[v] = (u,v,t)
        # if failed to fill priority queue, simulation is done
        if len(GC.trans_pq) == 0:
            GC.next_trans = None
            GC.end_time = GC.time
            return None

        # get next transmission event
        v = GC.trans_pq.getFront()
        u,v,t = GC.trans_pq_v2trans[v]
        GC.next_trans = (u,v,t)
        del GC.trans_pq_v2trans[v]
        return t