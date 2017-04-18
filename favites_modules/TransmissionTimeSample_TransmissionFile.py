#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionTimeSample" module, where the transmission network is read from a
file
'''
from TransmissionTimeSample import TransmissionTimeSample
import favites_modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class TransmissionTimeSample_TransmissionFile(TransmissionTimeSample):
    def init():
        assert "EndCriteria_TransmissionFile" in str(MF.modules['EndCriteria']), "Must use EndCriteria_TransmissionFile module"
        assert "SeedSelection_TransmissionFile" in str(MF.modules['SeedSelection']), "Must use SeedSelection_TransmissionFile module"
        assert "TransmissionNodeSample_TransmissionFile" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_TransmissionFile module"
        # SeedSelection_TransmissionFile sets everything up

    def sample_time():
        if 'time' in GC.transmission_state and 'node' in GC.transmission_state:
            GC.transmission_state = set()
            GC.transmission_num += 1
        elif 'time' in GC.transmission_state:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Performing two TransmissionTimeSample events before TransmissionNodeSample"
        if GC.transmission_num == len(GC.transmission_file):
            return None
        GC.transmission_state.add('time')
        return GC.transmission_file[GC.transmission_num][2]