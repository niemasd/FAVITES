#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Sequencing" module, using ART to simulate Roche 454 reads (paired-end)
'''
from Sequencing import Sequencing
import FAVITES_GlobalContext as GC
from subprocess import call
from os.path import expanduser
from os import getcwd,makedirs,chdir,listdir

class Sequencing_ART454PairedEnd(Sequencing):
    def cite():
        return GC.CITATION_ART

    def init():
        GC.out_dir = expanduser(GC.out_dir)
        GC.art_454_options = [i.strip() for i in GC.art_454_options.strip().split()]
        GC.art_454_path = expanduser(GC.art_454_path.strip())

    def introduce_sequencing_error(node):
        orig_dir = getcwd()
        chdir(GC.out_dir)
        makedirs("error_prone_files/sequence_data", exist_ok=True)
        chdir("error_prone_files/sequence_data")
        for filename in listdir("%s/error_free_files/sequence_data" % GC.out_dir):
            if filename.split('_')[1][1:] == node.get_name():
                command = [GC.art_454_path] + GC.art_454_options
                command.append("%s/error_free_files/sequence_data/%s" % (GC.out_dir,filename))
                command.append(filename[:-6])
                command.append(str(GC.art_454_fold_coverage))
                command.append(str(GC.art_454_mean_frag_len))
                command.append(str(GC.art_454_std_dev))
                try:
                    call(command, stdout=open("log_%s.txt" % filename[5:-6], 'w'))
                except FileNotFoundError:
                    chdir(GC.START_DIR)
                    assert False, "art_454 executable was not found: %s" % GC.art_454_path
        chdir(orig_dir)