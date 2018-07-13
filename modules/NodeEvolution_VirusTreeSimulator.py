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
from os import chdir,getcwd,makedirs
from os.path import expanduser
from subprocess import Popen,STDOUT
from glob import glob

VTS_OUTPUT_DIR = "VirusTreeSimulator_output"
VTS_TRANSMISSIONS = "transmissions.csv"
VTS_SAMPLES = "sample.csv"
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

            # create VirusTreeSimulator input files
            nodes = set()
            f = open(VTS_TRANSMISSIONS,'w')
            f.write("IDREC,IDTR,TIME_TR\n")
            for u,v,t in GC.transmissions:
                if u is None:
                    u = 'NA'
                elif u == v:
                    continue
                f.write("%s,%s,%f\n" % (v,u,t))
                nodes.add(u)
                nodes.add(v)
            f.close()
            f = open(VTS_SAMPLES,'w')
            f.write("IDPOP,TIME_SEQ,SEQ_COUNT\n")
            for n in nodes:
                if n in GC.cn_sample_times:
                    for t in sorted(GC.cn_sample_times[n]):
                        f.write("%s,%f,%d\n" % (n,t,MF.modules['NumBranchSample'].sample_num_branches(n,t)))
            f.close()

            # run VirusTreeSimulator
            jar_file = '%s/dependencies/VirusTreeSimulator.jar' % GC.FAVITES_DIR
            log_file = open("log.txt",'w')
            try:
                command = [GC.java_path,'-jar',jar_file,'-demoModel',GC.vts_model,'-N0',str(GC.vts_n0),'-growthRate',str(GC.vts_growthRate),'-t50',str(GC.vts_t50)]
                if GC.random_number_seed is not None:
                    command += ['-seed',str(GC.random_number_seed)]
                    GC.random_number_seed += 1
                command += [VTS_TRANSMISSIONS,VTS_SAMPLES,VTS_OUTPUT_PREFIX]
                process = Popen(command, stdout=log_file, stderr=STDOUT)
                while process.returncode is None:
                    process.poll()
                    if "Failed to coalesce lineages: %d"%GC.vts_max_attempts in open("log.txt").read():
                        process.kill()
                        raise RuntimeError("VirusTreeSimulator failed to coalesce after %d attempts. Perhaps the parameters are too unrealistic?"%GC.vts_max_attempts)
                process.wait(); process.communicate()
            except FileNotFoundError:
                chdir(GC.START_DIR)
                assert False, "Java executable was not found: %s" % GC.java_path
            log_file.close()
            log_content = open("log.txt").read()
            if "Unsupported major.minor version" in log_content:
                raise RuntimeError("VirusTreeSimulator.jar failed to run, likely because of an out-dated Java version. See %s/log.txt for error information"%VTS_OUTPUT_DIR)
            elif "Usage: virusTreeBuilder" in log_content:
                raise RuntimeError("VirusTreeSimulator.jar failed to run. See %s/log.txt for error information."%VTS_OUTPUT_DIR)

            # parse VirusTreeSimulator output
            GC.sampled_trees = set()
            for filename in glob('*_simple.nex'):
                cn_node = GC.contact_network.get_node(filename.split('_')[1])
                parts = open(filename).read().strip().split('Translate')[1].split('tree TREE1')
                translate = [l.strip()[:-1].replace("'",'').split() for l in parts[0].splitlines()][1:-1]
                translate = [(a, MF.modules['TreeNode']().get_label()+'|'+b.split('_')[1]+'|'+b.split('_')[-1]) for a,b in translate]
                translate_file = '%s.translate' % filename.split('.')[0]
                f = open(translate_file,'w')
                f.write('\n'.join(['%s\t%s' % e for e in translate]))
                f.close()
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
                # write to disk
                tree = str(tree)
                tree_file = '%s.tre.gz' % filename.split('.')[0]
                f = gopen(tree_file,'wb',9)
                f.write(tree.encode())
                f.close()
                virus = GC.seed_to_first_virus[cn_node]
                GC.sampled_trees.add((virus.get_root(),tree))
            chdir(orig_dir)
            GC.PRUNE_TREES = False
