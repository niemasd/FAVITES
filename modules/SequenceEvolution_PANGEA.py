#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SequenceEvolution" module, implemented such that no mutations are allowed
(i.e., all sequences are identical to the initial infection sequence).
'''
from SequenceEvolution import SequenceEvolution # abstract SequenceEvolution class
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class SequenceEvolution_PANGEA(SequenceEvolution):
    def cite():
        return GC.CITATION_PANGEA

    def init():
        GC.pangea_module_check()

    def finalize():
        pass

    def evolve_to_current_time(node):
        pass