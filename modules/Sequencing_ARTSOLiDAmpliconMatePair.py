#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Sequencing" module, using ART to simulate SOLiD reads (amplicon mate-pair, F3-R3)
'''
from Sequencing import Sequencing
import FAVITES_GlobalContext as GC
from subprocess import call
from os.path import expanduser
from os import getcwd
from os import makedirs
from os import chdir

class Sequencing_ARTSOLiDAmpliconMatePair(Sequencing):
    def init():
        GC.out_dir = expanduser(GC.out_dir)
        GC.art_SOLiD_options = [i.strip() for i in GC.art_SOLiD_options.strip().split()]
        GC.art_SOLiD_path = expanduser(GC.art_SOLiD_path.strip())
        assert GC.art_SOLiD_len_read <= 75, "Maximum ART SOLiD read length is 75"

    def introduce_sequencing_error(node):
        command = [GC.art_SOLiD_path] + GC.art_SOLiD_options + ['-A','m']
        command.append(GC.out_dir + "/error_free_files/sequence_data/seqs_" + node.get_name() + ".fasta")
        command.append(node.get_name())
        command.append(str(GC.art_SOLiD_len_read))
        command.append(str(GC.art_SOLiD_read_pairs_per_amplicon))
        orig_dir = getcwd()
        chdir(GC.out_dir)
        makedirs("error_prone_files/sequence_data", exist_ok=True)
        chdir("error_prone_files/sequence_data")
        call(command, stdout=open("log_" + node.get_name() + ".txt", 'w'))
        chdir(orig_dir)