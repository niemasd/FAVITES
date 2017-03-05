#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionTimeSample" module, where transmissions follow the SI model
'''
from TransmissionTimeSample import TransmissionTimeSample
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
import queue as Q
from random import choice

class TransmissionTimeSample_SI(TransmissionTimeSample):
    def init():
        global exponential
        from numpy.random import exponential
        assert "TransmissionNodeSample_SI" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_SI module"
        GC.infection_rate = float(GC.infection_rate)
        assert GC.infection_rate > 0, "infection_rate must be positive"
        GC.trans_pq = None

    def sample_time():
        if GC.contact_network.num_uninfected_nodes() == 0:
            GC.next_trans = None
            GC.end_time = GC.time
            return None
        # fill priority queue of infection events if empty (if possible)
        if GC.trans_pq is None:
            GC.trans_pq = Q.PriorityQueue()
            susceptible = set()
            for node in GC.contact_network.get_infected_nodes():
                for edge in GC.contact_network.get_edges_from(node):
                    neighbor = edge.get_to()
                    if not neighbor.is_infected():
                        susceptible.add(neighbor)
            for v in susceptible:
                infected_neighbors = [edge.get_from() for edge in GC.contact_network.get_edges_to(v) if edge.get_from().is_infected()]
                if len(infected_neighbors) > 0:
                    u = choice(infected_neighbors)
                    t = GC.time + exponential(scale=1/(GC.infection_rate*len(infected_neighbors))) # min of exponentials is exponential with sum of rates
                    GC.trans_pq.put((t,(u,v,t)))

        # get next transmission event
        u,v,t = GC.trans_pq.get()[1]
        while v.is_infected():
            u,v,t = GC.trans_pq.get()[1]
        GC.next_trans = (u,v,t)
        return t