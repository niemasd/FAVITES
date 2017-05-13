#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionTimeSample" module, where the transmission network is simulated by
GEMF (Sahneh et al. 2016) under the gonorrhea model used by Hethcote & Yorke
(1984).

The states of the model are as follows:
- MA  = Male Abstinent
- MS  = Male Susceptible
- MIS = Male Infected Symptomatic
- MIA = Male Infected Asymptomatic
- FA  = Female Abstinent
- FS  = Female Susceptible
- FIS = Female Infected Symptomatic
- FIA = Female Infected Asymptomatic

Below is an adjacency list representing the model:
- MA  -> [MS]
- MS  -> [MA, MIS, MIA]
- MIS -> [MA, MS]
- MIA -> [MA, MS]
- FA  -> [FS]
- FS  -> [FA, FIS, FIA]
- FIS -> [FA, FS]
- FIA -> [FA, FS]
'''
from TransmissionTimeSample import TransmissionTimeSample
from TransmissionTimeSample_TransmissionFile import TransmissionTimeSample_TransmissionFile
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from subprocess import call
from os.path import expanduser
from os import chdir,getcwd,makedirs
from random import choice

class TransmissionTimeSample_GonorrheaHethcoteYorkeGEMF(TransmissionTimeSample):
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
        GC.gemf_state_to_num = {'MA':0, 'MS':1, 'MIS':2, 'MIA':3, 'FA':4, 'FS':5, 'FIS':6, 'FIA':7}
        GC.gemf_num_to_state = {GC.gemf_state_to_num[state]:state for state in GC.gemf_state_to_num}

    def prep_GEMF():
        # check for gender attribute in contact network nodes
        for node in GC.contact_network.nodes_iter():
            attr = node.get_attribute()
            assert 'MALE' in attr or 'FEMALE' in attr, "All nodes must have MALE or FEMALE in their attributes"
            assert not ('MALE' in attr and 'FEMALE' in attr), "Nodes cannot be both MALE and FEMALE"

        # write GEMF parameter file
        orig_dir = getcwd()
        GC.gemf_path = expanduser(GC.gemf_path.strip())
        makedirs(GC.gemf_out_dir)
        f = open(GC.gemf_out_dir + "/para.txt",'w')
        f.write("[NODAL_TRAN_MATRIX]\n0\t" + str(GC.gon_ma_to_ms) + "\t0\t0\t0\t0\t0\t0\n" + str(GC.gon_ms_to_ma) + "\t0\t0\t0\t0\t0\t0\t0\n" + str(GC.gon_mis_to_ma) + "\t" + str(GC.gon_mis_to_ms) + "\t0\t0\t0\t0\t0\t0\n" + str(GC.gon_mia_to_ma) + "\t" + str(GC.gon_mia_to_ms) + "\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t" + str(GC.gon_fa_to_fs) + "\t0\t0\n0\t0\t0\t0\t" + str(GC.gon_fs_to_fa) + "\t0\t0\t0\n0\t0\t0\t0\t" + str(GC.gon_fis_to_fa) + "\t" + str(GC.gon_fis_to_fs) + "\t0\t0\n0\t0\t0\t0\t" + str(GC.gon_fia_to_fa) + "\t" + str(GC.gon_fia_to_fs) + "\t0\t0\n\n") # Gonorrhea-specific
        f.write("[EDGED_TRAN_MATRIX]\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t" + str(GC.gon_ms_to_mis_by_mis) + "\t" + str(GC.gon_ms_to_mia_by_mis) + "\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t" + str(GC.gon_fs_to_fis_by_mis) + "\t" + str(GC.gon_fs_to_fia_by_mis) + "\n0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\n\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t" + str(GC.gon_ms_to_mis_by_mia) + "\t" + str(GC.gon_ms_to_mia_by_mia) + "\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t" + str(GC.gon_fs_to_fis_by_mia) + "\t" + str(GC.gon_fs_to_fia_by_mia) + "\n0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\n\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t" + str(GC.gon_ms_to_mis_by_fis) + "\t" + str(GC.gon_ms_to_mia_by_fis) + "\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t" + str(GC.gon_fs_to_fis_by_fis) + "\t" + str(GC.gon_fs_to_fia_by_fis) + "\n0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\n\n")
        f.write("0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t" + str(GC.gon_ms_to_mis_by_fia) + "\t" + str(GC.gon_ms_to_mia_by_fia) + "\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t" + str(GC.gon_fs_to_fis_by_fia) + "\t" + str(GC.gon_fs_to_fia_by_fia) + "\n0\t0\t0\t0\t0\t0\t0\t0\n0\t0\t0\t0\t0\t0\t0\t0\n\n")
        f.write("[STATUS_BEGIN]\n0\n\n")
        infectious = ['MIS','MIA','FIS','FIA']
        f.write("[INDUCER_LIST]\n" + ' '.join([str(GC.gemf_state_to_num[e]) for e in infectious]) + "\n\n")
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

        # write GEMF status file (MA = 0, MS = 1, MIS = 2, MIA = 3, FA = 4, FS = 5, FIS = 6, FIA = 7)
        f = open(GC.gemf_out_dir + "/status.txt",'w')
        seeds = {seed for seed in GC.seed_nodes} # seed nodes are assumed to be asymptomatic
        for num in sorted(num2node.keys()):
            node = num2node[num]
            attr = node.get_attribute()
            if node in seeds:
                if 'MALE' in attr:
                    f.write(str(GC.gemf_state_to_num['MIA']) + "\n") # Gonorrhea-specific
                    node.gemf_state = GC.gemf_state_to_num['MIA']
                else:
                    f.write(str(GC.gemf_state_to_num['FIA']) + "\n") # Gonorrhea-specific
                    node.gemf_state = GC.gemf_state_to_num['FIA']
            else:
                if 'MALE' in attr:
                    f.write(str(GC.gemf_state_to_num['MS']) + "\n") # Gonorrhea-specific
                    node.gemf_state = GC.gemf_state_to_num['MS']
                else:
                    f.write(str(GC.gemf_state_to_num['FS']) + "\n") # Gonorrhea-specific
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
            t,rate,vNum,pre,post,num0,num1,num2,num3,num4,num5,num6,num7,lists = [i.strip() for i in line.split()]
            pre,post = int(pre),int(post)
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
            if post in {GC.gemf_state_to_num[i] for i in ['MA','MS','FA','FS']}:
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
            TransmissionTimeSample_GonorrheaHethcoteYorkeGEMF.prep_GEMF()
        return TransmissionTimeSample_TransmissionFile.sample_time()