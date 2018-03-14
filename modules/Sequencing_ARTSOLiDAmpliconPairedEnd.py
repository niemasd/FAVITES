#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Sequencing" module, using ART to simulate SOLiD reads (amplicon paired-end, F3-F5)
'''
from Sequencing import Sequencing
import FAVITES_GlobalContext as GC
from gzip import open as gopen
from subprocess import call
from tempfile import NamedTemporaryFile
from os.path import expanduser
from os import getcwd,makedirs,chdir,listdir

class Sequencing_ARTSOLiDAmpliconPairedEnd(Sequencing):
    def cite():
        return GC.CITATION_ART

    def init():
        GC.out_dir = expanduser(GC.out_dir)
        GC.art_SOLiD_options = [i.strip() for i in GC.art_SOLiD_options.strip().split()]
        GC.art_SOLiD_path = expanduser(GC.art_SOLiD_path.strip())
        assert GC.art_SOLiD_len_read_F3 <= 75, "Maximum ART SOLiD read length is 75"
        assert GC.art_SOLiD_len_read_F5 <= 75, "Maximum ART SOLiD read length is 75"

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
            command = [GC.art_SOLiD_path] + GC.art_SOLiD_options
            if GC.random_number_seed is not None:
                command += ['-r',str(GC.random_number_seed)]
                GC.random_number_seed += 1
            command += ['-A','p']
            command.append(f.name)
            command.append('%s_%f' % (cn_label,t))
            command.append(str(GC.art_SOLiD_len_read_F3))
            command.append(str(GC.art_SOLiD_len_read_F5))
            command.append(str(GC.art_SOLiD_read_pairs_per_amplicon))
            try:
                call(command, stdout=open('%s_%f.log' % (cn_label,t), 'w'))
            except FileNotFoundError:
                chdir(GC.START_DIR)
                assert False, "art_SOLiD executable was not found: %s" % GC.art_illumina_path
            f.close()
            if not hasattr(GC,"sequencing_file_F3"):
                GC.sequencing_file_F3 = gopen('%s/error_prone_files/sequence_data_subsampled_errorprone_F3.fastq.gz'%GC.out_dir, 'w')
            for l in open('%s_%f_F3.fq' % (cn_label,t)):
                GC.sequencing_file_F3.write(l.encode())
            if not hasattr(GC,"sequencing_file_F5"):
                GC.sequencing_file_F5 = gopen('%s/error_prone_files/sequence_data_subsampled_errorprone_F5.fastq.gz'%GC.out_dir, 'w')
            for l in open('%s_%f_F5.fq' % (cn_label,t)):
                GC.sequencing_file_F5.write(l.encode())
        chdir(orig_dir)

    def finalize():
        if hasattr(GC,"sequencing_file_F3"):
            GC.sequencing_file_F3.close()
        if hasattr(GC,"sequencing_file_F5"):
            GC.sequencing_file_F5.close()