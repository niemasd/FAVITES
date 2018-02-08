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
        orig_dir = getcwd()
        makedirs("error_prone_files/sequence_data", exist_ok=True)
        chdir("error_prone_files/sequence_data")
        for filename in listdir("%s/error_free_files/sequence_data" % GC.out_dir):
            if filename.split('_')[1][1:] == node.get_name():
                seqs = GC.parseFASTA(open("%s/error_free_files/sequence_data/%s" % (GC.out_dir,filename)))
                f = open(filename.replace('.fasta','.fastq'), 'w')
                for k in seqs:
                    f.write("@%s\n%s\n+\n%s\n" % (k, seqs[k], '~'*len(seqs[k])))
                f.close()
        chdir(orig_dir)