#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionTimeSample" module, where the transmission network is simulated by
GEMF (Sahneh et al. 2016) under the SIS model, but where individuals can be
"seed infected" (i.e., infected from outside the contact network) after time 0.
'''
from TransmissionTimeSample import TransmissionTimeSample
from TransmissionTimeSample_TransmissionFile import TransmissionTimeSample_TransmissionFile
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from datetime import datetime
from subprocess import call
from os.path import expanduser
from os import chdir,getcwd,makedirs
from sys import stderr

class TransmissionTimeSample_SISGEMF(TransmissionTimeSample):
    def init():
        assert "TransmissionNodeSample_GEMF" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_GEMF module"
        assert "EndCriteria_GEMF" in str(MF.modules['EndCriteria']), "Must use EndCriteria_GEMF module"
        GC.sis_beta_seed = float(GC.sis_beta_seed)
        assert GC.sis_beta_seed >= 0, "sis_beta_seed must be at least 0"
        GC.sis_beta_by_i = float(GC.sis_beta_by_i)
        assert GC.sis_beta_by_i >= 0, "sis_beta_by_i must be at least 0"
        GC.sis_delta = float(GC.sis_delta)
        assert GC.sis_delta >= 0, "sis_delta must be at least 0"
        GC.end_time = float(GC.end_time)
        assert GC.end_time > 0, "end_time must be positive"
        GC.gemf_ready = False
        GC.gemf_state_to_num = {'S':0, 'I':1}
        GC.gemf_num_to_state = {GC.gemf_state_to_num[state]:state for state in GC.gemf_state_to_num}

    def prep_GEMF():
        # write GEMF parameter file
        orig_dir = getcwd()
        GC.gemf_path = expanduser(GC.gemf_path.strip())
        makedirs(GC.gemf_out_dir)
        f = open(GC.gemf_out_dir + "/para.txt",'w')
        f.write("[NODAL_TRAN_MATRIX]\n0\t" + str(GC.sis_beta_seed) + "\n" + str(GC.sis_delta) + "\t0\n\n") # SIS-specific
        f.write("[EDGED_TRAN_MATRIX]\n0\t" + str(GC.sis_beta_by_i) + "\n0\t0\n\n")  # SIS-specific
        f.write("[STATUS_BEGIN]\n0\n\n")
        f.write("[INDUCER_LIST]\n" + str(GC.gemf_state_to_num['I']) + "\n\n")
        f.write("[SIM_ROUNDS]\n1\n\n")
        f.write("[INTERVAL_NUM]\n1\n\n")
        f.write("[MAX_TIME]\n" + str(GC.end_time) + "\n\n")
        f.write("[MAX_EVENTS]\n" + str(GC.C_INT_MAX) + "\n\n")
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

        # write GEMF status file (0 = S, 1 = I)
        f = open(GC.gemf_out_dir + "/status.txt",'w')
        seeds = {seed for seed in GC.seed_nodes}
        for num in sorted(num2node.keys()):
            node = num2node[num]
            if node in seeds:
                f.write(str(GC.gemf_state_to_num['I']) + "\n") # SIS-specific
                node.gemf_state = GC.gemf_state_to_num['I']
            else:
                f.write(str(GC.gemf_state_to_num['S']) + "\n") # SIS-specific
                node.gemf_state = GC.gemf_state_to_num['S']
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
        outside_infection_matrix = [[float(e) for e in l.split()] for l in matrices[matrices.index('[NODAL_TRAN_MATRIX]'):matrices.index('\n\n[EDGED_TRAN_MATRIX]')].replace('[NODAL_TRAN_MATRIX]\n','').splitlines()]
        matrices = [[[float(e) for e in l.split()] for l in m.splitlines()] for m in matrices[matrices.index('[EDGED_TRAN_MATRIX]'):matrices.index('\n\n[STATUS_BEGIN]')].replace('[EDGED_TRAN_MATRIX]\n','').split('\n\n')]
        infectious = ['I']
        matrices = {GC.gemf_state_to_num['S']:outside_infection_matrix, GC.gemf_state_to_num['I']:matrices[0]}

        # convert GEMF output to FAVITES transmission network format
        NUM_INFECTED = len(seeds)
        GC.transmission_file = []
        for line in open(GC.gemf_out_dir + "/output.txt"):
            t,rate,vNum,pre,post,num0,num1,lists = [i.strip() for i in line.split()]
            pre,post = int(pre),int(post)
            vName = num2node[int(vNum)].get_name()
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
            if post == GC.gemf_state_to_num['S']:
                NUM_INFECTED -= 1
                GC.transmission_file.append((vName,vName,float(t)))
                if GC.VERBOSE:
                    print('[%s] Uninfection\tTime %s\tNode %s (%s->%s)\tTotal Infected: %d\tTotal Uninfected: %d' % (datetime.now(),t,vName,GC.gemf_num_to_state[pre],GC.gemf_num_to_state[post],NUM_INFECTED,len(num2node)-NUM_INFECTED), file=stderr)
            else:
                NUM_INFECTED += 1
                uNodes = [num2node[num] for num in uNums]
                uRates = [matrices[uNode.gemf_state][pre][post] for uNode in uNodes]
                die = {uNodes[i]:GC.prob_exp_min(i, uRates) for i in range(len(uNodes))}
                u = GC.roll(die) # roll die weighted by exponential infectious rates
                v = num2node[int(vNum)]
                if u == v: # new seed
                    uName = None
                    if GC.VERBOSE:
                        print('[%s] Seed\tTime %s\tNode %s\tTotal Infected: %d\tTotal Uninfected: %d' % (datetime.now(),t,vName,NUM_INFECTED,len(num2node)-NUM_INFECTED), file=stderr)
                else:
                    uName = u.get_name()
                    if GC.VERBOSE:
                        print('[%s] Infection\tTime %s\tFrom Node %s (%s)\tTo Node %s (%s->%s)\tTotal Infected: %d\tTotal Uninfected: %d' % (datetime.now(),t,uName,GC.gemf_num_to_state[u.gemf_state],vName,GC.gemf_num_to_state[pre],GC.gemf_num_to_state[post],NUM_INFECTED,len(num2node)-NUM_INFECTED), file=stderr)
                GC.transmission_file.append((uName,v.get_name(),float(t)))
            num2node[int(vNum)].gemf_state = post
        assert len(GC.transmission_file) != 0, "GEMF didn't output any transmissions"
        GC.gemf_ready = True

    def sample_time():
        if not GC.gemf_ready:
            TransmissionTimeSample_SISGEMF.prep_GEMF()
        return TransmissionTimeSample_TransmissionFile.sample_time()