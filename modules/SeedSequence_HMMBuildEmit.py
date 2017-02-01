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

GC.HMMBuildEmit_path = "HMMBuildEmit_files"
GC.HMM_filename = "seedseq.hmm"

class SeedSequence_HMMBuildEmit(SeedSequence):
    '''
    Implement the ``SeedSequence'' using hmmbuild to build a profile HMM from
    an input MSA, and then use hmmemit to generate seed sequences from the
    resulting profile HMM
    '''

    def init():
        GC.hmmbuild_msafile = expanduser(GC.hmmbuild_msafile.strip())
        GC.hmmbuild_path = expanduser(GC.hmmbuild_path.strip())
        GC.hmmemit_path = expanduser(GC.hmmemit_path.strip())
        GC.hmmbuild_options = [i.strip() for i in GC.hmmbuild_options.strip().split()]
        GC.hmmemit_options = [i.strip() for i in GC.hmmemit_options.strip().split()]
        GC.HMMBuildEmit_build = False

    def generate():
        if not GC.HMMBuildEmit_build:
            makedirs(GC.HMMBuildEmit_path)
            command = [GC.hmmbuild_path] + GC.hmmbuild_options + [GC.HMMBuildEmit_path + "/" + GC.HMM_filename, GC.hmmbuild_msafile]
            check_output(command)
            GC.hmmemit_hmmfile = GC.HMMBuildEmit_path + "/" + GC.HMM_filename
            GC.HMMBuildEmit_build = True
        command = [GC.hmmemit_path] + GC.hmmemit_options + [GC.hmmemit_hmmfile]
        return SeedSequence_HMMEmit.generate()