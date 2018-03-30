#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionNodeSample" module, where the transmission network is read from a
file
'''
from TransmissionNodeSample import TransmissionNodeSample
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class TransmissionNodeSample_TransmissionFile(TransmissionNodeSample):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        assert "ContactNetworkGenerator_File" in str(MF.modules['ContactNetworkGenerator']), "Must use ContactNetworkGenerator_File module"
        assert "EndCriteria_TransmissionFile" in str(MF.modules['EndCriteria']), "Must use EndCriteria_TransmissionFile module"
        assert "SeedSelection_TransmissionFile" in str(MF.modules['SeedSelection']), "Must use SeedSelection_TransmissionFile module"
        assert "TransmissionTimeSample_TransmissionFile" in str(MF.modules['TransmissionTimeSample']), "Must use TransmissionTimeSample_TransmissionFile module"
        # SeedSelection_TransmissionFile sets everything up

    def sample_nodes(time):
        u,v,t = GC.transmission_file[GC.transmission_num]
        GC.transmission_num += 1
        return GC.contact_network.get_node(u), GC.contact_network.get_node(v)

    def check_contact_network(cn):
        pass