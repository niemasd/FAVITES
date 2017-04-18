#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSequence" module, which samples HIV sequences using a profile HMM generated
from a multiple sequence alignment from Los Alamos.
'''
from SeedSequence import SeedSequence
import FAVITES_GlobalContext as GC
from subprocess import check_output
from random import choice
from os.path import expanduser
from os import makedirs
from urllib.request import urlretrieve

HIV_PATH = "HIV_profile_HMM"
URL = { # URLs to preconstructed HIV profile HMMs from Los Alamos
    'DNA-ENV':    'https://raw.githubusercontent.com/niemasd/HIV-Data/master/profile_HMMs/DNA/HIV1_FLT_2016_env_DNA.hmm',
    'DNA-GENOME': 'https://raw.githubusercontent.com/niemasd/HIV-Data/master/profile_HMMs/DNA/HIV1_FLT_2016_genome_DNA.hmm',
    'DNA-POL':    'https://raw.githubusercontent.com/niemasd/HIV-Data/master/profile_HMMs/DNA/HIV1_FLT_2016_pol_DNA.hmm'
}

class SeedSequence_HIV(SeedSequence):
    def init():
        GC.hmmemit_path = expanduser(GC.hmmemit_path.strip())
        GC.HIV_region = GC.HIV_region.strip()
        assert GC.HIV_region in URL, "Invalid choice for HIV_region: %s" % GC.HIV_region

    def generate():
        makedirs(HIV_PATH)
        hmm_file = HIV_PATH + '/' + URL[GC.HIV_region].split('/')[-1]
        urlretrieve(URL[GC.HIV_region], hmm_file)
        command = [GC.hmmemit_path, hmm_file]
        try:
            return ''.join(choice(check_output(command).decode("ascii").strip().replace('-','').split('>')[1:]).splitlines()[1:])
        except FileNotFoundError:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "hmmemit executable was not found: %s" % GC.hmmemit_path