#! /usr/bin/env python3
'''
Niema Moshiri 2016

"NodeEvolution" module, implemented with Birth Death model.
'''
from NodeEvolution import NodeEvolution
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
import random as rng

class NodeEvolution_BirthDeath(NodeEvolution):
    def cite():
        return GC.CITATION_DENDROPY

    def init():
        try:
            global birth_death_tree
            from dendropy.model.birthdeath import birth_death_tree
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading DendroPy. Install with: pip3 install dendropy"

    def evolve_to_current_time(node, finalize=False):
        if node is None:
            return
        viruses = [virus for virus in node.viruses()]
        for virus in viruses:
            time = GC.time-virus.get_time()
            if time > 0:
                node.remove_virus(virus)
                success = False
                for _ in range(100):
                    tree = birth_death_tree(GC.bd_birth, GC.bd_death, birth_rate_sd=GC.bd_birth_sd, death_rate_sd=GC.bd_death_sd, max_time=time, repeat_until_success=True, rng=rng)
                    if tree.seed_node.num_child_nodes() > 1:
                        success = True
                        break
                assert success, "Failed to create non-empty Birth-Death tree after 100 attempts. Perhaps try a higher birth rate or lower death rate?"
                virus.set_time(virus.get_time() + tree.seed_node.edge_length)
                for c in tree.seed_node.child_node_iter():
                    GC.treenode_add_child(virus,c,node)
