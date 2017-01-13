#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Sequencing" module, using DWGSIM to simulate NGS reads
'''
from Sequencing import Sequencing
import FAVITES_GlobalContext as GC
from subprocess import call
from os.path import expanduser
from os import getcwd
from os import makedirs
from os import chdir

class Sequencing_DWGSIM(Sequencing):
    def init():
        GC.out_dir = expanduser(GC.out_dir)
        GC.dwgsim_path = expanduser(GC.dwgsim_path.strip())
        GC.dwgsim_options = [i.strip() for i in GC.dwgsim_options.strip().split()]

    def introduce_sequencing_error(node):
        command = [GC.dwgsim_path] + GC.dwgsim_options
        command.append(GC.out_dir + "/error_free_files/sequence_data/seqs_" + node.get_name() + ".fasta")
        command.append(node.get_name())
        orig_dir = getcwd()
        makedirs("error_prone_files/sequence_data", exist_ok=True)
        chdir("error_prone_files/sequence_data")
        call(command, stderr=open("log_" + node.get_name() + ".txt", 'w'))
        chdir(orig_dir)