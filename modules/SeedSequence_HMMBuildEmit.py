#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSequence" module, where the user specifies a multiple sequence alignment,
and hmmbuild is used to create a profile HMM from the MSA. Then, hmmemit is
used to sample seed sequences from the resulting profile HMM.
'''
from SeedSequence import SeedSequence
from SeedSequence_HMMEmit import SeedSequence_HMMEmit
import FAVITES_GlobalContext as GC
from subprocess import check_output
from random import choice
from os.path import expanduser
from os import makedirs

HMMBuildEmit_path = "HMMBuildEmit_files"
HMM_filename = "seedseq.hmm"

class SeedSequence_HMMBuildEmit(SeedSequence):
    '''
    Implement the ``SeedSequence'' using hmmbuild to build a profile HMM from
    an input MSA, and then use hmmemit to generate seed sequences from the
    resulting profile HMM
    '''

    def cite():
        return GC.CITATION_HMMER

    def init():
        GC.hmmbuild_msafile = expanduser(GC.hmmbuild_msafile.strip())
        GC.hmmbuild_path = expanduser(GC.hmmbuild_path.strip())
        GC.hmmemit_path = expanduser(GC.hmmemit_path.strip())
        GC.hmmbuild_options = [i.strip() for i in GC.hmmbuild_options.strip().split()]
        GC.hmmemit_options = [i.strip() for i in GC.hmmemit_options.strip().split()]
        GC.HMMBuildEmit_build = False

    def generate():
        if not GC.HMMBuildEmit_build:
            makedirs(HMMBuildEmit_path)
            command = [GC.hmmbuild_path] + GC.hmmbuild_options + [HMMBuildEmit_path + "/" + HMM_filename, GC.hmmbuild_msafile]
            try:
                check_output(command)
            except FileNotFoundError:
                from os import chdir
                chdir(GC.START_DIR)
                assert False, "hmmbuild executable was not found: %s" % GC.hmmbuild_path
            GC.hmmemit_hmmfile = HMMBuildEmit_path + "/" + HMM_filename
            GC.HMMBuildEmit_build = True
        return SeedSequence_HMMEmit.generate()