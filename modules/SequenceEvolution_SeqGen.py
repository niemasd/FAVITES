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
from subprocess import CalledProcessError,check_output,STDOUT
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
        assert "Usage: seq-gen" in check_output(['seq-gen'],stderr=STDOUT).decode(), "seqgen executable was not found: %s" % GC.seqgen_path

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
            # run Seq-Gen
            label = root.get_label()
            rootseq = root.get_seq()
            if GC.VERBOSE:
                print('[%s] Seq-Gen evolving sequences on tree: %s' % (datetime.now(),treestr), file=stderr)
                print('[%s] Seq-Gen root sequence: %s' % (datetime.now(),rootseq), file=stderr)
            f = open(label + '.txt','w')
            f.write("1 %d\n%s %s\n1\n%s" % (len(rootseq),label,rootseq,treestr))
            f.close()
            command = [GC.seqgen_path,'-or','-k1'] + GC.seqgen_args.split()
            try:
                seqgen_out = check_output(command, stdin=open(label+'.txt'), stderr=open('log_'+label+'.txt','w')).decode('ascii')
                f = open('seqgen_%s.out' % label,'w')
                f.write(seqgen_out)
                f.close()
            except CalledProcessError as e:
                f = open('seqgen.err','w'); f.write(str(e)); f.close()
                chdir(GC.START_DIR)
                assert False, "Seq-Gen encountered an error while processing: %s" % label

            # store leaf sequences in GlobalContext
            if not hasattr(GC,'final_sequences'): # GC.final_sequences[cn_node][t] = set of (label,seq) tuples
                GC.final_sequences = {}
            for line in seqgen_out.splitlines()[1:]:
                leaf,seq = line.split(' ')
                virus_label,cn_label,sample_time = leaf.split('|')
                sample_time = float(sample_time)
                if cn_label not in GC.final_sequences:
                    GC.final_sequences[cn_label] = {}
                if sample_time not in GC.final_sequences[cn_label]:
                    GC.final_sequences[cn_label][sample_time] = []
                GC.final_sequences[cn_label][sample_time].append((leaf,seq))
        chdir(orig_dir)