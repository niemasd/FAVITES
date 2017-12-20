#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Sequencing" module, using ART to simulate SOLiD reads (paired-end, F3-F5)
'''
from Sequencing import Sequencing
import FAVITES_GlobalContext as GC
from subprocess import call
from os.path import expanduser
from os import getcwd
from os import makedirs
from os import chdir

class Sequencing_ARTSOLiDPairedEnd(Sequencing):
    def cite():
        return GC.CITATION_ART

    def init():
        GC.out_dir = expanduser(GC.out_dir)
        GC.art_SOLiD_options = [i.strip() for i in GC.art_SOLiD_options.strip().split()]
        GC.art_SOLiD_path = expanduser(GC.art_SOLiD_path.strip())
        assert GC.art_SOLiD_len_read_F3 <= 75, "Maximum ART SOLiD read length is 75"
        assert GC.art_SOLiD_len_read_F5 <= 75, "Maximum ART SOLiD read length is 75"

    def introduce_sequencing_error(node):
        command = [GC.art_SOLiD_path] + GC.art_SOLiD_options
        command.append("%s/error_free_files/sequence_data/seqs_%s.fasta" % (GC.out_dir,node.get_name()))
        command.append(node.get_name())
        command.append(str(GC.art_SOLiD_len_read_F3))
        command.append(str(GC.art_SOLiD_len_read_F5))
        command.append(str(GC.art_SOLiD_fold_coverage))
        command.append(str(GC.art_SOLiD_mean_frag_len))
        command.append(str(GC.art_SOLiD_std_dev))
        orig_dir = getcwd()
        chdir(GC.out_dir)
        makedirs("error_prone_files/sequence_data", exist_ok=True)
        chdir("error_prone_files/sequence_data")
        try:
            call(command, stdout=open("log_%s.txt" % node.get_name(), 'w'))
        except FileNotFoundError:
            chdir(GC.START_DIR)
            assert False, "art_SOLiD executable was not found: %s" % GC.art_SOLiD_path
        chdir(orig_dir)