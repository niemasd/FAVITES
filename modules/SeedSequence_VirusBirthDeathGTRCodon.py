#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSequence" module, which samples a single viral sequence using a profile HMM
generated from a multiple sequence alignment from some public dataset, then
simulates a birth-death tree with "num_seeds" leaves, and then evolves the
sequence down this tree under a GTR codon model to get seed sequences for each
seed.
'''
from SeedSequence import SeedSequence
from SeedSequence_Virus import SeedSequence_Virus
from SequenceEvolution_GTRCodonSeqGen import SequenceEvolution_GTRCodonSeqGen
import FAVITES_GlobalContext as GC
import modules.FAVITES_ModuleFactory as MF
from subprocess import check_output,STDOUT
from os.path import expanduser
from os import chdir,makedirs
import random as rng

OUT_FOLDER = "seed_sequences"
class SeedSequence_VirusBirthDeathGTRCodon(SeedSequence):
    def cite():
        return [GC.CITATION_HMMER, GC.CITATION_DENDROPY, GC.CITATION_SEQGEN]

    def init():
        SeedSequence_Virus.init()
        SequenceEvolution_GTRCodonSeqGen.init()
        GC.seed_birth_rate = float(GC.seed_birth_rate)
        assert GC.seed_birth_rate > 0, "seed_birth_rate must be positive"
        GC.seed_death_rate = float(GC.seed_death_rate)
        assert GC.seed_death_rate >= 0, "seed_death_rate must be at least 0"
        GC.check_seqgen_executable()
        try:
            global treesim
            from dendropy.simulate import treesim
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading DendroPy. Install with: pip3 install dendropy"

    def generate():
        if not hasattr(GC, "seed_sequences"):
            rootseq = SeedSequence_Virus.generate()
            treestr = treesim.birth_death_tree(birth_rate=GC.seed_birth_rate, death_rate=GC.seed_death_rate, num_extant_tips=len(GC.seed_nodes), rng=rng).as_string(schema='newick')
            makedirs(OUT_FOLDER, exist_ok=True)
            f = open(OUT_FOLDER + '/time_tree.tre','w')
            f.write(treestr)
            f.close()
            treestr = treestr.split(']')[1].strip()
            treestr = MF.modules['TreeUnit'].time_to_mutation_rate(treestr)
            seqgen_file = OUT_FOLDER + '/seed.txt'
            f = open(seqgen_file, 'w')
            f.write("1 %d\nROOT %s\n1\n%s" % (len(rootseq),rootseq,treestr))
            f.close()
            command = [GC.seqgen_path,'-or','-k1']
            if GC.random_number_seed is not None:
                command += ['-z%d'%GC.random_number_seed]
                GC.random_number_seed += 1
            command += GC.seqgen_args.split()
            try:
                seqgen_out = check_output(command, stdin=open(seqgen_file), stderr=open('log_seqgen.txt','w')).decode('ascii')
                f = open(OUT_FOLDER + '/seqgen.out','w')
                f.write(seqgen_out)
                f.close()
            except CalledProcessError as e:
                f = open('seqgen.err','w'); f.write(str(e)); f.close()
                chdir(GC.START_DIR)
                assert False, "Seq-Gen encountered an error"
            GC.seed_sequences = [line.split()[-1].strip() for line in seqgen_out.splitlines()[1:]]
        try:
            return GC.seed_sequences.pop()
        except IndexError:
            assert False, "Late seeds are not supported at this time"

    def merge_trees():
        return GC.merge_trees_seqgen()