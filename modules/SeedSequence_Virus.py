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
URL = {
    # HIV-1 All Subtypes (Los Alamos)
    'HIV1-DNA-ENV':    'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_FLT_2016_env_DNA.hmm',
    'HIV1-DNA-GAG':    'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_FLT_2016_gag_DNA.hmm',
    'HIV1-DNA-GENOME': 'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_FLT_2016_genome_DNA.hmm',
    'HIV1-DNA-NEF':    'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_FLT_2016_nef_DNA.hmm',
    'HIV1-DNA-POL':    'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_FLT_2016_pol_DNA.hmm',
    'HIV1-DNA-REV':    'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_FLT_2016_rev_DNA.hmm',
    'HIV1-DNA-TAT':    'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_FLT_2016_tat_DNA.hmm',
    'HIV1-DNA-VIF':    'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_FLT_2016_vif_DNA.hmm',
    'HIV1-DNA-VPR':    'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_FLT_2016_vpr_DNA.hmm',
    'HIV1-DNA-VPU':    'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_FLT_2016_vpu_DNA.hmm',

    # HIV-1 All M Group (A-K + Recombinants) (Los Alamos)
    'HIV1-M-DNA-ENV':    'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_M_FLT_2016_env_DNA.hmm',
    'HIV1-M-DNA-GAG':    'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_M_FLT_2016_gag_DNA.hmm',
    'HIV1-M-DNA-GENOME': 'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_M_FLT_2016_genome_DNA.hmm',
    'HIV1-M-DNA-NEF':    'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_M_FLT_2016_nef_DNA.hmm',
    'HIV1-M-DNA-POL':    'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_M_FLT_2016_pol_DNA.hmm',
    'HIV1-M-DNA-REV':    'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_M_FLT_2016_rev_DNA.hmm',
    'HIV1-M-DNA-TAT':    'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_M_FLT_2016_tat_DNA.hmm',
    'HIV1-M-DNA-VIF':    'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_M_FLT_2016_vif_DNA.hmm',
    'HIV1-M-DNA-VPR':    'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_M_FLT_2016_vpr_DNA.hmm',
    'HIV1-M-DNA-VPU':    'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_M_FLT_2016_vpu_DNA.hmm',

    # HIV-1 M Group Without Recombinants (A-K) (Los Alamos)
    'HIV1-M-NORECOMB-DNA-ENV':    'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_M_NORECOMB_FLT_2016_env_DNA.hmm',
    'HIV1-M-NORECOMB-DNA-GAG':    'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_M_NORECOMB_FLT_2016_gag_DNA.hmm',
    'HIV1-M-NORECOMB-DNA-GENOME': 'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_M_NORECOMB_FLT_2016_genome_DNA.hmm',
    'HIV1-M-NORECOMB-DNA-NEF':    'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_M_NORECOMB_FLT_2016_nef_DNA.hmm',
    'HIV1-M-NORECOMB-DNA-POL':    'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_M_NORECOMB_FLT_2016_pol_DNA.hmm',
    'HIV1-M-NORECOMB-DNA-REV':    'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_M_NORECOMB_FLT_2016_rev_DNA.hmm',
    'HIV1-M-NORECOMB-DNA-TAT':    'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_M_NORECOMB_FLT_2016_tat_DNA.hmm',
    'HIV1-M-NORECOMB-DNA-VIF':    'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_M_NORECOMB_FLT_2016_vif_DNA.hmm',
    'HIV1-M-NORECOMB-DNA-VPR':    'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_M_NORECOMB_FLT_2016_vpr_DNA.hmm',
    'HIV1-M-NORECOMB-DNA-VPU':    'https://raw.githubusercontent.com/niemasd/Virus-Data/master/HIV/profile_HMMs/DNA/HIV1_M_NORECOMB_FLT_2016_vpu_DNA.hmm',
}

class SeedSequence_Virus(SeedSequence):
    def cite():
        return GC.CITATION_HMMER

    def init():
        GC.hmmemit_path = expanduser(GC.hmmemit_path.strip())
        GC.viral_sequence_type = GC.viral_sequence_type.strip()
        assert GC.viral_sequence_type in URL, "Invalid choice for viral_sequence_type: %s. Valid choices: %s" % (GC.viral_sequence_type, ', '.join(URL.keys()))

    def generate():
        makedirs(HMM_FOLDER, exist_ok=True)
        hmm_file = HMM_FOLDER + '/' + URL[GC.viral_sequence_type].split('/')[-1]
        urlretrieve(URL[GC.viral_sequence_type], hmm_file)
        command = [GC.hmmemit_path, hmm_file]
        try:
            return ''.join(choice(check_output(command).decode("ascii").strip().replace('-','').split('>')[1:]).splitlines()[1:])
        except FileNotFoundError:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "hmmemit executable was not found: %s" % GC.hmmemit_path
