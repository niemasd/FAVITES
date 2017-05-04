#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionTimeSample" module, where the transmission network is simulated by
GEMF (Sahneh et al. 2016) under the SAIS model.
'''
from TransmissionTimeSample import TransmissionTimeSample
from TransmissionTimeSample_TransmissionFile import TransmissionTimeSample_TransmissionFile
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from subprocess import call
from os.path import expanduser
from os import chdir,getcwd,makedirs
from random import choice

class TransmissionTimeSample_SAISGEMF(TransmissionTimeSample):
    def init():
        assert "TransmissionNodeSample_GEMF" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_GEMF module"
        assert "EndCriteria_GEMF" in str(MF.modules['EndCriteria']), "Must use EndCriteria_GEMF module"
        GC.sais_beta = float(GC.sais_beta)
        assert GC.sais_beta >= 0, "sais_beta must be at least 0"
        GC.sais_kappa = float(GC.sais_kappa)
        assert GC.sais_kappa >= 0, "sais_kappa must be at least 0"
        GC.sais_delta = float(GC.sais_delta)
        assert GC.sais_delta >= 0, "sais_delta must be at least 0"
        GC.sais_beta_a = float(GC.sais_beta_a)
        assert GC.sais_beta_a >= 0, "sais_beta_a must be at least 0"
        GC.end_time = float(GC.end_time)
        assert GC.end_time > 0, "end_time must be positive"
        GC.end_events = int(GC.end_events)
        assert GC.end_events > 0, "end_events must be positive"
        GC.gemf_ready = False
        GC.gemf_state_to_num = {'S':0, 'A':1, 'I':2}
        GC.gemf_num_to_state = {GC.gemf_state_to_num[state]:state for state in GC.gemf_state_to_num}

    def prep_GEMF():
        # write GEMF parameter file
        orig_dir = getcwd()
        GC.gemf_path = expanduser(GC.gemf_path.strip())
        makedirs(GC.gemf_out_dir)
        f = open(GC.gemf_out_dir + "/para.txt",'w')
        f.write("[NODAL_TRAN_MATRIX]\n0\t0\t0\n0\t0\t0\n" + str(GC.sais_delta) + "\t0\t0\n\n") # SAIS-specific
        f.write("[EDGED_TRAN_MATRIX]\n0\t" + str(GC.sais_kappa) + "\t" + str(GC.sais_beta) + "\n0\t0\t" + str(GC.sais_beta_a) + "\n0\t0\t0\n\n") # SAIS-specific
        f.write("[STATUS_BEGIN]\n0\n\n")
        f.write("[INDUCER_LIST]\n" + str(GC.gemf_state_to_num['I']) + "\n\n")
        f.write("[SIM_ROUNDS]\n1\n\n")
        f.write("[INTERVAL_NUM]\n1\n\n")
        f.write("[MAX_TIME]\n" + str(GC.end_time) + "\n\n")
        f.write("[MAX_EVENTS]\n" + str(GC.end_events) + "\n\n")
        f.write("[DIRECTED]\n1\n\n")
        f.write("[SHOW_INDUCER]\n1\n\n")
        f.write("[DATA_FILE]\nnetwork.txt\n\n")
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

        # write GEMF status file (0 = S, 1 = A, 2 = I)
        f = open("GEMF_output/status.txt",'w')
        seeds = {seed for seed in GC.seed_nodes}
        for num in sorted(num2node.keys()):
            node = num2node[num]
            if node in seeds:
                f.write(str(GC.gemf_state_to_num['I']) + "\n") # SAIS-specific
            else:
                f.write(str(GC.gemf_state_to_num['S']) + "\n") # SAIS-specific
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
            t,rate,vNum,pre,post,num0,num1,num2,lists = [i.strip() for i in line.split()]
            uNums = [u for u in lists.split('],[')[1][:-1].split(',') if u != '']
            if post == str(GC.gemf_state_to_num['S']):
                vName = num2node[int(vNum)].get_name()
                GC.transmission_file.append((vName,vName,float(t)))
            elif len(uNums) != 0:
                uNum = choice(uNums) # randomly choose a single infector
                u,v = num2node[int(uNum)],num2node[int(vNum)]
                GC.transmission_file.append((u.get_name(),v.get_name(),float(t)))
        assert len(GC.transmission_file) != 0, "GEMF didn't output any transmissions"
        GC.gemf_ready = True

    def sample_time():
        if not GC.gemf_ready:
            TransmissionTimeSample_SAISGEMF.prep_GEMF()
        return TransmissionTimeSample_TransmissionFile.sample_time()