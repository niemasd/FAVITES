#! /usr/bin/env python3
'''
Niema Moshiri 2016

"NodeEvolution" module, implemented with Birth Death model.
'''
from NodeEvolution import NodeEvolution
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from dendropy.model.birthdeath import birth_death_tree

def add_child(parent_treenode, child_dpnode, cn_node):
    if parent_treenode.get_time() >= GC.time:
        parent_treenode.set_time(GC.time)
        cn_node.add_virus(parent_treenode)
        return
    newnode = TreeNode(time=parent_treenode.get_time()+child_dpnode.edge_length, contact_network_node=cn_node)
    parent_treenode.add_child(newnode)
    for c in child_dpnode.child_node_iter():
        add_child(newnode,c,cn_node)
    if child_dpnode.num_child_nodes() == 0:
        newnode.set_time(GC.time)
        cn_node.add_virus(newnode)

class NodeEvolution_BirthDeath(NodeEvolution):
    def init():
        global TreeNode
        TreeNode = MF.modules['TreeNode']

    def evolve_to_current_time(node, finalize=False):
        viruses = [virus for virus in node.viruses()]
        for virus in viruses:
            time = GC.time-virus.get_time()
            if time > 0:
                node.remove_virus(virus)
                success = False
                for _ in range(100):
                    tree = birth_death_tree(GC.bd_birth, GC.bd_death, birth_rate_sd=GC.bd_birth_sd, death_rate_sd=GC.bd_death_sd, max_time=time)
                    if tree.seed_node.num_child_nodes() > 1:
                        success = True
                        break
                assert success, "Failed to create non-empty Birth-Death tree after 100 attempts. Perhaps try a higher birth rate or lower death rate?"
                virus.set_time(virus.get_time() + tree.seed_node.edge_length)
                for c in tree.seed_node.child_node_iter():
                    add_child(virus,c,node)