#! /usr/bin/env python3
'''
Niema Moshiri 2020

"TransmissionTimeSample" module, where the transmission network is simulated by
GEMF (Sahneh et al. 2016) under the SAPHIRE model (Hao et al., 2020) containing
the following 7 states: Susceptible (S), Exposed (E), Presymptomatic (P),
Ascertained Infectious (I), Unascertained Infectious (A), Hospitalized (H), and
Recovered (R). Individuals can be "seed infected" (i.e., infected from outside
the contact network) after time 0.

Susceptible individuals can be exposed to the virus by infection (S -> E).
Exposed individuals become presymptomatic (E -> P). Presymptomatic individuals
become either ascertained (P -> I) or unascertained (P -> A). Ascertained
individuals can become hospitalized (I -> H). Ascertained, unascertained, and
hospitalized individuals can recover (I -> R, A -> R, and H -> R).
'''
from TransmissionTimeSample import TransmissionTimeSample
from TransmissionTimeSample_SAAPPHIIREGEMF import TransmissionTimeSample_SAAPPHIIREGEMF
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class TransmissionTimeSample_SAPHIREGEMF(TransmissionTimeSample):
    def cite():
        return GC.CITATION_GEMF

    def init():
        assert "TransmissionNodeSample_GEMF" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_GEMF module"
        assert "EndCriteria_GEMF" in str(MF.modules['EndCriteria']), "Must use EndCriteria_GEMF module"
        GC.saapphiire_freq_s = GC.saphire_freq_s
        GC.saapphiire_freq_e = GC.saphire_freq_e
        GC.saapphiire_freq_p1 = 0
        GC.saapphiire_freq_p2 = GC.saphire_freq_p
        GC.saapphiire_freq_i1 = 0
        GC.saapphiire_freq_i2 = GC.saphire_freq_i
        GC.saapphiire_freq_a1 = 0
        GC.saapphiire_freq_a2 = GC.saphire_freq_a
        GC.saapphiire_freq_h = GC.saphire_freq_h
        GC.saapphiire_freq_r = GC.saphire_freq_r
        GC.saapphiire_s_to_e_seed = GC.saphire_s_to_e_seed
        GC.saapphiire_e_to_p1 = GC.saphire_e_to_p
        GC.saapphiire_p1_to_p2 = GC.C_INT_MAX
        GC.saapphiire_p2_to_i1 = GC.saphire_p_to_i
        GC.saapphiire_p2_to_a1 = GC.saphire_p_to_a
        GC.saapphiire_i1_to_i2 = GC.C_INT_MAX
        GC.saapphiire_i1_to_h = 0
        GC.saapphiire_i2_to_h = GC.saphire_i_to_h
        GC.saapphiire_i2_to_r = GC.saphire_i_to_r
        GC.saapphiire_a1_to_a2 = GC.C_INT_MAX
        GC.saapphiire_a2_to_r = GC.saphire_a_to_r
        GC.saapphiire_h_to_r = GC.saphire_h_to_r
        GC.saapphiire_s_to_e_by_e  = GC.saphire_s_to_e_by_e
        GC.saapphiire_s_to_e_by_p1 = 0
        GC.saapphiire_s_to_e_by_p2 = GC.saphire_s_to_e_by_p
        GC.saapphiire_s_to_e_by_i1 = 0
        GC.saapphiire_s_to_e_by_i2 = GC.saphire_s_to_e_by_i
        GC.saapphiire_s_to_e_by_a1 = 0
        GC.saapphiire_s_to_e_by_a2 = GC.saphire_s_to_e_by_a
        TransmissionTimeSample_SAAPPHIIREGEMF.init()

    def prep_GEMF():
        TransmissionTimeSample_SAAPPHIIREGEMF.prep_GEMF()

    def sample_time():
        return TransmissionTimeSample_SAAPPHIIREGEMF.sample_time()
