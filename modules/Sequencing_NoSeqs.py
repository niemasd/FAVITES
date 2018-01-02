#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Sequencing" module, implemented such that no sequences are generated.
'''
from Sequencing import Sequencing # abstract Sequencing class
import FAVITES_GlobalContext as GC

class Sequencing_NoSeqs(Sequencing):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        pass

    def introduce_sequencing_error(node):
        pass