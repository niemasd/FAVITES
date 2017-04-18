#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSequence" module, which samples viral sequences using a profile HMM
generated from a multiple sequence alignment from some public dataset.

Currently, it only contains HIV alignments from Los Alamos.
'''
from SeedSequence import SeedSequence
import FAVITES_GlobalContext as GC
from subprocess import check_output
from random import choice
from os.path import expanduser
from os import makedirs
from urllib.request import urlretrieve

HMM_FOLDER = "virus_profile_HMM"
URL = { # URLs to preconstructed HIV profile HMMs from Los Alamos
    'HIV-DNA-ENV':    'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_FLT_2016_env_DNA.hmm',
    'HIV-DNA-GENOME': 'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_FLT_2016_genome_DNA.hmm',
    'HIV-DNA-POL':    'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_FLT_2016_pol_DNA.hmm'
}

class SeedSequence_Virus(SeedSequence):
    def init():
        GC.hmmemit_path = expanduser(GC.hmmemit_path.strip())
        GC.viral_sequence_type = GC.viral_sequence_type.strip()
        assert GC.viral_sequence_type in URL, "Invalid choice for viral_sequence_type: %s" % GC.viral_sequence_type

    def generate():
        makedirs(HMM_FOLDER)
        hmm_file = HMM_FOLDER + '/' + URL[GC.viral_sequence_type].split('/')[-1]
        urlretrieve(URL[GC.viral_sequence_type], hmm_file)
        command = [GC.hmmemit_path, hmm_file]
        try:
            return ''.join(choice(check_output(command).decode("ascii").strip().replace('-','').split('>')[1:]).splitlines()[1:])
        except FileNotFoundError:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "hmmemit executable was not found: %s" % GC.hmmemit_path