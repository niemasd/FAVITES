#! /usr/bin/env python3
'''
Niema Moshiri 2016

"NodeEvolution" module, implemented with Dual Birth model
'''
from NodeEvolution import NodeEvolution
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from os.path import expanduser
from subprocess import check_output

class NodeEvolution_DualBirth(NodeEvolution):
    def cite():
        return [GC.CITATION_DUALBIRTH, GC.CITATION_TREESWIFT]

    def init():
        GC.rate_A = float(GC.rate_A)
        GC.rate_B = float(GC.rate_B)
        GC.dualbirth_path = expanduser(GC.dualbirth_path.strip())
        try:
            global read_tree_newick
            from treeswift import read_tree_newick
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading TreeSwift. Install with: pip3 install treeswift"

    def evolve_to_current_time(node, finalize=False):
        viruses = [virus for virus in node.viruses()]
        for virus in viruses:
            time = GC.time-virus.get_time()
            if time > 0:
                node.remove_virus(virus)
                try:
                    command = [GC.dualbirth_path,str(GC.rate_A),str(GC.rate_B),'-t',str(time)]
                    if GC.random_number_seed is not None:
                        command += ['-s',str(GC.random_number_seed)]
                        GC.random_number_seed += 1
                    treestr = check_output(command).decode()
                except FileNotFoundError:
                    from os import chdir
                    chdir(GC.START_DIR)
                    assert False, "dualbirth executable was not found: %s" % GC.dualbirth_path
                tree = read_tree_newick(treestr)
                virus.set_time(virus.get_time() + tree.root.edge_length)
                for c in tree.root.children:
                    GC.treenode_add_child(virus,c,node)