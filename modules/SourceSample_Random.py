#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SourceSample" module, implemented to randomly select a virus at present time
'''
from SourceSample import SourceSample
import FAVITES_GlobalContext as GC
from random import choice

class SourceSample_Random(SourceSample):
    def init():
        pass

    def sample_virus(node):
        viruses = []
        for virus in node.viruses():
            assert virus.time == GC.time, "Encountered leaf node not at current time!"
            viruses.append(virus)
        if len(viruses) == 1:
            viruses = viruses[0].split()
        return choice(viruses)