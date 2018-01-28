#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Sequencing" module, perfect sequencing
'''
from Sequencing import Sequencing # abstract Sequencing class
import FAVITES_GlobalContext as GC
import os

class Sequencing_Perfect(Sequencing):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        pass

    def introduce_sequencing_error(node):
        orig_dir = os.getcwd()
        os.makedirs("error_prone_files/sequence_data", exist_ok=True)
        os.chdir("error_prone_files/sequence_data")
        l = [leaf for leaf in node.viruses()]
        seq_data = [leaf.get_seq() for leaf in l]
        labels = [leaf.get_label() for leaf in l]
        f = open("seqs_%s.fastq" % node.get_name(), 'w')
        for i in range(len(l)):
            f.write("@%s\n%s\n+\n%s\n" % (labels[i], seq_data[i], '~'*len(seq_data[i])))
        f.close()
        os.chdir(orig_dir)