#! /usr/bin/env python3
'''
Niema Moshiri 2016

"EndCriteria" module, where the transmission network is read from a file
'''
from EndCriteria import EndCriteria
from EndCriteria_TransmissionFile import EndCriteria_TransmissionFile
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class EndCriteria_PangeaSim(EndCriteria):
    def cite():
        return GC.CITATION_PANGEA

    def init():
        assert "ContactNetworkGenerator_PangeaSim" in str(MF.modules['ContactNetworkGenerator']), "Must use ContactNetworkGenerator_PangeaSim module"
        assert "SeedSelection_PangeaSim" in str(MF.modules['SeedSelection']), "Must use SeedSelection_PangeaSim module"
        assert "TransmissionNodeSample_PangeaSim" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_PangeaSim module"
        assert "TransmissionTimeSample_PangeaSim" in str(MF.modules['TransmissionTimeSample']), "Must use TransmissionTimeSample_PangeaSim module"

    def done():
        return EndCriteria_TransmissionFile.done()

    def not_done():
        return EndCriteria_TransmissionFile.not_done()

    def finalize_time():
        pass