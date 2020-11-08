#! /usr/bin/env python3
'''
Niema Moshiri 2017

"TransmissionTimeSample" module, where the transmission network is simulated by
GEMF (Sahneh et al. 2016) under an extension of the SIR model containing the
following five states: Susceptible (S), Vaccinated (V), Infected (I),
Treated (T), and Recovered (R), but where individuals can be
"seed infected" (i.e., infected from outside the contact network) after time 0.

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
from datetime import datetime
from subprocess import call
from os.path import expanduser
from os import chdir,getcwd,makedirs
from sys import stderr

class TransmissionTimeSample_SVITRGEMF(TransmissionTimeSample):
    def cite():
        return GC.CITATION_GEMF

    def init():
        assert "TransmissionNodeSample_GEMF" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_GEMF module"
        assert "EndCriteria_GEMF" in str(MF.modules['EndCriteria']), "Must use EndCriteria_GEMF module"
        GC.svitr_beta_seed = float(GC.svitr_beta_seed)
        assert GC.svitr_beta_seed >= 0, "svitr_beta_seed must be at least 0"
        GC.svitr_beta_by_i = float(GC.svitr_beta_by_i)
        assert GC.svitr_beta_by_i >= 0, "svitr_beta_by_i must be at least 0"
        GC.svitr_beta_by_t = float(GC.svitr_beta_by_t)
        assert GC.svitr_beta_by_t >= 0, "svitr_beta_by_t must be at least 0"
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
        GC.gemf_ready = False
        GC.gemf_state_to_num = {'S':0, 'I':1, 'T':2, 'R':3, 'V':3}
        GC.gemf_num_to_state = {GC.gemf_state_to_num[state]:state for state in GC.gemf_state_to_num}

    def prep_GEMF():
        # write GEMF parameter file
        orig_dir = getcwd()
        GC.gemf_path = expanduser(GC.gemf_path.strip())
        makedirs(GC.gemf_out_dir, exist_ok=True)
        f = open(GC.gemf_out_dir + "/para.txt",'w')
        f.write("[NODAL_TRAN_MATRIX]\n0\t" + str(GC.svitr_beta_seed) + "\t0\t" + str(GC.svitr_s_to_v) + "\n0\t0\t" + str(GC.svitr_i_to_t) + "\t" + str(GC.svitr_delta) + "\n0\t0\t0\t" + str(GC.svitr_t_to_r) + "\n0\t0\t0\t0\n\n") # SVITR-specific
        f.write("[EDGED_TRAN_MATRIX]\n")
        f.write("0\t" + str(GC.svitr_beta_by_i) + "\t0\t0\n0\t0\t0\t0\n0\t0\t0\t0\n0\t0\t0\t0\n\n") # SVITR-specific
        f.write("0\t" + str(GC.svitr_beta_by_t) + "\t0\t0\n0\t0\t0\t0\n0\t0\t0\t0\n0\t0\t0\t0\n\n") # SVITR-specific
        f.write("[STATUS_BEGIN]\n0\n\n")
        f.write("[INDUCER_LIST]\n" + str(GC.gemf_state_to_num['I']) + ' ' + str(GC.gemf_state_to_num['T']) + "\n\n")
        f.write("[SIM_ROUNDS]\n1\n\n")
        f.write("[INTERVAL_NUM]\n1\n\n")
        f.write("[MAX_TIME]\n" + str(GC.end_time) + "\n\n")
        f.write("[MAX_EVENTS]\n" + str(GC.C_INT_MAX) + "\n\n")
        f.write("[DIRECTED]\n" + str(int(GC.contact_network.is_directed())) + "\n\n")
        f.write("[SHOW_INDUCER]\n1\n\n")
        f.write("[DATA_FILE]\nnetwork.txt\nnetwork.txt\n\n")
        f.write("[STATUS_FILE]\nstatus.txt\n\n")
        if GC.random_number_seed is not None:
            f.write("[RANDOM_SEED]\n%d\n\n"%GC.random_number_seed)
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

        # write GEMF status file (0 = S, 1 = I, 2 = T, 3 = R)
        f = open(GC.gemf_out_dir + "/status.txt",'w')
        seeds = {seed for seed in GC.seed_nodes}
        for num in sorted(num2node.keys()):
            node = num2node[num]
            if node in seeds:
                f.write(str(GC.gemf_state_to_num['I']) + "\n") # SVITR-specific
                node.gemf_state = GC.gemf_state_to_num['I']
            else:
                f.write(str(GC.gemf_state_to_num['S']) + "\n") # SVITR-specific
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
        matrices = {GC.gemf_state_to_num['S']:outside_infection_matrix, GC.gemf_state_to_num['I']:matrices[0], GC.gemf_state_to_num['T']:matrices[1]}

        # convert GEMF output to FAVITES transmission network format
        GC.transmission_num = 0
        GC.transmission_state = set() # 'node' and 'time'
        NUM_INFECTED = len(seeds)
        GC.transmission_file = []
        for line in open(GC.gemf_out_dir + "/output.txt"):
            t,rate,vNum,pre,post,num0,num1,num2,num3,lists = [i.strip() for i in line.split()]
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
            if post == GC.gemf_state_to_num['R']:
                NUM_INFECTED -= 1
                GC.transmission_file.append((vName,vName,float(t)))
                if GC.VERBOSE:
                    print('[%s] Uninfection\tTime %s\tNode %s (%s->%s)\tTotal Infected: %d\tTotal Uninfected: %d' % (datetime.now(),t,vName,GC.gemf_num_to_state[pre],GC.gemf_num_to_state[post],NUM_INFECTED,len(num2node)-NUM_INFECTED), file=stderr)
            elif post == GC.gemf_state_to_num['I']:
                NUM_INFECTED += 1
                v = num2node[int(vNum)]
                uNodes = [num2node[num] for num in uNums]
                uRates = [matrices[uNode.gemf_state][pre][post] for uNode in uNodes]
                die = {uNodes[i]:GC.prob_exp_min(i, uRates) for i in range(len(uNodes))}
                if len(die) != 0:
                    u = GC.roll(die) # roll die weighted by exponential infectious rates
                    uName = u.get_name()
                    if GC.VERBOSE:
                        print('[%s] Infection\tTime %s\tFrom Node %s (%s)\tTo Node %s (%s->%s)\tTotal Infected: %d\tTotal Uninfected: %d' % (datetime.now(),t,uName,GC.gemf_num_to_state[u.gemf_state],vName,GC.gemf_num_to_state[pre],GC.gemf_num_to_state[post],NUM_INFECTED,len(num2node)-NUM_INFECTED), file=stderr)
                elif len(die) == 0 or u == v: # new seed
                    uName = None
                    if GC.VERBOSE:
                        print('[%s] Seed\tTime %s\tNode %s\tTotal Infected: %d\tTotal Uninfected: %d' % (datetime.now(),t,vName,NUM_INFECTED,len(num2node)-NUM_INFECTED), file=stderr)
                GC.transmission_file.append((uName,v.get_name(),float(t)))
            elif GC.VERBOSE:
                print('[%s] Transition\tTime %s\tNode %s (%s->%s)' % (datetime.now(),t,vName,GC.gemf_num_to_state[pre],GC.gemf_num_to_state[post]), file=stderr)
            num2node[int(vNum)].gemf_state = post
        assert len(GC.transmission_file) != 0, "GEMF didn't output any transmissions"
        GC.gemf_ready = True
        GC.granich_num2node = num2node # for TimeSample_GranichFirstArt to access

    def sample_time():
        if not GC.gemf_ready:
            TransmissionTimeSample_SVITRGEMF.prep_GEMF()
        return TransmissionTimeSample_TransmissionFile.sample_time()
