#! /usr/bin/env python3
'''
Niema Moshiri 2020

"NodeEvolution" module, where the evolutionary tree(s) is/are equivalent to the
transmission tree(s).
'''
from NodeEvolution import NodeEvolution
import FAVITES_GlobalContext as GC

class NodeEvolution_TransmissionTree(NodeEvolution):
    def cite():
        return [GC.CITATION_TREESWIFT]

    def init():
        try:
            global Node
            from treeswift import Node
            global Tree
            from treeswift import Tree
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading TreeSwift. Install with: pip3 install treeswift"

    def evolve_to_current_time(node, finalize=False):
        # if it's not the end yet, just dummy
        if not finalize:
            if node is None:
                return
            for virus in node.viruses():
                virus.set_time(GC.time)
        elif not hasattr(GC,'sampled_trees'):
            # convert transmission tree to TreeSwift
            seed_roots = dict(); person_to_leaf = dict()
            for u,v,t in GC.transmissions:
                if v in person_to_leaf: # ignore repeat infections
                    continue
                if u is None:
                    v_new = Node(edge_length=t); v_new.time = t
                    seed_roots[v] = v_new; person_to_leaf[v] = v_new
                else:
                    u_old = person_to_leaf[u]
                    u_new = Node(edge_length=0); u_new.time = u_old.time
                    v_new = Node(edge_length=t-u_old.time); v_new.time = t
                    u_old.add_child(u_new); u_old.add_child(v_new)
                    person_to_leaf[u] = u_new; person_to_leaf[v] = v_new

            # extend or remove leaves based on sample times
            remove = set(); count = 1
            for u in person_to_leaf:
                if u in GC.cn_sample_times and len(GC.cn_sample_times[u]) != 0:
                    u_leaf = person_to_leaf[u]
                    u_leaf.edge_length += (min(GC.cn_sample_times[u]) - u_leaf.time); u_leaf.time = min(GC.cn_sample_times[u])
                    u_leaf.label = "N%d|%s|%f" % (count, str(u), u_leaf.time); count += 1
                else:
                    remove.add(person_to_leaf[u])
            seed_trees = dict()
            for seed in seed_roots:
                tree = Tree(is_rooted=True); tree.root = seed_roots[seed]; curr_remove = set()
                for u in tree.traverse_leaves():
                    if u in remove:
                        u.label = "DUMMY_%d" % count; curr_remove.add(u.label); count += 1
                seed_trees[seed] = tree.extract_tree_without(curr_remove)

            # output phylogenies
            GC.sampled_trees = set()
            for seed in seed_roots:
                GC.sampled_trees.add((GC.seed_to_first_virus[seed].get_root(), seed_trees[seed].newick()))
            GC.PRUNE_TREES = False
