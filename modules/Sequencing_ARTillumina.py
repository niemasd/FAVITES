#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Sequencing" module, using ART to simulate Illumina NGS reads
'''
from Sequencing import Sequencing
import FAVITES_GlobalContext as GC
from subprocess import call
from tempfile import NamedTemporaryFile
from os.path import expanduser,isfile
from os import getcwd,makedirs,chdir,listdir,rename

class Sequencing_ARTillumina(Sequencing):
    def cite():
        return GC.CITATION_ART

    def init():
        GC.out_dir = expanduser(GC.out_dir)
        GC.art_illumina_options = [i.strip() for i in GC.art_illumina_options.strip().split()]
        assert "-i" not in GC.art_illumina_options and "--in" not in GC.art_illumina_options, "Don't use the -i (--in) argument (we will specify it for you)"
        assert "-o" not in GC.art_illumina_options and "--out" not in GC.art_illumina_options, "Don't use the -o (--out) argument (we will specify it for you)"
        GC.art_illumina_path = expanduser(GC.art_illumina_path.strip())

    def introduce_sequencing_error(node):
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
            command = [GC.art_illumina_path] + GC.art_illumina_options
            command.append("-i")
            command.append(f.name)
            command.append("-o")
            command.append('%s_%f' % (cn_label,t))
            try:
                call(command, stdout=open('%s_%f.log' % (cn_label,t), 'w'))
            except FileNotFoundError:
                chdir(GC.START_DIR)
                assert False, "art_illumina executable was not found: %s" % GC.art_illumina_path
            f.close()
            if isfile('%s_%f.fq' % (cn_label,t)):
                if not hasattr(GC,"sequencing_file"):
                    GC.sequencing_file = open('%s/error_prone_files/sequence_data_subsampled_errorprone.fastq'%GC.out_dir, 'w')
                for l in open('%s_%f.fq' % (cn_label,t)):
                    GC.sequencing_file.write(l)
            elif isfile('%s_%f1.fq' % (cn_label,t)):
                if not hasattr(GC,"sequencing_file"):
                    GC.sequencing_file = open('%s/error_prone_files/sequence_data_subsampled_errorprone_read1.fastq'%GC.out_dir, 'w')
                    GC.sequencing_file2 = open('%s/error_prone_files/sequence_data_subsampled_errorprone_read2.fastq'%GC.out_dir, 'w')
                rename('%s_%f1.fq' % (cn_label,t), '%s_%f_read1.fq' % (cn_label,t))
                for l in open('%s_%f_read1.fq' % (cn_label,t)):
                    GC.sequencing_file.write(l)
                rename('%s_%f2.fq' % (cn_label,t), '%s_%f_read2.fq' % (cn_label,t))
                for l in open('%s_%f_read2.fq' % (cn_label,t)):
                    GC.sequencing_file2.write(l)
            else:
                assert False, "Error occurred with art_illumina"
        chdir(orig_dir)

    def finalize():
        if hasattr(GC,"sequencing_file"):
            GC.sequencing_file.close()
        if hasattr(GC,"sequencing_file2"):
            GC.sequencing_file2.close()