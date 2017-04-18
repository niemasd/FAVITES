#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSelection" module, where the transmission network is read from a file

Seed nodes are passed in via the "seed_file" parameter of the configuration file
'''
from SeedSelection import SeedSelection
import favites_modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from os.path import expanduser

class SeedSelection_TransmissionFile(SeedSelection):
    def init():
        assert "EndCriteria_TransmissionFile" in str(MF.modules['EndCriteria']), "Must use EndCriteria_TransmissionFile module"
        assert "TransmissionNodeSample_TransmissionFile" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_TransmissionFile module"
        assert "TransmissionTimeSample_TransmissionFile" in str(MF.modules['TransmissionTimeSample']), "Must use TransmissionTimeSample_TransmissionFile module"
        GC.transmission_file = [i.strip().split() for i in open(expanduser(GC.transmission_network_file)) if len(i.strip()) > 0]
        for i in range(len(GC.transmission_file)):
            GC.transmission_file[i][2] = float(GC.transmission_file[i][2])
        GC.transmission_num = 0
        GC.transmission_state = set() # 'node' and 'time'

    def select_seeds():
        return [GC.contact_network.get_node(i.strip()) for i in open(expanduser(GC.seed_file)) if len(i.strip()) > 0]