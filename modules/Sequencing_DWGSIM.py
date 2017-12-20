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
    def cite():
        return GC.CITATION_DWGSIM

    def init():
        GC.out_dir = expanduser(GC.out_dir)
        GC.dwgsim_path = expanduser(GC.dwgsim_path.strip())
        GC.dwgsim_options = [i.strip() for i in GC.dwgsim_options.strip().split()]

    def introduce_sequencing_error(node):
        orig_dir = getcwd()
        chdir(GC.out_dir)
        makedirs("error_prone_files/sequence_data", exist_ok=True)
        chdir("error_prone_files/sequence_data")
        for filename in listdir("%s/error_free_files/sequence_data" % GC.out_dir):
            if filename.split('_')[1][1:] == node.get_name():
                command = [GC.dwgsim_path] + GC.dwgsim_options
                command.append("%s/error_free_files/sequence_data/%s" % (GC.out_dir,filename))
                command.append(filename[:-6])
                try:
                    call(command, stderr=open("log_%s.txt" % filename[5:-6], 'w'))
                except FileNotFoundError:
                    chdir(GC.START_DIR)
                    assert False, "dwgsim executable was not found: %s" % GC.dwgsim_path
        chdir(orig_dir)