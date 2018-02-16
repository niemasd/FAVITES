#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Sequencing" module, perfect sequencing
'''
from Sequencing import Sequencing # abstract Sequencing class
import FAVITES_GlobalContext as GC
from os import getcwd,makedirs,chdir,listdir

class Sequencing_Perfect(Sequencing):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        pass

    def introduce_sequencing_error(node):
        if not hasattr(GC,"sequencing_file"):
            GC.sequencing_file = open('%s/error_prone_files/sequence_data_subsampled_errorprone.fastq'%GC.out_dir, 'w')
        cn_label = node.get_name()
        for t in GC.final_sequences[cn_label]:
            for l,s in GC.final_sequences[cn_label][t]:
                GC.sequencing_file.write("@%s\n%s\n+\n%s\n" % (l,s,'~'*len(s)))

    def finalize():
        GC.sequencing_file.close()