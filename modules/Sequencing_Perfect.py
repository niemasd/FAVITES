#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Sequencing" module, perfect sequencing
'''
from Sequencing import Sequencing # abstract Sequencing class
import FAVITES_GlobalContext as GC

class Sequencing_Perfect(Sequencing):
    def introduce_sequencing_error(node):
        l = [leaf for leaf in node.viruses()]
        seq_data = [leaf.get_seq() for leaf in l]
        labels = [leaf.get_label() for leaf in l]
        return '\n'.join(["@%s\n%s\n+\n%s" % (labels[i], seq_data[i], '~'*len(seq_data[i])) for i in range(len(l))])