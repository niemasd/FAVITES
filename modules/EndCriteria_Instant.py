#! /usr/bin/env python3
'''
Niema Moshiri 2016

"EndCriteria" module, where simulations end immediately (i.e., no transmissions)

This is intended to be used if you only want to simulate a contact network and
nothing else
'''
from EndCriteria import EndCriteria
import modules.FAVITES_ModuleFactory as MF

class EndCriteria_Instant(EndCriteria):
    def init():
        assert "NodeEvolution_None" in str(MF.modules['NodeEvolution']), "Must use NodeEvolution_None module"
        assert "NodeSample_Perfect" in str(MF.modules['NodeSample']), "Must use NodeSample_Perfect module"
        assert "SequenceEvolution_NoMutation" in str(MF.modules['SequenceEvolution']), "Must use SequenceEvolution_NoMutation module"
        assert "Sequencing_Perfect" in str(MF.modules['Sequencing']), "Must use Sequencing_Perfect module"
        assert "TransmissionTimeSample_Instant" in str(MF.modules['TransmissionTimeSample']), "Must use TransmissionTimeSample_Instant module"

    def done():
        return True

    def not_done():
        return False

    def finalize_time():
        pass