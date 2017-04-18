#! /usr/bin/env python3
'''
Niema Moshiri 2016

"EndCriteria" module, where the transmission network is simulated by GEMF
(Sahneh et al. 2016).
'''
from EndCriteria import EndCriteria
import favites_modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class EndCriteria_GEMF(EndCriteria):
    def init():
        assert "GEMF" in str(MF.modules['TransmissionNodeSample']), "Must use a GEMF TransmissionNodeSample module"
        assert "GEMF" in str(MF.modules['TransmissionTimeSample']), "Must use a GEMF TransmissionTimeSample module"

    def done():
        return GC.transmission_num == len(GC.transmission_file)

    def not_done():
        return not EndCriteria_TransmissionFile.done()

    def finalize_time():
        pass