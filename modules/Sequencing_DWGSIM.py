#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Sequencing" module, using DWGSIM to simulate NGS reads
'''
from Sequencing import Sequencing
import FAVITES_GlobalContext as GC
from gzip import open as gopen
from subprocess import call,DEVNULL
from tempfile import NamedTemporaryFile
from os.path import expanduser,isfile
from os import getcwd,makedirs,chdir,listdir

class Sequencing_DWGSIM(Sequencing):
    def cite():
        return GC.CITATION_DWGSIM

    def init():
        GC.out_dir = expanduser(GC.out_dir)
        GC.dwgsim_path = expanduser(GC.dwgsim_path.strip())
        GC.dwgsim_options = [i.strip() for i in GC.dwgsim_options.strip().split()]

    def introduce_sequencing_error(node):
        if not hasattr(GC,"sequencing_file"):
            GC.sequencing_file = gopen('%s/error_prone_files/sequence_data_subsampled_errorprone_read1.fastq.gz'%GC.out_dir, 'wb', 9)
            GC.sequencing_file2 = gopen('%s/error_prone_files/sequence_data_subsampled_errorprone_read2.fastq.gz'%GC.out_dir, 'wb', 9)
        orig_dir = getcwd()
        chdir(GC.out_dir)
        makedirs("DWGSIM_output", exist_ok=True)
        chdir("DWGSIM_output")
        cn_label = node.get_name()
        for t in GC.final_sequences[cn_label]:
            f = NamedTemporaryFile(mode='w')
            for l,s in GC.final_sequences[cn_label][t]:
                f.write(">%s\n%s\n" % (l,s))
            f.flush()
            command = [GC.dwgsim_path] + GC.dwgsim_options
            if GC.random_number_seed is not None:
                command += ['-z',str(GC.random_number_seed)]
                GC.random_number_seed += 1
            command.append(f.name)
            command.append('%s_%f' % (cn_label,t))
            try:
                call(command, stderr=open('%s_%f.log' % (cn_label,t), 'w'))
            except FileNotFoundError:
                chdir(GC.START_DIR)
                assert False, "dwgsim executable was not found: %s" % GC.dwgsim_path
            f.close()
            if isfile('%s_%f.bwa.read1.fastq' % (cn_label,t)):
                f = open('%s_%f.bwa.read1.fastq' % (cn_label,t))
            elif isfile('%s_%f.bwa.read1.fastq.gz' % (cn_label,t)):
                f = gopen('%s_%f.bwa.read1.fastq.gz' % (cn_label,t))
            else:
                raise FileNotFoundError("Couldn't find %s_%f.bwa.read1.fastq or %s_%f.bwa.read1.fastq.gz" % (cn_label,t,cn_label,t))
            for l in f:
                if isinstance(l,bytes):
                    GC.sequencing_file.write(l.decode())
                else:
                    GC.sequencing_file.write(l)
            if isfile('%s_%f.bwa.read2.fastq' % (cn_label,t)):
                f = open('%s_%f.bwa.read2.fastq' % (cn_label,t))
            elif isfile('%s_%f.bwa.read2.fastq.gz' % (cn_label,t)):
                f = gopen('%s_%f.bwa.read2.fastq.gz' % (cn_label,t))
            else:
                raise FileNotFoundError("Couldn't find %s_%f.bwa.read2.fastq or %s_%f.bwa.read2.fastq.gz" % (cn_label,t,cn_label,t))
            for l in f:
                if isinstance(l,bytes):
                    GC.sequencing_file2.write(l)
                else:
                    GC.sequencing_file2.write(l.encode())
        chdir(orig_dir)

    def finalize():
        if hasattr(GC,"sequencing_file"):
            GC.sequencing_file.close()
            GC.sequencing_file2.close()
