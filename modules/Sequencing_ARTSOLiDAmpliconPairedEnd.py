#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Sequencing" module, using ART to simulate SOLiD reads (amplicon paired-end, F3-F5)
'''
from Sequencing import Sequencing
import FAVITES_GlobalContext as GC
from subprocess import call
from os.path import expanduser
from os import getcwd,makedirs,chdir,listdir

class Sequencing_ARTSOLiDAmpliconPairedEnd(Sequencing):
    def cite():
        return GC.CITATION_ART

    def init():
        GC.out_dir = expanduser(GC.out_dir)
        GC.art_SOLiD_options = [i.strip() for i in GC.art_SOLiD_options.strip().split()]
        GC.art_SOLiD_path = expanduser(GC.art_SOLiD_path.strip())
        assert GC.art_SOLiD_len_read_F3 <= 75, "Maximum ART SOLiD read length is 75"
        assert GC.art_SOLiD_len_read_F5 <= 75, "Maximum ART SOLiD read length is 75"

    def introduce_sequencing_error(node):
        orig_dir = getcwd()
        chdir(GC.out_dir)
        makedirs("error_prone_files/sequence_data", exist_ok=True)
        chdir("error_prone_files/sequence_data")
        for filename in listdir(GC.out_dir + "/error_free_files/sequence_data"):
            if filename.split('_')[1][1:] == node.get_name():
                command = [GC.art_SOLiD_path] + GC.art_SOLiD_options + ['-A','p']
                command.append(GC.out_dir + "/error_free_files/sequence_data/" + filename)
                command.append(filename[:-6])
                command.append(str(GC.art_SOLiD_len_read_F3))
                command.append(str(GC.art_SOLiD_len_read_F5))
                command.append(str(GC.art_SOLiD_read_pairs_per_amplicon))
                try:
                    call(command, stdout=open("log_" + filename[5:-6] + ".txt", 'w'))
                except FileNotFoundError:
                    chdir(GC.START_DIR)
                    assert False, "art_SOLiD executable was not found: %s" % GC.art_SOLiD_path
        chdir(orig_dir)