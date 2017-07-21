#! /usr/bin/env python3
'''
Niema Moshiri 2016

"NodeEvolution" module, implemented using a coalescent model in which
within-host phylogenies have increasing effective population sizes using under
the specified growth model. More information can be found here:

https://github.com/olli0601/PANGEA.HIV.sim#dated-viral-phylogenies

VirusTreeSimulator written by Matthew Hall (whgu0705@nexus.ox.ac.uk)
'''
from NodeEvolution import NodeEvolution
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from os import chdir,getcwd,makedirs
from os.path import expanduser
from subprocess import call
from glob import glob

VTS_OUTPUT_DIR = "VirusTreeSimulator_output"
VTS_TRANSMISSIONS = "transmissions.csv"
VTS_SAMPLES = "sample.csv"
VTS_OUTPUT_PREFIX = ""

class NodeEvolution_VirusTreeSimulator(NodeEvolution):
    def cite():
        return GC.CITATION_PANGEA

    def init():
        GC.java_path = expanduser(GC.java_path.strip())
        GC.vts_model = GC.vts_model.strip().lower()
        assert GC.vts_model in {"constant", "exponential", "logistic"}, 'vts_model must be either "constant", "exponential", or "logistic"'
        GC.vts_n0 = int(GC.vts_n0)
        assert GC.vts_n0 >= 1, "vts_n0 must be a positive integer"
        GC.vts_growthRate = float(GC.vts_growthRate)
        assert GC.vts_growthRate >= 0, "vts_growthRate cannot be negative"
        GC.vts_t50 = float(GC.vts_t50)

    def evolve_to_current_time(node, finalize=False):
        # if it's not the end yet, just dummy
        if not finalize:
            for virus in node.viruses():
                virus.set_time(GC.time)
        elif not hasattr(GC,'sampled_trees'):
            # create directory for VirusTreeSimulator output
            orig_dir = getcwd()
            makedirs(VTS_OUTPUT_DIR, exist_ok=True)
            chdir(VTS_OUTPUT_DIR)

            # create VirusTreeSimulator input files
            nodes = set()
            f = open(VTS_TRANSMISSIONS,'w')
            f.write("IDREC,IDTR,TIME_TR\n")
            for u,v,t in GC.transmissions:
                if u is None:
                    u = 'NA'
                f.write("%s,%s,%f\n" % (v,u,t))
                nodes.add(u)
                nodes.add(v)
            f.close()
            f = open(VTS_SAMPLES,'w')
            f.write("IDPOP,TIME_SEQ,SEQ_COUNT\n")
            for node in nodes:
                if node in GC.cn_sample_times:
                    for t in sorted(GC.cn_sample_times[node]):
                        f.write("%s,%f,%d\n" % (node,t,MF.modules['NumBranchSample'].sample_num_branches(node,t)))
            f.close()

            # run VirusTreeSimulator
            jar_file = GC.FAVITES_DIR + '/dependencies/VirusTreeSimulator.jar'
            try:
                call([GC.java_path,'-jar',jar_file,'-demoModel',GC.vts_model,'-N0',str(GC.vts_n0),'-growthRate',str(GC.vts_growthRate),'-t50',str(GC.vts_t50),VTS_TRANSMISSIONS,VTS_SAMPLES,VTS_OUTPUT_PREFIX], stdout=open("log.txt",'w'))
            except FileNotFoundError:
                chdir(GC.START_DIR)
                assert False, "Java executable was not found: %s" % GC.java_path

            # parse VirusTreeSimulator output
            GC.sampled_trees = set()
            num_tree_nodes = 0
            for filename in glob('*_simple.nex'):
                parts = open(filename).read().strip().split('Translate')[1].split('tree TREE1')
                translate = [l.strip().replace(',','').replace("'",'').split() for l in parts[0].splitlines()][1:-1]
                tree = parts[1].split('] = [&R] ')[1].splitlines()[0].strip()
                wiped = set()
                new_viruses = set()
                for a,b in translate: # ID must be before : and must be after either ( or ,
                    num_tree_nodes += 1
                    bParts = b.strip().split('_')
                    bTime = float(bParts[-1])
                    b_cn_node_label = '_'.join(bParts[1:-3])
                    b_cn_node = GC.contact_network.get_node(b_cn_node_label)
                    if b_cn_node not in wiped:
                        b_cn_node.uninfect()
                        wiped.add(b_cn_node)
                    new_virus = MF.modules['TreeNode'](time=bTime,contact_network_node=b_cn_node)
                    b_cn_node.infect(bTime,new_virus)
                    bFix = 'N' + str(num_tree_nodes) + '|' + b_cn_node_label + '|' + bParts[-1]
                    tree = tree.replace('(' + a.strip() + ':', '(' + bFix + ':')
                    tree = tree.replace(',' + a.strip() + ':', ',' + bFix + ':')
                virus = GC.seed_to_first_virus[GC.contact_network.get_node('_'.join(filename.split('_')[1:-1]))]
                virus.set_newick(tree)
                GC.sampled_trees.add(virus)
            chdir(orig_dir)
