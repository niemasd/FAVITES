#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SequenceEvolution" module, implemented such that no sequences are generated.
'''
from SequenceEvolution import SequenceEvolution # abstract SequenceEvolution class
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class SequenceEvolution_NoSeqs(SequenceEvolution):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        assert "SeedSequence_NoSeqs" in str(MF.modules['SeedSequence']), "Must use SeedSequence_NoSeqs module"
        assert "Sequencing_NoSeqs" in str(MF.modules['Sequencing']), "Must use Sequencing_NoSeqs module"

    def finalize():
        GC.final_sequences = {}

    def evolve_to_current_time(node):
        pass
