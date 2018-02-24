#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Sequencing" module, using Grinder to simulate Sanger sequencing
'''
from Sequencing import Sequencing
import FAVITES_GlobalContext as GC
from subprocess import call
from tempfile import NamedTemporaryFile
from os.path import expanduser
from os import getcwd,makedirs,chdir,listdir

class Sequencing_GrinderSanger(Sequencing):
    def cite():
        return GC.CITATION_GRINDER

    def init():
        GC.out_dir = expanduser(GC.out_dir)
        GC.grinder_path = expanduser(GC.grinder_path.strip())

    def introduce_sequencing_error(node):
        if not hasattr(GC,"sequencing_file"):
            GC.sequencing_file = open('%s/error_prone_files/sequence_data_subsampled_errorprone.fastq'%GC.out_dir, 'w')
        orig_dir = getcwd()
        chdir(GC.out_dir)
        makedirs("Grinder_output", exist_ok=True)
        chdir("Grinder_output")
        cn_label = node.get_name()
        for t in GC.final_sequences[cn_label]:
            f = NamedTemporaryFile(mode='w')
            for l,s in GC.final_sequences[cn_label][t]:
                f.write(">%s\n%s\n" % (l,s))
            f.flush()
            command = [GC.grinder_path,"-reference_file"]
            command.append(f.name)
            command += ["-total_reads","1"] # only get 1 read
            command += ["-read_dist","999999999999"] # set average length absurdly long (it truncates at full length of sequence)
            command += ["-mutation_dist","linear",'1','2',"-mutation_ratio",'80','20'] # Sanger parameters (see Grinder README)
            command += ["-unidirectional",'1'] # only generate reads from forward strand
            command += ["-fastq_output",'1',"-qual_levels",'30','10'] # for FASTQ output
            command += ["-base_name",'%s_%f' % (cn_label,t)]
            try:
                call(command, stdout=open('%s_%f.log' % (cn_label,t), 'w'))
            except FileNotFoundError:
                chdir(GC.START_DIR)
                assert False, "grinder executable was not found: %s" % GC.dwgsim_path
            f.close()
            for l in open('%s_%f-reads.fastq' % (cn_label,t)):
                GC.sequencing_file.write(l)
        chdir(orig_dir)

    def finalize():
        if hasattr(GC,"sequencing_file"):
            GC.sequencing_file.close()