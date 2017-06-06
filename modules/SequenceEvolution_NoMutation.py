#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SequenceEvolution" module, implemented such that no mutations are allowed
(i.e., all sequences are identical to the initial infection sequence).
'''
from SequenceEvolution import SequenceEvolution # abstract SequenceEvolution class
import FAVITES_GlobalContext as GC

class SequenceEvolution_NoMutation(SequenceEvolution):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        pass

    def finalize():
        pass

    def evolve_to_current_time(node):
        for time,virus in node.get_infections():
            for leaf in virus.leaves():
                leaf.set_seq(leaf.get_root().get_seq())