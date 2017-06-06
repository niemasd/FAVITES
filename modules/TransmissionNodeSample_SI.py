#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionNodeSample" module, where transmissions follow the SI model
'''
from TransmissionNodeSample import TransmissionNodeSample
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from random import choice

class TransmissionNodeSample_SI(TransmissionNodeSample):
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
        assert "TransmissionTimeSample_SI" in str(MF.modules['TransmissionTimeSample']), "Must use TransmissionTimeSample_SI module"
        # handle parameter checking in TransmissionTimeSample_SI

    def sample_nodes(time):
        assert GC.next_trans is not None, "Must call TransmissionTimeSample_SI before TransmissionNodeSample_SI"
        u,v,t = GC.next_trans
        assert not v.is_infected(), "Destination virus is already infected"
        GC.next_trans = None
        for edge in GC.contact_network.get_edges_from(v):
            neighbor = edge.get_to()
            if not neighbor.is_infected():
                infected_neighbors = [edge.get_from() for edge in GC.contact_network.get_edges_to(neighbor) if edge.get_from().is_infected()]
                infected_neighbors.append(v)
                infector = choice(infected_neighbors)
                time = t + exponential(scale=1/(GC.infection_rate*len(infected_neighbors))) # min of exponentials is exponential with sum of rates
                if neighbor in GC.trans_pq_v2trans:
                    GC.trans_pq.removeFirst(neighbor)
                GC.trans_pq.put(neighbor,time)
                GC.trans_pq_v2trans[neighbor] = (infector,neighbor,time)
        return u,v