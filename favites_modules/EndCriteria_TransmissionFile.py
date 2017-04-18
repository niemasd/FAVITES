#! /usr/bin/env python3
'''
Niema Moshiri 2016

"EndCriteria" module, where the transmission network is read from a file
'''
from EndCriteria import EndCriteria
import favites_modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class EndCriteria_TransmissionFile(EndCriteria):
    def init():
        assert "SeedSelection_TransmissionFile" in str(MF.modules['SeedSelection']), "Must use SeedSelection_TransmissionFile module"
        assert "TransmissionNodeSample_TransmissionFile" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_TransmissionFile module"
        assert "TransmissionTimeSample_TransmissionFile" in str(MF.modules['TransmissionTimeSample']), "Must use TransmissionTimeSample_TransmissionFile module"
        # SeedSelection_TransmissionFile sets everything up

    def done():
        return GC.transmission_num == len(GC.transmission_file)

    def not_done():
        return not EndCriteria_TransmissionFile.done()

    def finalize_time():
        pass