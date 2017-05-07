#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionTimeSample" module, where the transmission network is simulated by
GEMF (Sahneh et al. 2016) under the HIV-ART model developed by Granich et al
(2008).

The states of the model are as follows:
- NS = Non-Susceptible
- S  = Susceptible
- I1 = Infected Stage 1
- I2 = Infected Stage 2
- I3 = Infected Stage 3
- I4 = Infected Stage 4
- A1 = ART Stage 1
- A2 = ART Stage 2
- A3 = ART Stage 3
- A4 = ART Stage 4
- D  = Deceased

Below is an adjacency list representing the model:
- NS -> [S, D]
- S  -> [I1, D]
- I1 -> [I2, A1, D]
- I2 -> [I3, A2, D]
- I3 -> [I4, A3, D]
- I4 -> [A4, D]
- A1 -> [I1, A2, D]
- A2 -> [I2, A3, D]
- A3 -> [I3, A4, D]
- A4 -> [I4, D]
- D  -> []
'''
from TransmissionTimeSample import TransmissionTimeSample
from TransmissionTimeSample_TransmissionFile import TransmissionTimeSample_TransmissionFile
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from subprocess import call
from os.path import expanduser
from os import chdir,getcwd,makedirs
from random import choice

class TransmissionTimeSample_HIVARTGranichGEMF(TransmissionTimeSample):
    def init():
        assert "TransmissionNodeSample_GEMF" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_GEMF module"
        assert "EndCriteria_GEMF" in str(MF.modules['EndCriteria']), "Must use EndCriteria_GEMF module"
        GC.hiv_ns_to_s = float(GC.hiv_ns_to_s)
        assert GC.hiv_ns_to_s >= 0, "hiv_ns_to_s must be at least 0"
        GC.hiv_ns_to_d = float(GC.hiv_ns_to_d)
        assert GC.hiv_ns_to_d >= 0, "hiv_ns_to_d must be at least 0"
        GC.hiv_s_to_i1 = float(GC.hiv_s_to_i1)
        assert GC.hiv_s_to_i1 >= 0, "hiv_s_to_i1 must be at least 0"
        GC.hiv_s_to_d = float(GC.hiv_s_to_d)
        assert GC.hiv_s_to_d >= 0, "hiv_s_to_d must be at least 0"
        GC.hiv_i1_to_i2 = float(GC.hiv_i1_to_i2)
        assert GC.hiv_i1_to_i2 >= 0, "hiv_i1_to_i2 must be at least 0"
        GC.hiv_i1_to_a1 = float(GC.hiv_i1_to_a1)
        assert GC.hiv_i1_to_a1 >= 0, "hiv_i1_to_a1 must be at least 0"
        GC.hiv_i1_to_d = float(GC.hiv_i1_to_d)
        assert GC.hiv_i1_to_d >= 0, "hiv_i1_to_d must be at least 0"
        GC.hiv_i2_to_i3 = float(GC.hiv_i2_to_i3)
        assert GC.hiv_i2_to_i3 >= 0, "hiv_i2_to_i3 must be at least 0"
        GC.hiv_i2_to_a2 = float(GC.hiv_i2_to_a2)
        assert GC.hiv_i2_to_a2 >= 0, "hiv_i2_to_a2 must be at least 0"
        GC.hiv_i2_to_d = float(GC.hiv_i2_to_d)
        assert GC.hiv_i2_to_d >= 0, "hiv_i2_to_d must be at least 0"
        GC.hiv_i3_to_i4 = float(GC.hiv_i3_to_i4)
        assert GC.hiv_i3_to_i4 >= 0, "hiv_i3_to_i4 must be at least 0"
        GC.hiv_i3_to_a3 = float(GC.hiv_i3_to_a3)
        assert GC.hiv_i3_to_a3 >= 0, "hiv_i3_to_a3 must be at least 0"
        GC.hiv_i3_to_d = float(GC.hiv_i3_to_d)
        assert GC.hiv_i3_to_d >= 0, "hiv_i3_to_d must be at least 0"
        GC.hiv_i4_to_a4 = float(GC.hiv_i4_to_a4)
        assert GC.hiv_i4_to_a4 >= 0, "hiv_i4_to_a4 must be at least 0"
        GC.hiv_i4_to_d = float(GC.hiv_i4_to_d)
        assert GC.hiv_i4_to_d >= 0, "hiv_i4_to_d must be at least 0"
        GC.hiv_a1_to_a2 = float(GC.hiv_a1_to_a2)
        assert GC.hiv_a1_to_a2 >= 0, "hiv_a1_to_a2 must be at least 0"
        GC.hiv_a1_to_i1 = float(GC.hiv_a1_to_i1)
        assert GC.hiv_a1_to_i1 >= 0, "hiv_a1_to_i1 must be at least 0"
        GC.hiv_a1_to_d = float(GC.hiv_a1_to_d)
        assert GC.hiv_a1_to_d >= 0, "hiv_a1_to_d must be at least 0"
        GC.hiv_a2_to_a3 = float(GC.hiv_a2_to_a3)
        assert GC.hiv_a2_to_a3 >= 0, "hiv_a2_to_a3 must be at least 0"
        GC.hiv_a2_to_i2 = float(GC.hiv_a2_to_i2)
        assert GC.hiv_a2_to_i2 >= 0, "hiv_a2_to_i2 must be at least 0"
        GC.hiv_a2_to_d = float(GC.hiv_a2_to_d)
        assert GC.hiv_a2_to_d >= 0, "hiv_a2_to_d must be at least 0"
        GC.hiv_a3_to_a4 = float(GC.hiv_a3_to_a4)
        assert GC.hiv_a3_to_a4 >= 0, "hiv_a3_to_a4 must be at least 0"
        GC.hiv_a3_to_i3 = float(GC.hiv_a3_to_i3)
        assert GC.hiv_a3_to_i3 >= 0, "hiv_a3_to_i3 must be at least 0"
        GC.hiv_a3_to_d = float(GC.hiv_a3_to_d)
        assert GC.hiv_a3_to_d >= 0, "hiv_a3_to_d must be at least 0"
        GC.hiv_a4_to_i4 = float(GC.hiv_a4_to_i4)
        assert GC.hiv_a4_to_i4 >= 0, "hiv_a4_to_i4 must be at least 0"
        GC.hiv_a4_to_d = float(GC.hiv_a4_to_d)
        assert GC.hiv_a4_to_d >= 0, "hiv_a4_to_d must be at least 0"
        GC.end_time = float(GC.end_time)
        assert GC.end_time > 0, "end_time must be positive"
        GC.end_events = int(GC.end_events)
        assert GC.end_events > 0, "end_events must be positive"
        GC.gemf_ready = False
        GC.gemf_state_to_num = {'NS':0, 'S':1, 'I1':2, 'I2':3, 'I3':4, 'I4':5, 'A1':6, 'A2':7, 'A3':8, 'A4':9, 'D':10}
        GC.gemf_num_to_state = {GC.gemf_state_to_num[state]:state for state in GC.gemf_state_to_num}

    def prep_GEMF():
        # write GEMF parameter file
        orig_dir = getcwd()
        GC.gemf_path = expanduser(GC.gemf_path.strip())
        makedirs(GC.gemf_out_dir)
        f = open(GC.gemf_out_dir + "/para.txt",'w')
        f.write("[NODAL_TRAN_MATRIX]\n0\t" + str(GC.hiv_ns_to_s) + "\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_ns_to_d) + "\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_s_to_d) + "\n0\t0\t0\t" + str(GC.hiv_i1_to_i2) + "\t0\t0\t" + str(GC.hiv_i1_to_a1) + "\t0\t0\t0\t" + str(GC.hiv_i1_to_d) + "\n0\t0\t0\t0\t" + str(GC.hiv_i2_to_i3) + "\t0\t0\t" + str(GC.hiv_i2_to_a2) + "\t0\t0\t" + str(GC.hiv_i2_to_d) + "\n0\t0\t0\t0\t0\t" + str(GC.hiv_i3_to_i4) + "\t0\t0\t" + str(GC.hiv_i3_to_a3) + "\t0\t" + str(GC.hiv_i3_to_d) + "\n0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.hiv_i4_to_a4) + "\t" + str(GC.hiv_i4_to_d) + "\n0\t0\t" + str(GC.hiv_a1_to_i1) + "\t0\t0\t0\t0\t" + str(GC.hiv_a1_to_a2) + "\t0\t0\t" + str(GC.hiv_a1_to_d) + "\n0\t0\t0\t" + str(GC.hiv_a2_to_i2) + "\t0\t0\t0\t0\t" + str(GC.hiv_a2_to_a3) + "\t0\t" + str(GC.hiv_a2_to_d) + "\n0\t0\t0\t0\t" + str(GC.hiv_a3_to_i3) + "\t0\t0\t0\t0\t" + str(GC.hiv_a3_to_a4) + "\t" + str(GC.hiv_a3_to_d) + "\n0\t0\t0\t0\t0\t" + str(GC.hiv_a4_to_i4) + "\t0\t0\t0\t0\t" + str(GC.hiv_a4_to_d) + "\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n\n") # HIV-ART-specific
        f.write("[EDGED_TRAN_MATRIX]\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t" + str(GC.hiv_s_to_i1) + "\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n\n")
        f.write("[STATUS_BEGIN]\n0\n\n")
        f.write("[INDUCER_LIST]\n" + str(GC.gemf_state_to_num['I1']) + ' ' + str(GC.gemf_state_to_num['I2']) + ' ' + str(GC.gemf_state_to_num['I3']) + ' ' + str(GC.gemf_state_to_num['I4']) + "\n\n")
        f.write("[SIM_ROUNDS]\n1\n\n")
        f.write("[INTERVAL_NUM]\n1\n\n")
        f.write("[MAX_TIME]\n" + str(GC.end_time) + "\n\n")
        f.write("[MAX_EVENTS]\n" + str(GC.end_events) + "\n\n")
        f.write("[DIRECTED]\n1\n\n")
        f.write("[SHOW_INDUCER]\n1\n\n")
        f.write("[DATA_FILE]\nnetwork.txt\nnetwork.txt\nnetwork.txt\nnetwork.txt\n\n")
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

        # write GEMF status file (NS = 0, S = 1, I1 = 2, I2 = 3, I3 = 4, I4 = 5, A1 = 6, A2 = 7, A3 = 8, A4 = 9, D = 10)
        f = open(GC.gemf_out_dir + "/status.txt",'w')
        seeds = {seed for seed in GC.seed_nodes} # seed nodes are assumed to be in I1 and non-seeds to be in NS
        for num in sorted(num2node.keys()):
            node = num2node[num]
            if node in seeds:
                f.write(str(GC.gemf_state_to_num['I1']) + "\n") # HIV-ART-specific
            else:
                f.write(str(GC.gemf_state_to_num['NS']) + "\n") # HIV-ART-specific
        f.close()

        # run GEMF
        chdir(GC.gemf_out_dir)
        try:
            call([GC.gemf_path], stdout=open("log.txt",'w'))
        except FileNotFoundError:
            chdir(GC.START_DIR)
            assert False, "GEMF executable was not found: %s" % GC.gemf_path
        chdir(orig_dir)

        # convert GEMF output to FAVITES transmission network format
        GC.transmission_num = 0
        GC.transmission_state = set() # 'node' and 'time'
        GC.transmission_file = []
        for line in open(GC.gemf_out_dir + "/output.txt"):
            t,rate,vNum,pre,post,num0,num1,num2,num3,num4,num5,num6,num7,num8,num9,num10,lists = [i.strip() for i in line.split()]
            lists = [l.replace('[','').replace(']','').strip() for l in lists.split('],[')][1:] # ignore nodal list
            lists = [l.split(',') for l in lists if len(l) != 0]
            uNums = []
            for l in lists:
                uNums.extend(l)
            if len(uNums) != 0:
                uNum = choice(uNums) # randomly choose a single infector
                u,v = num2node[int(uNum)],num2node[int(vNum)]
                GC.transmission_file.append((u.get_name(),v.get_name(),float(t)))
        assert len(GC.transmission_file) != 0, "GEMF didn't output any transmissions"
        GC.gemf_ready = True

    def sample_time():
        if not GC.gemf_ready:
            TransmissionTimeSample_HIVARTGranichGEMF.prep_GEMF()
        return TransmissionTimeSample_TransmissionFile.sample_time()