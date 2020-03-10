#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SequenceEvolution" module, implemented with Seq-Gen
'''
from SequenceEvolution import SequenceEvolution
import FAVITES_GlobalContext as GC
import modules.FAVITES_ModuleFactory as MF
from datetime import datetime
from io import StringIO
from os.path import expanduser
from os import chdir,getcwd,makedirs,remove
from shutil import rmtree
from subprocess import CalledProcessError,check_output,STDOUT
from sys import stderr

SEQGEN_OUTPUT_DIR = "SeqGen_output"
SEQGEN_MODES = "HKY, F84, GTR, JTT, WAG, PAM, BLOSUM, MTREV, CPREV45, MTART, LG, GENERAL"

class SequenceEvolution_SeqGen(SequenceEvolution):
    def cite():
        return [GC.CITATION_TREESWIFT, GC.CITATION_SEQGEN]

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
        mode = GC.seqgen_args.split('-m')[1].strip().split(' ')[0]
        assert mode in SEQGEN_MODES.split(', '), "Invalid Seq-Gen model (%s). Options: %s" % (mode,SEQGEN_MODES)
        GC.check_seqgen_executable()
        try:
            global read_tree_newick
            from treeswift import read_tree_newick
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading TreeSwift. Install with: pip3 install treeswift"

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
            treestr = treestr.strip().replace('[&R] ','')
            if ',' not in treestr: # if one-node tree, add DUMMY 0-length leaf
                treestr = "(DUMMY:0,%s);" % treestr.replace('(','').replace(')','')[:-1]
            else: # otherwise, resolve polytomies and unifurcations
                tmp = read_tree_newick(treestr)
                tmp.suppress_unifurcations(); tmp.resolve_polytomies()
                treestr = tmp.newick().replace('[&R] ','')

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
                seqgen_out = check_output(command, stdin=open('%s.txt'%label), stderr=open('log_%s.txt'%label,'w')).decode('ascii')
            except CalledProcessError as e:
                f = open('seqgen.err','w'); f.write(str(e)); f.close()
                chdir(GC.START_DIR)
                assert False, "Seq-Gen encountered an error while processing: %s" % label
            error = False
            for line in open('log_%s.txt'%label):
                if line.startswith("Error") or 'Bad state in ancestoral sequence' in line: # have to manually check for errors (Seq-Gen exits with status 0)
                    error = True; break
            if error:
                chdir(GC.START_DIR)
                assert False, "Seq-Gen encountered an error while processing: %s" % label
            remove('log_%s.txt'%label); remove('%s.txt'%label)

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
        rmtree(SEQGEN_OUTPUT_DIR, ignore_errors=True)
