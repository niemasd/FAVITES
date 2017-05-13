#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionTimeSample" module, where the transmission network is simulated by
GEMF (Sahneh et al. 2016) under the HPTN 071 (PopART) model.

In the descriptions below, the four "stages" are as follows:
- Stage 1: CD4 >= 500
- Stage 2: 350 <= CD4 < 500
- Stage 3: 200 <= CD4 < 350
- Stage 4: CD4 < 200

The states of the model are as follows:
- MSU  = Male Susceptible Uncircumcised
- MSPC = Male Susceptible Pending Circumcision
- MSCH = Male Susceptible Circumcised Healing
- MSC  = Male Susceptible Circumcised
- MIA  = Male Infected Acute
- MIAH = Male Infected Acute (Healing From Circumcision)
- MI1  = Male Infected Stage 1 (Untreated)
- MJ1  = Male Infected Stage 1 (Treatment Pending)
- MT1  = Male Infected Stage 1 (Treatment, Not Virally Supressed)
- MA1  = Male Infected Stage 1 (Treatment, Virally Supressed)
- MI2  = Male Infected Stage 2 (Untreated)
- MJ2  = Male Infected Stage 2 (Treatment Pending)
- MT2  = Male Infected Stage 2 (Treatment, Not Virally Supressed)
- MA2  = Male Infected Stage 2 (Treatment, Virally Supressed)
- MI3  = Male Infected Stage 3 (Untreated)
- MJ3  = Male Infected Stage 3 (Treatment Pending)
- MT3  = Male Infected Stage 3 (Treatment, Not Virally Supressed)
- MA3  = Male Infected Stage 3 (Treatment, Virally Supressed)
- MI4  = Male Infected Stage 4 (Untreated)
- MJ4  = Male Infected Stage 4 (Treatment Pending)
- MT4  = Male Infected Stage 4 (Treatment, Not Virally Supressed)
- MA4  = Male Infected Stage 4 (Treatment, Virally Supressed)
- FS   = Female Susceptible
- FIA  = Female Infected Acute
- FI1  = Female Infected Stage 1 (Untreated)
- FJ1  = Female Infected Stage 1 (Treatment Pending)
- FT1  = Female Infected Stage 1 (Treatment, Not Virally Supressed)
- FA1  = Female Infected Stage 1 (Treatment, Virally Supressed)
- FI2  = Female Infected Stage 2 (Untreated)
- FJ2  = Female Infected Stage 2 (Treatment Pending)
- FT2  = Female Infected Stage 2 (Treatment, Not Virally Supressed)
- FA2  = Female Infected Stage 2 (Treatment, Virally Supressed)
- FI3  = Female Infected Stage 3 (Untreated)
- FJ3  = Female Infected Stage 3 (Treatment Pending)
- FT3  = Female Infected Stage 3 (Treatment, Not Virally Supressed)
- FA3  = Female Infected Stage 3 (Treatment, Virally Supressed)
- FI4  = Female Infected Stage 4 (Untreated)
- FJ4  = Female Infected Stage 4 (Treatment Pending)
- FT4  = Female Infected Stage 4 (Treatment, Not Virally Supressed)
- FA4  = Female Infected Stage 4 (Treatment, Virally Supressed)
- D    = Deceased

