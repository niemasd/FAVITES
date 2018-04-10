#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSequence" module, implemented such that no sequences are generated.
'''
from SeedSequence import SeedSequence
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class SeedSequence_NoSeqs(SeedSequence):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        if "SequenceEvolution_File" not in str(MF.modules['SequenceEvolution']):
            assert "SequenceEvolution_NoSeqs" in str(MF.modules['SequenceEvolution']), "Must use SequenceEvolution_NoSeqs module"
            assert "Sequencing_NoSeqs" in str(MF.modules['Sequencing']), "Must use Sequencing_NoSeqs module"

    def generate():
        return ""

    def merge_trees():
        return [],[]