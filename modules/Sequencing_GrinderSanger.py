#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Sequencing" module, using Grinder to simulate Sanger sequencing
'''
from Sequencing import Sequencing
import FAVITES_GlobalContext as GC
from subprocess import call
from os.path import expanduser
from os import getcwd,makedirs,chdir,listdir

class Sequencing_GrinderSanger(Sequencing):
    def init():
        GC.out_dir = expanduser(GC.out_dir)
        GC.grinder_path = expanduser(GC.grinder_path.strip())

    def introduce_sequencing_error(node):
        orig_dir = getcwd()
        chdir(GC.out_dir)
        makedirs("error_prone_files/sequence_data", exist_ok=True)
        chdir("error_prone_files/sequence_data")
        for filename in listdir(GC.out_dir + "/error_free_files/sequence_data"):
            if filename.split('_')[1][1:] == node.get_name():
                command = [GC.grinder_path,"-reference_file"]
                command.append(GC.out_dir + "/error_free_files/sequence_data/" + filename)
                command += ["-read_dist","999999999999"] # set average length absurdly long (it truncates at full length of sequence)
                command += ["-mutation_dist","linear",'1','2',"-mutation_ratio",'80','20'] # Sanger parameters (see Grinder README)
                command += ["-fastq_output",'1',"-qual_levels",'30','10'] # for FASTQ output
                command += ["-base_name",filename[:-6]]
                try:
                    call(command, stdout=open("log_" + filename[5:-6] + ".txt", 'w'))
                except FileNotFoundError:
                    chdir(GC.START_DIR)
                    assert False, "grinder executable was not found: %s" % GC.grinder_path
        chdir(orig_dir)