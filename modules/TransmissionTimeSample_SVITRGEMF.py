#! /usr/bin/env python3
'''
Niema Moshiri 2017

"TransmissionTimeSample" module, where the transmission network is simulated by
GEMF (Sahneh et al. 2016) under an extension of the SIR model containing the
following five states: Susceptible (S), Vaccinated (V), Infected (I),
Treated (T), and Recovered (R).

Susceptible individuals can be vaccinated (S -> V), and vaccinated individuals
remain in the (V) state. Susceptible individuals can also become infected
(S -> I). Infected individuals can either be treated (I -> T) and later recover
(T -> R), or they can go directly into recovery without treatment (I -> R).

For the sake of computational efficiency, we merge the (V) and (R) states.
'''
from TransmissionTimeSample import TransmissionTimeSample
from TransmissionTimeSample_TransmissionFile import TransmissionTimeSample_TransmissionFile
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from subprocess import call
from os.path import expanduser
from os import chdir,getcwd,makedirs
from random import choice

class TransmissionTimeSample_SVITRGEMF(TransmissionTimeSample):
    def init():
        assert "TransmissionNodeSample_GEMF" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_GEMF module"
        assert "EndCriteria_GEMF" in str(MF.modules['EndCriteria']), "Must use EndCriteria_GEMF module"
        GC.svitr_beta = float(GC.svitr_beta)
        assert GC.svitr_beta >= 0, "svitr_beta must be at least 0"
        GC.svitr_delta = float(GC.svitr_delta)
        assert GC.svitr_delta >= 0, "svitr_delta must be at least 0"
        GC.svitr_s_to_v = float(GC.svitr_s_to_v)
        assert GC.svitr_s_to_v >= 0, "svitr_s_to_v must be at least 0"
        GC.svitr_i_to_t = float(GC.svitr_i_to_t)
        assert GC.svitr_i_to_t >= 0, "svitr_i_to_t must be at least 0"
        GC.svitr_t_to_r = float(GC.svitr_t_to_r)
        assert GC.svitr_t_to_r >= 0, "svitr_t_to_r must be at least 0"
        GC.end_time = float(GC.end_time)
        assert GC.end_time > 0, "end_time must be positive"
        GC.end_events = int(GC.end_events)
        assert GC.end_events > 0, "end_events must be positive"
        GC.gemf_ready = False

    def prep_GEMF():
        # write GEMF parameter file
        GC.gemf_path = expanduser(GC.gemf_path.strip())
        makedirs("GEMF_output")
        f = open("GEMF_output/para.txt",'w')
        f.write("[NODAL_TRAN_MATRIX]\n0\t0\t0\t" + str(GC.svitr_s_to_v) + "\n0\t0\t" + str(GC.svitr_i_to_t) + "\t" + str(GC.svitr_delta) + "\n0\t0\t0\t" + str(GC.svitr_t_to_r) + "\n0\t0\t0\t0\n\n") # SVITR-specific
        f.write("[EDGED_TRAN_MATRIX]\n0\t" + str(GC.svitr_beta) + "\t0\t0\n0\t0\t0\t0\n0\t0\t0\t0\n0\t0\t0\t0\n\n") # SVITR-specific
        f.write("[STATUS_BEGIN]\n0\n\n")
        f.write("[INDUCER_LIST]\n1\n\n")
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

        # write GEMF to original mapping
        f = open("GEMF_output/gemf2orig.json",'w')
        f.write(str({num:num2node[num].get_name() for num in num2node}))
        f.close()

        # write GEMF status file (0 = S, 1 = I, 2 = T, 3 = R)
        f = open("GEMF_output/status.txt",'w')
        seeds = {seed for seed in GC.seed_nodes}
        for num in sorted(num2node.keys()):
            node = num2node[num]
            if node in seeds:
                f.write("1\n") # SVITR-specific
            else:
                f.write("0\n") # SVITR-specific
        f.close()

        # run GEMF
        orig_dir = getcwd()
        chdir("GEMF_output")
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
        for line in open("GEMF_output/output.txt"):
            t,rate,vNum,pre,post,num0,num1,num2,num3,lists = [i.strip() for i in line.split()]
            uNums = [u for u in lists.split('],[')[1][:-1].split(',') if u != '']
            if len(uNums) != 0:
                uNum = choice(uNums) # randomly choose a single infector
                u,v = num2node[int(uNum)],num2node[int(vNum)]
                GC.transmission_file.append((u.get_name(),v.get_name(),float(t)))
        assert len(GC.transmission_file) != 0, "GEMF didn't output any transmissions"
        GC.gemf_ready = True

    def sample_time():
        if not GC.gemf_ready:
            TransmissionTimeSample_SVITRGEMF.prep_GEMF()
        return TransmissionTimeSample_TransmissionFile.sample_time()