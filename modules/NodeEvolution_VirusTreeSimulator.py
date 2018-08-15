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
from gzip import open as gopen
from os import chdir,getcwd,makedirs,remove
from os.path import expanduser
from subprocess import Popen,STDOUT
from glob import glob
from shutil import rmtree
from tempfile import NamedTemporaryFile

VTS_OUTPUT_DIR = "VirusTreeSimulator_output"
#VTS_TRANSMISSIONS = "transmissions.csv"
#VTS_SAMPLES = "sample.csv"
VTS_OUTPUT_PREFIX = ""

class NodeEvolution_VirusTreeSimulator(NodeEvolution):
    def cite():
        return [GC.CITATION_PANGEA, GC.CITATION_TREESWIFT]

    def init():
        GC.java_path = expanduser(GC.java_path.strip())
        GC.vts_model = GC.vts_model.strip().lower()
        assert GC.vts_model in {"constant", "exponential", "logistic"}, 'vts_model must be either "constant", "exponential", or "logistic"'
        GC.vts_n0 = int(GC.vts_n0)
        assert GC.vts_n0 >= 1, "vts_n0 must be a positive integer"
        GC.vts_growthRate = float(GC.vts_growthRate)
        assert GC.vts_growthRate >= 0, "vts_growthRate cannot be negative"
        GC.vts_t50 = float(GC.vts_t50)
        try:
            global read_tree_newick
            from treeswift import read_tree_newick
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading TreeSwift. Install with: pip3 install treeswift"
        GC.vts_max_attempts = int(GC.vts_max_attempts)
        assert GC.vts_max_attempts > 0, "vts_max_attempts must be a positive integer"

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
            jar_file = '%s/dependencies/VirusTreeSimulator.jar' % GC.FAVITES_DIR

            # parse each seed node's transmission history
            node_to_seed = {}
            trans_per_seed = {}
            for e in GC.transmissions:
                if e[0] is None:
                    assert e[1] not in trans_per_seed, "Individual was a seed multiple times: %s" % e[1]
                    trans_per_seed[e[1]] = [e]
                    node_to_seed[e[1]] = e[1]
                else:
                    trans_per_seed[node_to_seed[e[0]]].append(e)
                    node_to_seed[e[1]] = node_to_seed[e[0]]

            # run VirusTreeSimulator on each seed individually
            GC.sampled_trees = set()
            for seed in trans_per_seed:
                #if len(trans_per_seed) ==
                nodes = set()
                vts_trans = open("ID_%s_trans.txt"%str(seed),'w')
                vts_trans.write("IDREC,IDTR,TIME_TR\n")
                for u,v,t in trans_per_seed[seed]:
                    if u is None:
                        u = 'NA'
                    elif u == v:
                        continue
                    vts_trans.write("%s,%s,%f\n" % (v,u,t))
                    nodes.add(u); nodes.add(v)
                vts_trans.flush()
                vts_samples = open("ID_%s_samples.txt"%str(seed),'w')
                vts_samples.write("IDPOP,TIME_SEQ,SEQ_COUNT\n")
                valid = False
                for n in nodes:
                    if n in GC.cn_sample_times:
                        for t in sorted(GC.cn_sample_times[n]):
                            vts_samples.write("%s,%f,%d\n" % (n,t,MF.modules["NumBranchSample"].sample_num_branches(n,t)))
                            valid = True
                vts_samples.flush()
                if valid: # don't do anything if "samples" file is empty
                    command = [GC.java_path,'-jar',jar_file,'-demoModel',GC.vts_model,'-N0',str(GC.vts_n0),'-growthRate',str(GC.vts_growthRate),'-t50',str(GC.vts_t50)]
                    if GC.random_number_seed is not None:
                        command += ['-seed',str(GC.random_number_seed)]
                        GC.random_number_seed += 1
                    command += ["ID_%s_trans.txt"%str(seed),"ID_%s_samples.txt"%str(seed),VTS_OUTPUT_PREFIX]
                    log_file = open("ID_%s_log.txt"%str(seed),'w')
                    try:
                        process = Popen(command, stdout=log_file, stderr=STDOUT)
                        while process.returncode is None:
                            process.poll()
                            if "Failed to coalesce lineages: %d"%GC.vts_max_attempts in open("ID_%s_log.txt"%str(seed)).read():
                                process.kill(); raise RuntimeError("VirusTreeSimulator failed to coalesce after %d attempts. Perhaps the parameters are too unrealistic?"%GC.vts_max_attempts)
                        process.wait(); process.communicate()
                    except FileNotFoundError:
                        chdir(GC.START_DIR)
                        assert False, "Java executable was not found: %s" % GC.java_path
                    log_file.close()
                    log_content = open("ID_%s_log.txt"%str(seed)).read()
                    if "Unsupported major.minor version" in log_content:
                        raise RuntimeError("VirusTreeSimulator.jar failed to run, likely because of an out-dated Java version. See %s/ID_%s_log.txt for error information"%(VTS_OUTPUT_DIR,str(seed)))
                    elif "Usage: virusTreeBuilder" in log_content:
                        raise RuntimeError("VirusTreeSimulator.jar failed to run. See %s/ID_%s_log.txt for error information."%(VTS_OUTPUT_DIR,str(seed)))
                    try:
                        parts = open('ID_%s_simple.nex'%str(seed)).read().strip().split('Translate')[1].split('tree TREE1')
                        translate = [l.strip()[:-1].replace("'",'').split() for l in parts[0].splitlines()][1:-1]
                        translate = [(a, MF.modules['TreeNode']().get_label()+'|'+b.split('_')[1]+'|'+b.split('_')[-1]) for a,b in translate]
                        old2new = {old:new for old,new in translate}
                        tree = parts[1].split('] = [&R] ')[1].splitlines()[0].strip()
                        # add 0 length to branches with missing lengths
                        tree = read_tree_newick(tree)
                        for n in tree.traverse_preorder():
                            if n.edge_length is None:
                                n.edge_length = 0
                        # translate labels back to FAVITES nodes
                        tmpleaf = None
                        for n in tree.traverse_leaves():
                            n.label = old2new[str(n).replace("'","")]
                            if tmpleaf is None:
                                tmpleaf = n
                        # add root edge length
                        root_length = float(str(tmpleaf).split('|')[-1])
                        while tmpleaf != None:
                            root_length -= tmpleaf.edge_length
                            tmpleaf = tmpleaf.parent
                        tree.root.edge_length += root_length
                        virus = GC.seed_to_first_virus[seed]
                        GC.sampled_trees.add((virus.get_root(),tree.newick()))
                    except FileNotFoundError:
                        chdir(GC.START_DIR)
                        assert False, "Failed to create tree. See %s/ID_%s_log.txt for error information."%(VTS_OUTPUT_DIR,str(seed))
                    remove("ID_%s_log.txt"%str(seed))
                    remove("ID_%s_simple.nex"%str(seed))
                    remove("ID_%s_detailed.nex"%str(seed))
                remove("ID_%s_trans.txt"%str(seed))
                remove("ID_%s_samples.txt"%str(seed))
            chdir(orig_dir)
            rmtree(VTS_OUTPUT_DIR, ignore_errors=True)
            GC.PRUNE_TREES = False
