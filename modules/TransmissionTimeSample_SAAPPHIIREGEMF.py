#! /usr/bin/env python3
'''
Niema Moshiri 2020

"TransmissionTimeSample" module, where the transmission network is simulated by
GEMF (Sahneh et al. 2016) under the SAAPPHIIRE model, which is an extension of
the SAPHIRE model (Hao et al., 2020) containing the following 10 states:
Susceptible (S), Exposed (E), Presymptomatic 1 (P1), Presymptomatic 2 (P2),
Ascertained Infectious 1 (I1), Ascertained Infectious 2 (I2), Unascertained
Infectious 1 (A1), Unascertained Infectious 2 (A2), Hospitalized (H), and
Recovered (R). Individuals can be "seed infected" (i.e., infected from outside
the contact network) after time 0.

Susceptible individuals can be exposed to the virus by infection (S -> E).
Exposed individuals become early presymptomatic (E -> P1), and later, they
transition to late presymptomatic (P1 -> P2). Late presymptomatic individuals
become either early ascertained (P2 -> I1) or early unascertained (P2 -> A1).
After some time, early ascertained or unascertained transition to late
ascertained or unascertained (I1 -> I2 and A1 -> A2). Early and late ascertained
individuals can become hospitalized (I1 -> H and I2 -> H), and late ascertained
and unascertained individuals as well as hospitalized individuals can recover
(I2 -> R, A2 -> R, and H -> R).
'''
from TransmissionTimeSample import TransmissionTimeSample
from TransmissionTimeSample_TransmissionFile import TransmissionTimeSample_TransmissionFile
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from datetime import datetime
from os.path import expanduser
from os import chdir,getcwd,makedirs
from random import shuffle
from subprocess import call
from sys import stderr

