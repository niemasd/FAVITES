#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SequenceEvolution" module, implemented such that no mutations are allowed
(i.e., all sequences are identical to the initial infection sequence).
'''
from SequenceEvolution import SequenceEvolution
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from treeswift import read_tree_newick

class SequenceEvolution_NoMutation(SequenceEvolution):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        pass

    def finalize():
        GC.final_sequences = {}; TreeNode = MF.modules['TreeNode']
        for root,treestr in GC.pruned_newick_trees:
            seq = root.get_seq(); leaves = list()
            for node in read_tree_newick(treestr).traverse_leaves():
                virus_name, cn_label, t_str = [s.strip() for s in node.label.split('|')]; sample_time = float(t_str)
                if cn_label not in GC.final_sequences:
                    GC.final_sequences[cn_label] = {}
                if sample_time not in GC.final_sequences[cn_label]:
                    GC.final_sequences[cn_label][sample_time] = []
                leaf = TreeNode(time=sample_time, seq=seq, contact_network_node=GC.contact_network.get_node(cn_label)); leaves.append(leaf)
                GC.final_sequences[cn_label][sample_time].append((leaf,seq))
            root.set_leaves(leaves)

    def evolve_to_current_time(node):
        pass
