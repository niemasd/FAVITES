#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Sequencing" module, using ART to simulate Roche 454 reads (amplicon sequencing)
'''
from Sequencing import Sequencing
import FAVITES_GlobalContext as GC
from subprocess import call
from os.path import expanduser
from os import getcwd,makedirs,chdir,listdir

class Sequencing_ART454Amplicon(Sequencing):
    def cite():
        return GC.CITATION_ART

    def init():
        GC.out_dir = expanduser(GC.out_dir)
        GC.art_454_options = [i.strip() for i in GC.art_454_options.strip().split()]
        GC.art_454_path = expanduser(GC.art_454_path.strip())
        GC.art_454_amplicon_mode = GC.art_454_amplicon_mode.strip()
        assert GC.art_454_amplicon_mode == "single" or GC.art_454_amplicon_mode == "paired", '"art_454_amplicon_mode" must be either "single" or "paired"'

    def introduce_sequencing_error(node):
        orig_dir = getcwd()
        chdir(GC.out_dir)
        makedirs("error_prone_files/sequence_data", exist_ok=True)
        chdir("error_prone_files/sequence_data")
        for filename in listdir("%s/error_free_files/sequence_data" % GC.out_dir):
            if filename.split('_')[1][1:] == node.get_name():
                command = [GC.art_454_path] + GC.art_454_options
                if GC.art_454_amplicon_mode == "single":
                    command.append('-A')
                else:
                    command.append('-B')
                command.append("%s/error_free_files/sequence_data/%s" % (GC.out_dir,filename))
                command.append(filename[:-6])
                command.append(str(GC.art_454_reads_pairs_per_amplicon))
                try:
                    call(command, stdout=open("log_%s.txt" % filename[5:-6], 'w'))
                except FileNotFoundError:
                    chdir(GC.START_DIR)
                    assert False, "art_454 executable was not found: %s" % GC.art_454_path
        chdir(orig_dir)