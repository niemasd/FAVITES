#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Sequencing" module, using Grinder to simulate Sanger sequencing
'''
from Sequencing import Sequencing
import FAVITES_GlobalContext as GC
from subprocess import call
from os.path import expanduser
from os import getcwd
from os import makedirs
from os import chdir

class Sequencing_GrinderSanger(Sequencing):
    def init():
        GC.out_dir = expanduser(GC.out_dir)
        GC.grinder_path = expanduser(GC.grinder_path.strip())

    def introduce_sequencing_error(node):
        command = [GC.grinder_path,"-reference_file"]
        command.append(GC.out_dir + "/error_free_files/sequence_data/seqs_" + node.get_name() + ".fasta")
        command += ["-read_dist","999999999999"] # set average length absurdly long (it truncates at full length of sequence)
        command += ["-mutation_dist","linear",'1','2',"-mutation_ratio",'80','20'] # Sanger parameters (see Grinder README)
        command += ["-fastq_output",'1',"-qual_levels",'30','10'] # for FASTQ output
        command += ["-base_name",node.get_name()]
        orig_dir = getcwd()
        makedirs("error_prone_files/sequence_data", exist_ok=True)
        chdir("error_prone_files/sequence_data")
        try:
            call(command, stdout=open("log_" + node.get_name() + ".txt", 'w'))
        except FileNotFoundError:
            chdir(GC.START_DIR)
            assert False, "grinder executable was not found: %s" % GC.grinder_path
        chdir(orig_dir)