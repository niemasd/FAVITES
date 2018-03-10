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
        return [GC.CITATION_DENDROPY, GC.CITATION_SEQGEN]

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
        GC.check_seqgen_executable()
        try:
            global Tree
            from dendropy import Tree
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading DendroPy. Install with: pip3 install dendropy"

    def evolve_to_current_time(node):
        pass

    def finalize():
        # create directory for Seq-Gen output
        orig_dir = getcwd()
        makedirs(SEQGEN_OUTPUT_DIR, exist_ok=True)
        chdir(SEQGEN_OUTPUT_DIR)

        # perform sequence evolution
        assert len(GC.pruned_newick_trees) != 0, "No trees were generated"
        for root,treestr in GC.pruned_newick_trees:
            treestr = treestr.strip()
            if ',' not in treestr: # if one-node tree, add DUMMY 0-length leaf
                treestr = "(DUMMY:0,%s);" % treestr.replace('(','').replace(')','')[:-1]
            else: # otherwise, resolve polytomies and unifurcations
                tmp = Tree.get(data=treestr, schema='newick')
                tmp.suppress_unifurcations(); tmp.resolve_polytomies()
                treestr = tmp.as_string(schema="newick").replace("'",'')

            # run Seq-Gen
            label = root.get_label()
            rootseq = root.get_seq()
            if GC.VERBOSE:
                print('[%s] Seq-Gen evolving sequences on tree: %s' % (datetime.now(),treestr), file=stderr)
                print('[%s] Seq-Gen root sequence: %s' % (datetime.now(),rootseq), file=stderr)
            f = open('%s.txt' % label,'w')
            f.write("1 %d\n%s %s\n1\n%s" % (len(rootseq),label,rootseq,treestr))
            f.close()
            command = [GC.seqgen_path,'-or','-k1']
            if GC.random_number_seed is not None:
                command += ['-z%d'%GC.random_number_seed]
                GC.random_number_seed += 1
            command += GC.seqgen_args.split()
            try:
                seqgen_out = check_output(command, stdin=open(label+'.txt'), stderr=open('log_'+label+'.txt','w')).decode('ascii')
            except CalledProcessError as e:
                f = open('seqgen.err','w'); f.write(str(e)); f.close()
                chdir(GC.START_DIR)
                assert False, "Seq-Gen encountered an error while processing: %s" % label
            error = False
            for line in open('log_'+label+'.txt'):
                if line.startswith("Error"): # have to manually check for errors (Seq-Gen exits with status 0)
                    error = True; break
            if error:
                chdir(GC.START_DIR)
                assert False, "Seq-Gen encountered an error while processing: %s" % label
            f = open('seqgen_%s.out' % label,'w'); f.write(seqgen_out); f.close()

            # store leaf sequences in GlobalContext
            if not hasattr(GC,'final_sequences'): # GC.final_sequences[cn_node][t] = set of (label,seq) tuples
                GC.final_sequences = {}
            for line in seqgen_out.splitlines()[1:]:
                leaf,seq = line.split(' ')
                if leaf == 'DUMMY':
                    continue
                virus_label,cn_label,sample_time = leaf.split('|')
                sample_time = float(sample_time)
                if cn_label not in GC.final_sequences:
                    GC.final_sequences[cn_label] = {}
                if sample_time not in GC.final_sequences[cn_label]:
                    GC.final_sequences[cn_label][sample_time] = []
                GC.final_sequences[cn_label][sample_time].append((leaf,seq))
        chdir(orig_dir)