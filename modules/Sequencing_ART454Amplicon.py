#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Sequencing" module, using ART to simulate Roche 454 reads (amplicon sequencing)
'''
from Sequencing import Sequencing
import FAVITES_GlobalContext as GC
from subprocess import call,STDOUT
from tempfile import NamedTemporaryFile
from os.path import expanduser
from os import getcwd,makedirs,chdir,listdir,rename

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
        if not hasattr(GC,"sequencing_file"):
            if GC.art_454_amplicon_mode == "single":
                GC.sequencing_file = open('%s/error_prone_files/sequence_data_subsampled_errorprone.fastq'%GC.out_dir, 'w')
            else:
                GC.sequencing_file = open('%s/error_prone_files/sequence_data_subsampled_errorprone_read1.fastq'%GC.out_dir, 'w')
                GC.sequencing_file2 = open('%s/error_prone_files/sequence_data_subsampled_errorprone_read2.fastq'%GC.out_dir, 'w')
        orig_dir = getcwd()
        chdir(GC.out_dir)
        makedirs("ART_output", exist_ok=True)
        chdir("ART_output")
        cn_label = node.get_name()
        for t in GC.final_sequences[cn_label]:
            f = NamedTemporaryFile(mode='w')
            for l,s in GC.final_sequences[cn_label][t]:
                f.write(">%s\n%s\n" % (l,s))
            f.flush()
            command = [GC.art_454_path] + GC.art_454_options
            if GC.random_number_seed is not None:
                command += ['-r',str(GC.random_number_seed)]
                GC.random_number_seed += 1
            if GC.art_454_amplicon_mode == "single":
                command.append('-A')
            else:
                command.append('-B')
            command.append(f.name)
            command.append('%s_%f' % (cn_label,t))
            command.append(str(GC.art_454_reads_pairs_per_amplicon))
            try:
                call(command, stdout=open('%s_%f.log' % (cn_label,t), 'w'), stderr=STDOUT)
            except FileNotFoundError:
                chdir(GC.START_DIR)
                assert False, "art_454 executable was not found: %s" % GC.art_454_path
            f.close()
            if GC.art_454_amplicon_mode == "single":
                for l in open('%s_%f.fq' % (cn_label,t)):
                    GC.sequencing_file.write(l)
            else:
                rename('%s_%f.fq' % (cn_label,t), '%s_%f_read1.fq' % (cn_label,t))
                for l in open('%s_%f_read1.fq' % (cn_label,t)):
                    GC.sequencing_file.write(l)
                rename('%s_%f2.fq' % (cn_label,t), '%s_%f_read2.fq' % (cn_label,t))
                for l in open('%s_%f_read2.fq' % (cn_label,t)):
                    GC.sequencing_file2.write(l)
        chdir(orig_dir)

    def finalize():
        if hasattr(GC,"sequencing_file"):
            GC.sequencing_file.close()
        if hasattr(GC,"sequencing_file2"):
            GC.sequencing_file2.close()