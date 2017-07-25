#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SequenceEvolution" module, implemented with Seq-Gen
'''
from SequenceEvolution import SequenceEvolution
import FAVITES_GlobalContext as GC
import modules.FAVITES_ModuleFactory as MF
from datetime import datetime
from os.path import expanduser
from os import chdir,getcwd,makedirs
from subprocess import check_output,STDOUT
from sys import stderr

SEQGEN_OUTPUT_DIR = "SeqGen_output"

class SequenceEvolution_SeqGen(SequenceEvolution):
    def cite():
        return GC.CITATION_SEQGEN

    def init():
        GC.seqgen_path = expanduser(GC.seqgen_path.strip())
        GC.seqgen_args = GC.seqgen_args.strip()
        assert '-d' not in GC.seqgen_args, "Do not use the Seq-Gen -d argument"
        assert '-k' not in GC.seqgen_args, "Do not use the Seq-Gen -k argument"
        assert '-l' not in GC.seqgen_args, "Do not use the Seq-Gen -l argument"
        assert '-n' not in GC.seqgen_args, "Do not use the Seq-Gen -n argument"
        assert '-o' not in GC.seqgen_args, "Do not use the Seq-Gen -o argument"
        assert '-p' not in GC.seqgen_args, "Do not use the Seq-Gen -p argument"
        assert '-s' not in GC.seqgen_args, "Do not use the Seq-Gen -s argument"
        assert '-m' in GC.seqgen_args, "Must specify a Seq-Gen model using the -m argument"

    def evolve_to_current_time(node):
        pass

    def finalize():
        # create directory for Seq-Gen output
        orig_dir = getcwd()
        makedirs(SEQGEN_OUTPUT_DIR, exist_ok=True)
        chdir(SEQGEN_OUTPUT_DIR)

        # perform sequence evolution
        label_to_node = MF.modules['TreeNode'].label_to_node()
        for root,treestr in GC.pruned_newick_trees:
            label = root.get_label()
            rootseq = root.get_seq()
            if GC.VERBOSE:
                print('[%s] Seq-Gen evolving sequences on tree: %s' % (datetime.now(),treestr), file=stderr)
                print('[%s] Seq-Gen root sequence: %s' % (datetime.now(),rootseq), file=stderr)
            f = open(label + '.txt','w')
            f.write("1 %d\n%s %s\n1\n%s" % (len(rootseq),label,rootseq,treestr))
            f.close()
            command = [GC.seqgen_path,'-or','-k1'] + GC.seqgen_args.split()
            seqgen_out = check_output(command, stdin=open(label+'.txt'), stderr=open('log_'+label+'.txt','w')).decode('ascii')
            seqs = {}
            for line in seqgen_out.splitlines()[1:]:
                l,s = line.strip().split(' ')
                seqs[l.strip()] = s.strip()
            FIX_GC = False
            if not hasattr(GC,'leaves_at_sample_time'):
                FIX_GC = True
                GC.leaves_at_sample_time = {} # see GlobalContext for what this is
            leaves = set()
            for label in seqs:
                leaf = MF.modules['TreeNode'].str_to_node(label)
                leaf.set_seq(seqs[label])
                leaves.add(leaf)
                if FIX_GC:
                    cn_node = leaf.get_contact_network_node()
                    t = leaf.get_time()
                    if cn_node not in GC.leaves_at_sample_time:
                        GC.leaves_at_sample_time[cn_node] = {}
                    if t not in GC.leaves_at_sample_time[cn_node]:
                        GC.leaves_at_sample_time[cn_node][t] = set()
                    GC.leaves_at_sample_time[cn_node][t].add(leaf)
            root.set_leaves(leaves)
        chdir(orig_dir)