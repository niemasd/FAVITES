#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Sequencing" module, using ART to simulate Roche 454 reads (amplicon sequencing)
'''
from Sequencing import Sequencing
import FAVITES_GlobalContext as GC
from subprocess import call
from os.path import expanduser
from os import getcwd
from os import makedirs
from os import chdir

class Sequencing_ART454Amplicon(Sequencing):
    def init():
        GC.out_dir = expanduser(GC.out_dir)
        GC.art_454_args = [i.strip() for i in GC.art_454_args.strip().split()]
        GC.art_454_path = expanduser(GC.art_454_path.strip())
        GC.art_454_amplicon_mode = GC.art_454_amplicon_mode.strip()
        assert GC.art_454_amplicon_mode == "single" or GC.art_454_amplicon_mode == "paired", '"art_454_amplicon_mode" must be either "single" or "paired"'

    def introduce_sequencing_error(node):
        command = [GC.art_454_path] + GC.art_454_args
        if GC.art_454_amplicon_mode == "single":
            command.append('-A')
        else:
            command.append('-B')
        command.append(GC.out_dir + "/error_free_files/sequence_data/seqs_" + node.get_name() + ".fasta")
        command.append(node.get_name())
        command.append(str(GC.art_454_reads_pairs_per_amplicon))
        orig_dir = getcwd()
        chdir(GC.out_dir)
        makedirs("error_prone_files/sequence_data", exist_ok=True)
        chdir("error_prone_files/sequence_data")
        call(command, stdout=open("log_" + node.get_name() + ".txt", 'w'))
        chdir(orig_dir)