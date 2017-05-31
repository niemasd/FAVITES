#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Sequencing" module, using DWGSIM to simulate NGS reads
'''
from Sequencing import Sequencing
import FAVITES_GlobalContext as GC
from subprocess import call
from os.path import expanduser
from os import getcwd,makedirs,chdir,listdir

class Sequencing_DWGSIM(Sequencing):
    def init():
        GC.out_dir = expanduser(GC.out_dir)
        GC.dwgsim_path = expanduser(GC.dwgsim_path.strip())
        GC.dwgsim_options = [i.strip() for i in GC.dwgsim_options.strip().split()]

    def introduce_sequencing_error(node):
        orig_dir = getcwd()
        chdir(GC.out_dir)
        makedirs("error_prone_files/sequence_data", exist_ok=True)
        chdir("error_prone_files/sequence_data")
        for filename in listdir(GC.out_dir + "/error_free_files/sequence_data"):
            if filename.split('_')[1][1:] == node.get_name():
                command = [GC.dwgsim_path] + GC.dwgsim_options
                command.append(GC.out_dir + "/error_free_files/sequence_data/" + filename)
                command.append(filename[:-6])
                try:
                    call(command, stderr=open("log_" + filename[5:-6] + ".txt", 'w'))
                except FileNotFoundError:
                    chdir(GC.START_DIR)
                    assert False, "dwgsim executable was not found: %s" % GC.dwgsim_path
        chdir(orig_dir)