#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Sequencing" module, using DWGSIM to simulate NGS reads
'''
from Sequencing import Sequencing # abstract Sequencing class
import FAVITES_GlobalContext as GC
from subprocess import call
import os

class Sequencing_DWGSIM(Sequencing):
    def init():
        GC.out_dir = os.path.expanduser(GC.out_dir)
        GC.dwgsim_path = GC.dwgsim_path.strip()
        GC.dwgsim_options = [i.strip() for i in GC.dwgsim_options.strip().split()]

    def introduce_sequencing_error(node):
        # run DWGSIM, it will create a FASTQ I think,
        # then read the FASTQ as a single string and return it
        # this is called on each ContactNetwork node individuallyt
        command = [GC.dwgsim_path] + GC.dwgsim_options
        command.append(GC.out_dir + "/error_free_files/sequence_data/seqs_" + node.get_name() + ".fasta")
        command.append(node.get_name())
        orig_dir = os.getcwd()
        os.makedirs("error_prone_files/sequence_data", exist_ok=True)
        os.chdir("error_prone_files/sequence_data")
        call(command, stderr=open("log_" + node.get_name() + ".txt", 'w'))
        os.chdir(orig_dir)