Below is an adjacency list representing the model:
- MSU  -> [MSPC, MIA, D]
- MSPC -> [MSCH, MIA, D]
- MSCH -> [MSC, MIAH, D]
- MSC  -> [MIA, D]
- MIAH -> [MIA, D]
- MIA  -> [MI1, MI2, MI3, MI4, D]
- MI1  -> [MI2, MJ1, D]
- MI2  -> [MI3, MJ2, D]
- MI3  -> [MI4, MJ3, D]
- MI4  -> [MJ4, D]
- MJ1  -> [MJ2, MT1, D]
- MJ2  -> [MJ3, MT2, D]
- MJ3  -> [MJ4, MT3, D]
- MJ4  -> [MT4, D]
- MT1  -> [MI1, MT2, MA1, D]
- MT2  -> [MI2, MT3, MA2, D]
- MT3  -> [MI3, MT4, MA3, D]
- MT4  -> [MI4, MA4, D]
- MA1  -> [MI1, MA2, D]
- MA2  -> [MI2, MA3, D]
- MA3  -> [MI3, MA4, D]
- MA4  -> [MI4, D]
- FS   -> [FIA, D]
- FIA  -> [FI1, FI2, FI3, FI4, D]
- FI1  -> [FI2, FJ1, D]
- FI2  -> [FI3, FJ2, D]
- FI3  -> [FI4, FJ3, D]
- FI4  -> [FJ4, D]
- FJ1  -> [FJ2, FT1, D]
- FJ2  -> [FJ3, FT2, D]
- FJ3  -> [FJ4, FT3, D]
- FJ4  -> [FT4, D]
- FT1  -> [FI1, FT2, FA1, D]
- FT2  -> [FI2, FT3, FA2, D]
- FT3  -> [FI3, FT4, FA3, D]
- FT4  -> [FI4, FA4, D]
- FA1  -> [FI1, FA2, D]
- FA2  -> [FI2, FA3, D]
- FA3  -> [FI3, FA4, D]
- FA4  -> [FI4, D]
- D    -> []
'''
from TransmissionTimeSample import TransmissionTimeSample
from TransmissionTimeSample_TransmissionFile import TransmissionTimeSample_TransmissionFile
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from subprocess import call
from os.path import expanduser
from os import chdir,getcwd,makedirs

class TransmissionTimeSample_HIVPopARTGEMF(TransmissionTimeSample):
    def init():
        assert "TransmissionNodeSample_GEMF" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_GEMF module"
        assert "EndCriteria_GEMF" in str(MF.modules['EndCriteria']), "Must use EndCriteria_GEMF module"
        for p in dir(GC):
            if not p.startswith('__') and '_to_' in p:
                setattr(GC, p, float(getattr(GC,p)))
                assert getattr(GC,p) >= 0, "%s must be at least 0" % p
        GC.end_time = float(GC.end_time)
        assert GC.end_time > 0, "end_time must be positive"
        GC.end_events = int(GC.end_events)
        assert GC.end_events > 0, "end_events must be positive"
        GC.gemf_ready = False
        GC.gemf_state_to_num = {'MSU':0, 'MSPC':1, 'MSCH':2, 'MSC':3, 'MIAH':4, 'MIA':5, 'MI1':6, 'MI2':7, 'MI3':8, 'MI4':9, 'MJ1':10, 'MJ2':11, 'MJ3':12, 'MJ4':13, 'MT1':14, 'MT2':15, 'MT3':16, 'MT4':17, 'MA1':18, 'MA2':19, 'MA3':20, 'MA4':21, 'FS':22, 'FIA':23, 'FI1':24, 'FI2':25, 'FI3':26, 'FI4':27, 'FJ1':28, 'FJ2':29, 'FJ3':30, 'FJ4':31, 'FT1':32, 'FT2':33, 'FT3':34, 'FT4':35, 'FA1':36, 'FA2':37, 'FA3':38, 'FA4':39, 'D':40}
        GC.gemf_num_to_state = {GC.gemf_state_to_num[state]:state for state in GC.gemf_state_to_num}

    def prep_GEMF():
        # check for attributes in contact network nodes
        for node in GC.contact_network.nodes_iter():
            attr = node.get_attribute()
            assert 'MALE' in attr or 'FEMALE' in attr, "All nodes must have MALE or FEMALE in their attributes"
            assert not ('MALE' in attr and 'FEMALE' in attr), "Nodes cannot be both MALE and FEMALE"
            if 'MALE' in attr:
                assert 'CIRCUMCISED' in attr or 'UNCIRCUMCISED' in attr, "MALE nodes must be either CIRCUMCISED or UNCIRCUMCISED"
            else:
                assert 'CIRCUMCISED' not in attr, "FEMALE nodes cannot be CIRCUMCISED"

        # write GEMF parameter file
        orig_dir = getcwd()
        GC.gemf_path = expanduser(GC.gemf_path.strip())
        makedirs(GC.gemf_out_dir)
        f = open(GC.gemf_out_dir + "/para.txt",'w')
        f.write("[NODAL_TRAN_MATRIX]\n")
        f.write("0\t" + str(GC.hiv_msu_to_mspc) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_msu_to_d) + "\n")
        f.write("0\t0\t" + str(GC.hiv_mspc_to_msch) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mspc_to_d) + "\n")
        f.write("0\t0\t0\t" + str(GC.hiv_msch_to_msc) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_msch_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_msc_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t" + str(GC.hiv_miah_to_mia) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_miah_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mia_to_mi1) + "\t" + str(GC.hiv_mia_to_mi2) + "\t" + str(GC.hiv_mia_to_mi3) + "\t" + str(GC.hiv_mia_to_mi4) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mia_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mi1_to_mi2) + "\t0\t0\t" + str(GC.hiv_mi1_to_mj1) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mi1_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mi2_to_mi3) + "\t0\t0\t" + str(GC.hiv_mi2_to_mj2) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mi2_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mi3_to_mi4) + "\t0\t0\t" + str(GC.hiv_mi3_to_mj3) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mi3_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mi4_to_mj4) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mi4_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mj1_to_mj2) + "\t0\t0\t" + str(GC.hiv_mj1_to_mt1) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mj1_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mj2_to_mj3) + "\t0\t0\t" + str(GC.hiv_mj2_to_mt2) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mj2_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mj3_to_mj4) + "\t0\t0\t" + str(GC.hiv_mj3_to_mt3) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mj3_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mj4_to_mt4) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mj4_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mt1_to_mi1) + "\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mt1_to_mt2) + "\t0\t0\t" + str(GC.hiv_mt1_to_ma1) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mt1_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mt2_to_mi2) + "\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mt2_to_mt3) + "\t0\t0\t" + str(GC.hiv_mt2_to_ma2) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mt2_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mt3_to_mi3) + "\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mt3_to_mt4) + "\t0\t0\t" + str(GC.hiv_mt3_to_ma3) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mt3_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mt4_to_mi4) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mt4_to_ma4) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_mt4_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t" + str(GC.hiv_ma1_to_mi1) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_ma1_to_ma2) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_ma1_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_ma2_to_mi2) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_ma2_to_ma3) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_ma2_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_ma3_to_mi3) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_ma3_to_ma4) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_ma3_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_ma4_to_mi4) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_ma4_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_fs_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_fia_to_fi1) + "\t" + str(GC.hiv_fia_to_fi2) + "\t" + str(GC.hiv_fia_to_fi3) + "\t" + str(GC.hiv_fia_to_fi4) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_fia_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_fi1_to_fi2) + "\t0\t0\t" + str(GC.hiv_fi1_to_fj1) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_fi1_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_fi2_to_fi3) + "\t0\t0\t" + str(GC.hiv_fi2_to_fj2) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_fi2_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_fi3_to_fi4) + "\t0\t0\t" + str(GC.hiv_fi3_to_fj3) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_fi3_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_fi4_to_fj4) + "\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_fi4_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_fj1_to_fj2) + "\t0\t0\t" + str(GC.hiv_fj1_to_ft1) + "\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_fj1_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_fj2_to_fj3) + "\t0\t0\t" + str(GC.hiv_fj2_to_ft2) + "\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_fj2_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_fj3_to_fj4) + "\t0\t0\t" + str(GC.hiv_fj3_to_ft3) + "\t0\t0\t0\t0\t0\t" + str(GC.hiv_fj3_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_fj4_to_ft4) + "\t0\t0\t0\t0\t" + str(GC.hiv_fj4_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_ft1_to_fi1) + "\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_ft1_to_ft2) + "\t0\t0\t" + str(GC.hiv_ft1_to_fa1) + "\t0\t0\t0\t" + str(GC.hiv_ft1_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_ft2_to_fi2) + "\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_ft2_to_ft3) + "\t0\t0\t" + str(GC.hiv_ft2_to_fa2) + "\t0\t0\t" + str(GC.hiv_ft2_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_ft3_to_fi3) + "\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_ft3_to_ft4) + "\t0\t0\t" + str(GC.hiv_ft3_to_fa3) + "\t0\t" + str(GC.hiv_ft3_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_ft4_to_fi4) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_ft4_to_fa4) + "\t" + str(GC.hiv_ft4_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_fa1_to_fi1) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_fa1_to_fa2) + "\t0\t0\t" + str(GC.hiv_fa1_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_fa2_to_fi2) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_fa2_to_fa3) + "\t0\t" + str(GC.hiv_fa2_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_fa3_to_fi3) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_fa3_to_fa4) + "\t" + str(GC.hiv_fa3_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_fa4_to_fi4) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_fa4_to_d) + "\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
        f.write("\n")
        infectious = ['MIAH', 'MIA', 'MI1', 'MI2', 'MI3', 'MI4', 'MJ1', 'MJ2', 'MJ3', 'MJ4', 'MT1', 'MT2', 'MT3', 'MT4', 'MA1', 'MA2', 'MA3', 'MA4', 'FIA', 'FI1', 'FI2', 'FI3', 'FI4', 'FJ1', 'FJ2', 'FJ3', 'FJ4', 'FT1', 'FT2', 'FT3', 'FT4', 'FA1', 'FA2', 'FA3', 'FA4']
        f.write("[EDGED_TRAN_MATRIX]\n")
        for _ in infectious:
            by = _.lower()
            f.write("0\t0\t0\t0\t0\t" + str(getattr(GC,'hiv_msu_to_mia_by_' + by)) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t" + str(getattr(GC,'hiv_mspc_to_mia_by_' + by)) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t" + str(getattr(GC,'hiv_msch_to_miah_by_' + by)) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t" + str(getattr(GC,'hiv_msc_to_mia_by_' + by)) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(getattr(GC,'hiv_fs_to_fia_by_' + by)) + "\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")
            f.write('\n')
        f.write("[STATUS_BEGIN]\n0\n\n")
        f.write("[INDUCER_LIST]\n" + ' '.join([str(GC.gemf_state_to_num[i]) for i in infectious]) + "\n\n")
        f.write("[SIM_ROUNDS]\n1\n\n")
        f.write("[INTERVAL_NUM]\n1\n\n")
        f.write("[MAX_TIME]\n" + str(GC.end_time) + "\n\n")
        f.write("[MAX_EVENTS]\n" + str(GC.end_events) + "\n\n")
        f.write("[DIRECTED]\n1\n\n")
        f.write("[SHOW_INDUCER]\n1\n\n")
        f.write("[DATA_FILE]\n" + '\n'.join(["network.txt"]*len(infectious)) + "\n\n")
        f.write("[STATUS_FILE]\nstatus.txt\n\n")
        f.write("[OUT_FILE]\noutput.txt")
        f.close()

        # write GEMF network file
        f = open(GC.gemf_out_dir + "/network.txt",'w')
        num2node = {}
        node2num = {}
        for edge in GC.contact_network.edges_iter():
            u = edge.get_from()
            v = edge.get_to()
            if u not in node2num:
                num = len(node2num) + 1
                node2num[u] = num
                num2node[num] = u
            if v not in node2num:
                num = len(node2num) + 1
                node2num[v] = num
                num2node[num] = v
            f.write(str(node2num[u]) + '\t' + str(node2num[v]) + '\n')
        f.close()

        # write GEMF to original mapping
        f = open(GC.gemf_out_dir + "/gemf2orig.json",'w')
        f.write(str({num:num2node[num].get_name() for num in num2node}))
        f.close()

        # write GEMF status file (see above for the states)
        f = open(GC.gemf_out_dir + "/status.txt",'w')
        seeds = {seed for seed in GC.seed_nodes} # seed nodes are assumed to be in acute infection
        for num in sorted(num2node.keys()):
            node = num2node[num]
            attr = node.get_attribute()
            if node in seeds:
                if 'MALE' in attr:
                    f.write(str(GC.gemf_state_to_num['MIA']) + "\n") # PopART-specific
                    node.gemf_state = GC.gemf_state_to_num['MIA']
                else:
                    f.write(str(GC.gemf_state_to_num['FIA']) + "\n") # PopART-specific
                    node.gemf_state = GC.gemf_state_to_num['FIA']
            else:
                if 'MALE' in attr:
                    if 'CIRCUMCISED' in attr:
                        f.write(str(GC.gemf_state_to_num['MSC']) + "\n") # PopART-specific
                        node.gemf_state = GC.gemf_state_to_num['MSC']
                    else:
                        f.write(str(GC.gemf_state_to_num['MSU']) + "\n") # PopART-specific
                        node.gemf_state = GC.gemf_state_to_num['MSU']
                else:
                    f.write(str(GC.gemf_state_to_num['FS']) + "\n") # PopART-specific
                    node.gemf_state = GC.gemf_state_to_num['FS']
        f.close()

        # run GEMF
        chdir(GC.gemf_out_dir)
        try:
            call([GC.gemf_path], stdout=open("log.txt",'w'))
        except FileNotFoundError:
            chdir(GC.START_DIR)
            assert False, "GEMF executable was not found: %s" % GC.gemf_path
        chdir(orig_dir)

        # reload edge-based matrices for ease of use
        matrices = open(GC.gemf_out_dir + '/para.txt').read().strip()
        matrices = [[[float(e) for e in l.split()] for l in m.splitlines()] for m in matrices[matrices.index('[EDGED_TRAN_MATRIX]'):matrices.index('\n\n[STATUS_BEGIN]')].replace('[EDGED_TRAN_MATRIX]\n','').split('\n\n')]
        matrices = {GC.gemf_state_to_num[infectious[i]]:matrices[i] for i in range(len(infectious))}

        # convert GEMF output to FAVITES transmission network format
        GC.transmission_num = 0
        GC.transmission_state = set() # 'node' and 'time'
        GC.transmission_file = []
        for line in open(GC.gemf_out_dir + "/output.txt"):
            parts = [i.strip() for i in line.split()]
            t     = parts[0]
            rate  = parts[1]
            vNum  = parts[2]
            pre   = int(parts[3])
            post  = int(parts[4])
            lists = parts[-1]
            lists = lists.split('],[')
            lists[0] += ']'
            lists[-1] = '[' + lists[-1]
            for i in range(1,len(lists)-1):
                if '[' not in lists[i]:
                    lists[i] = '[' + lists[i] + ']'
            lists = [eval(l) for l in lists]
            uNums = []
            for l in lists:
                uNums.extend(l)
            if post == GC.gemf_state_to_num['D']:
                vName = num2node[int(vNum)].get_name()
                GC.transmission_file.append((vName,vName,float(t)))
            elif len(lists[0]) == 0:
                uNodes = [num2node[num] for num in uNums]
                uRates = [matrices[uNode.gemf_state][pre][post] for uNode in uNodes]
                die = {uNodes[i]:GC.prob_exp_min(i, uRates) for i in range(len(uNodes))}
                u = GC.roll(die) # roll die weighted by exponential infectious rates
                v = num2node[int(vNum)]
                GC.transmission_file.append((u.get_name(),v.get_name(),float(t)))
            num2node[int(vNum)].gemf_state = post
        assert len(GC.transmission_file) != 0, "GEMF didn't output any transmissions"
        GC.gemf_ready = True

    def sample_time():
        if not GC.gemf_ready:
            TransmissionTimeSample_HIVPopARTGEMF.prep_GEMF()
        return TransmissionTimeSample_TransmissionFile.sample_time()