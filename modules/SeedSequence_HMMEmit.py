#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSequence" module, implemented using hmmemit.

Do not use the -o argument, as we use standard output to parse hmmemit output.

If you specify a file with
multiple profile HMMs, each seed sequence sampling will generate a sequence from
all of the profile HMMs and will return a random one with uniform probability.
'''
from SeedSequence import SeedSequence
import FAVITES_GlobalContext as GC
from subprocess import check_output
from random import choice
from os.path import expanduser

class SeedSequence_HMMEmit(SeedSequence):
    '''
    Implement the ``SeedSequence'' using hmmemit
    '''

    def init():
        GC.hmmemit_hmmfile = expanduser(GC.hmmemit_hmmfile.strip())
        GC.hmmemit_path = expanduser(GC.hmmemit_path.strip())
        GC.hmmemit_options = [i.strip() for i in GC.hmmemit_options.strip().split()]

    def generate():
        command = [GC.hmmemit_path] + GC.hmmemit_options + [GC.hmmemit_hmmfile]
        return ''.join(choice(check_output(command).decode("ascii").strip().split('>')[1:]).splitlines()[1:])