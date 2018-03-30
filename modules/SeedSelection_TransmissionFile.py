#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSelection" module, where the transmission network is read from a file

Seed nodes are passed in via the "seed_file" parameter of the configuration file
'''
from SeedSelection import SeedSelection
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from os.path import expanduser

class SeedSelection_TransmissionFile(SeedSelection):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        assert "ContactNetworkGenerator_File" in str(MF.modules['ContactNetworkGenerator']), "Must use ContactNetworkGenerator_File module"
        assert "EndCriteria_TransmissionFile" in str(MF.modules['EndCriteria']), "Must use EndCriteria_TransmissionFile module"
        assert "TransmissionNodeSample_TransmissionFile" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_TransmissionFile module"
        assert "TransmissionTimeSample_TransmissionFile" in str(MF.modules['TransmissionTimeSample']), "Must use TransmissionTimeSample_TransmissionFile module"
        GC.transmission_file = [i.strip().split() for i in open(expanduser(GC.transmission_network_file)) if len(i.strip()) > 0 and i[0] != '#']
        for i in range(len(GC.transmission_file)):
            GC.transmission_file[i][2] = float(GC.transmission_file[i][2])
        GC.transmission_num = 0

    def select_seeds():
        seeds = []
        while GC.transmission_file[GC.transmission_num][0] == "None":
            seeds.append(GC.contact_network.get_node(GC.transmission_file[GC.transmission_num][1])); GC.transmission_num += 1
        return seeds