class TransmissionTimeSample_SAAPPHIIREGEMF(TransmissionTimeSample):
    def cite():
        return GC.CITATION_GEMF

    def init():
        assert "TransmissionNodeSample_GEMF" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_GEMF module"
        assert "EndCriteria_GEMF" in str(MF.modules['EndCriteria']), "Must use EndCriteria_GEMF module"
        for p in dir(GC):
            if p.startswith('saapphiire_') and '_to_' in p:
                setattr(GC, p, float(getattr(GC,p)))
                assert getattr(GC,p) >= 0, "%s must be at least 0" % p
        GC.end_time = float(GC.end_time)
        assert GC.end_time > 0, "end_time must be positive"
        GC.gemf_ready = False
        GC.gemf_state_to_num = {'S':0, 'E':1, 'P1':2, 'P2':3, 'I1':4, 'I2':5, 'A1':6, 'A2':7, 'H':8, 'R':9}
        GC.gemf_num_to_state = {GC.gemf_state_to_num[state]:state for state in GC.gemf_state_to_num}
        freq_sum = 0
        for s in GC.gemf_state_to_num.keys():
            p = "saapphiire_freq_%s"%s.lower(); f = getattr(GC,p)
            if f > 1:
                f = int(f)
            else:
                f = float(f)
            assert f >= 0, "%s must be at least 0" % p
            setattr(GC,p,f)
            freq_sum += f
        assert freq_sum > 1 or abs(freq_sum-1) < 0.000001, "Sum of saapphiire_freq_* parameters must equal 1"

    def prep_GEMF():
        # write GEMF parameter file
        orig_dir = getcwd()
        GC.gemf_path = expanduser(GC.gemf_path.strip())
        makedirs(GC.gemf_out_dir, exist_ok=True)
        f = open(GC.gemf_out_dir + "/para.txt",'w')
        f.write("[NODAL_TRAN_MATRIX]\n")
        f.write("0\t" + str(GC.saapphiire_s_to_e_seed) + "\t0\t0\t0\t0\t0\t0\t0\t0\n")                                # S  can go to E (nodal would mean seed infection)
        f.write("0\t0\t" + str(GC.saapphiire_e_to_p1) + "\t0\t0\t0\t0\t0\t0\t0\n")                                    # E  can go to P1
        f.write("0\t0\t0\t" + str(GC.saapphiire_p1_to_p2) + "\t0\t0\t0\t0\t0\t0\n")                                   # P1 can go to P2
        f.write("0\t0\t0\t0\t" + str(GC.saapphiire_p2_to_i1) + "\t0\t" + str(GC.saapphiire_p2_to_a1) + "\t0\t0\t0\n") # P2 can go to I1 or A1
        f.write("0\t0\t0\t0\t0\t" + str(GC.saapphiire_i1_to_i2) + "\t0\t0\t" + str(GC.saapphiire_i1_to_h) + "\t0\n")  # I1 can go to I2 or H
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.saapphiire_i2_to_h) + "\t" + str(GC.saapphiire_i2_to_r) + "\n")   # I2 can go to H  or R
        f.write("0\t0\t0\t0\t0\t0\t0\t" + str(GC.saapphiire_a1_to_a2) + "\t0\t0\n")                                   # A1 can go to A2
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.saapphiire_a2_to_r) + "\n")                                    # A2 can go to R
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t" + str(GC.saapphiire_h_to_r) + "\n")                                     # H  can go to R
        f.write("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n")                                                                     # R  can't go anywhere
        f.write("\n[EDGED_TRAN_MATRIX]\n")
        f.write("0\t" + str(GC.saapphiire_s_to_e_by_e)  + "\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n\n")
        f.write("0\t" + str(GC.saapphiire_s_to_e_by_p1) + "\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n\n")
        f.write("0\t" + str(GC.saapphiire_s_to_e_by_p2) + "\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n\n")
        f.write("0\t" + str(GC.saapphiire_s_to_e_by_i1) + "\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n\n")
        f.write("0\t" + str(GC.saapphiire_s_to_e_by_i2) + "\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n\n")
        f.write("0\t" + str(GC.saapphiire_s_to_e_by_a1) + "\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n\n")
        f.write("0\t" + str(GC.saapphiire_s_to_e_by_a2) + "\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\t0\t0\n\n")
        f.write("[STATUS_BEGIN]\n0\n\n")
        infectious = ['E', 'P1','P2','I1','I2','A1','A2']
        f.write("[INDUCER_LIST]\n" + ' '.join([str(GC.gemf_state_to_num[i]) for i in infectious]) + "\n\n")
        f.write("[SIM_ROUNDS]\n1\n\n")
        f.write("[INTERVAL_NUM]\n1\n\n")
        f.write("[MAX_TIME]\n" + str(GC.end_time) + "\n\n")
        f.write("[MAX_EVENTS]\n" + str(GC.C_INT_MAX) + "\n\n")
        f.write("[DIRECTED]\n1\n\n")
        f.write("[SHOW_INDUCER]\n1\n\n")
        f.write("[DATA_FILE]\n" + '\n'.join(["network.txt"]*len(infectious)) + "\n\n")
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

        # write GEMF status file (see gemf_state_to_num for mapping)
        leftover = len(num2node)
        start_states = {'seed':[], 'other':[]}
        for s in infectious:
            k = "saapphiire_freq_%s"%s.lower()
            if isinstance(getattr(GC,k), float):
                n = int(len(num2node)*getattr(GC,k))
            else:
                n = getattr(GC,k)
            start_states['seed'] += [GC.gemf_state_to_num[s]]*n
            leftover -= n
        assert len(start_states['seed']) == len(GC.seed_nodes), "At time 0, E+P1+P2+I1+I2+A1+A2 = %d, but there are %d seed nodes. Fix saapphiire_freq_* parameters accordingly" % (len(start_states['seed']),len(GC.seed_nodes))
        for s in ['S']:
            k = "saapphiire_freq_%s"%s.lower()
            if isinstance(getattr(GC,k), float):
                n = int(len(num2node)*getattr(GC,k))
            else:
                n = getattr(GC,k)
            start_states['other'] += [GC.gemf_state_to_num[s]]*n
            leftover -= n
        start_states['other'] += [GC.gemf_state_to_num['R']]*leftover
        shuffle(start_states['seed']); shuffle(start_states['other'])
        f = open(GC.gemf_out_dir + "/status.txt",'w')
        seeds = {seed for seed in GC.seed_nodes} # seed nodes are assumed to be in P1 and non-seeds to be in S
        for num in sorted(num2node.keys()):
            node = num2node[num]
            if node in seeds:
                s = start_states['seed'].pop()
                f.write("%d\n"%s)
                node.gemf_state = s
            else:
                s = start_states['other'].pop()
                f.write("%d\n"%s)
                node.gemf_state = s
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
        matrices = {GC.gemf_state_to_num[infectious[i]]:matrices[i] for i in range(len(infectious))}
        matrices[GC.gemf_state_to_num['S']] = outside_infection_matrix

        # convert GEMF output to FAVITES transmission network format
        GC.transmission_num = 0
        GC.transmission_state = set() # 'node' and 'time'
        NUM_INFECTED = len(seeds)
        GC.transmission_file = []
        for line in open(GC.gemf_out_dir + "/output.txt"):
            t,rate,vNum,pre,post,num0,num1,num2,num3,num4,num5,num6,num7,num8,num9,lists = [i.strip() for i in line.split()]
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
            elif GC.gemf_num_to_state[pre] == 'S' and GC.gemf_num_to_state[post] == 'E':
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
        GC.gemf_num2node = num2node

    def sample_time():
        if not GC.gemf_ready:
            TransmissionTimeSample_SAAPPHIIREGEMF.prep_GEMF()
        return TransmissionTimeSample_TransmissionFile.sample_time()
