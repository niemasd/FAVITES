#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SequenceEvolution" module, implemented such that no mutations are allowed
(i.e., all sequences are identical to the initial infection sequence).
'''
from SequenceEvolution import SequenceEvolution # abstract SequenceEvolution class
import FAVITES_GlobalContext as GC

class SequenceEvolution_NoMutation(SequenceEvolution):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        pass

    def finalize():
        GC.final_sequences = {}
        for root,treestr in GC.pruned_newick_trees:
            seq = root.get_seq()
            for leaf in root.leaves():
                cn_label = leaf.get_contact_network_node().get_name()
                sample_time = leaf.get_time()
                if cn_label not in GC.final_sequences:
                    GC.final_sequences[cn_label] = {}
                if sample_time not in GC.final_sequences[cn_label]:
                    GC.final_sequences[cn_label][sample_time] = []
                GC.final_sequences[cn_label][sample_time].append((leaf,seq))

    def evolve_to_current_time(node):
        pass
