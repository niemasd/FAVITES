#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionTimeSample" module, where the transmission network is simulated by
GEMF (Sahneh et al. 2016) under the SIS model.
'''
from TransmissionTimeSample import TransmissionTimeSample
from TransmissionTimeSample_TransmissionFile import TransmissionTimeSample_TransmissionFile
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from subprocess import call
from os.path import expanduser
from os import chdir,getcwd,makedirs
from random import choice

class TransmissionTimeSample_SISGEMF(TransmissionTimeSample):
    def init():
        assert "TransmissionNodeSample_SISGEMF" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_SISGEMF module"
        assert "EndCriteria_GEMF" in str(MF.modules['EndCriteria']), "Must use EndCriteria_GEMF module"
        GC.sis_beta = float(GC.sis_beta)
        assert GC.sis_beta >= 0, "sis_beta must be at least 0"
        GC.sis_delta = float(GC.sis_delta)
        assert GC.sis_delta >= 0, "sis_delta must be at least 0"
        GC.end_time = float(GC.end_time)
        assert GC.end_time > 0, "end_time must be positive"
        GC.end_transmissions = int(GC.end_transmissions)
        assert GC.end_transmissions > 0, "end_transmissions must be positive"
        GC.gemf_ready = False

    def prep_GEMF():
        # write GEMF parameter file
        GC.gemf_path = expanduser(GC.gemf_path.strip())
        makedirs("GEMF_output")
        f = open("GEMF_output/para.txt",'w')
        f.write("[NODAL_TRAN_MATRIX]\n0\t0\n" + str(GC.sis_delta) + "\t0\n\n") # SIS-specific
        f.write("[EDGED_TRAN_MATRIX]\n0\t" + str(GC.sis_beta) + "\n0\t0\n\n")  # SIS-specific
        f.write("[STATUS_BEGIN]\n0\n\n")
        f.write("[INDUCER_LIST]\n1\n\n")
        f.write("[SIM_ROUNDS]\n1\n\n")
        f.write("[INTERVAL_NUM]\n1\n\n")
        f.write("[MAX_TIME]\n" + str(GC.end_time) + "\n\n")
        f.write("[MAX_EVENTS]\n" + str(GC.end_transmissions) + "\n\n")
        f.write("[DIRECTED]\n1\n\n")
        f.write("[SHOW_INDUCER]\n1\n\n")
        f.write("[DATA_FILE]\nnetwork.txt\n\n")
        f.write("[STATUS_FILE]\nstatus.txt\n\n")
        f.write("[OUT_FILE]\noutput.txt")
        f.close()

        # write GEMF network file
        f = open("GEMF_output/network.txt",'w')
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

        # write GEMF status file (0 = S, 1 = I)
        f = open("GEMF_output/status.txt",'w')
        seeds = {seed for seed in GC.seed_nodes}
        for num in sorted(num2node.keys()):
            node = num2node[num]
            if node in seeds:
                f.write("1\n") # SIS-specific
            else:
                f.write("0\n") # SIS-specific
        f.close()

        # run GEMF
        orig_dir = getcwd()
        chdir("GEMF_output")
        call([GC.gemf_path], stdout=open("log.txt",'w'))
        chdir(orig_dir)

        # convert GEMF output to FAVITES transmission network format
        GC.transmission_num = 0
        GC.transmission_state = set() # 'node' and 'time'
        GC.transmission_file = []
        for line in open("GEMF_output/output.txt"):
            t,rate,vNum,pre,post,num0,num1,lists = [i.strip() for i in line.split()]
            uNums = [u for u in lists.split('],[')[1][:-1].split(',') if u != '']
            if len(uNums) != 0:
                uNum = choice(uNums) # randomly choose a single infector
                u,v = num2node[int(uNum)],num2node[int(vNum)]
                GC.transmission_file.append((u.get_name(),v.get_name(),float(t)))
        assert len(GC.transmission_file) != 0, "GEMF didn't output any transmissions"
        GC.gemf_ready = True

    def sample_time():
        if not GC.gemf_ready:
            TransmissionTimeSample_SISGEMF.prep_GEMF()
        return TransmissionTimeSample_TransmissionFile.sample_time()