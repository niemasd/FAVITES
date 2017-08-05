#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSequence" module, which samples a single viral sequence using a profile HMM
generated from a multiple sequence alignment from some public dataset, then
simulates a birth-death tree with "num_seeds" leaves, and then evolves the
sequence down this tree under the GTR+Gamma model to get seed sequences for each
seed.
'''
from SeedSequence import SeedSequence
from SeedSequence_Virus import SeedSequence_Virus
from SequenceEvolution_GTRGammaSeqGen import SequenceEvolution_GTRGammaSeqGen
import FAVITES_GlobalContext as GC
from subprocess import check_output
from os.path import expanduser
from os import makedirs
import dendropy
from dendropy.simulate import treesim

OUT_FOLDER = "seed_sequences"
class SeedSequence_VirusBirthDeathGTRGamma(SeedSequence):
    def cite():
        return [GC.CITATION_HMMER, GC.CITATION_DENDROPY, GC.CITATION_SEQGEN]

    def init():
        SeedSequence_Virus.init()
        SequenceEvolution_GTRGammaSeqGen.init()
        GC.seed_birth_rate = float(GC.seed_birth_rate)
        assert GC.seed_birth_rate > 0, "seed_birth_rate must be positive"
        GC.seed_death_rate = float(GC.seed_death_rate)
        assert GC.seed_death_rate >= 0, "seed_death_rate must be at least 0"

    def generate():
        if not hasattr(GC, "seed_sequences"):
            num_seeds = len(GC.seed_nodes)
            rootseq = SeedSequence_Virus.generate()
            treestr = treesim.birth_death_tree(birth_rate=GC.seed_birth_rate, death_rate=GC.seed_death_rate, ntax=num_seeds).as_string(schema='newick')
            treestr = treestr.split(']')[1].strip()
            makedirs(OUT_FOLDER, exist_ok=True)
            seqgen_file = OUT_FOLDER + '/seed.txt'
            f = open(seqgen_file, 'w')
            f.write("1 %d\nROOT %s\n1\n%s" % (len(rootseq),rootseq,treestr))
            f.close()
            command = [GC.seqgen_path,'-or','-k1'] + GC.seqgen_args.split()
            try:
                seqgen_out = check_output(command, stdin=open(seqgen_file), stderr=open('log_seqgen.txt','w')).decode('ascii')
            except:
                from os import chdir
                chdir(GC.START_DIR)
                assert False, "seqgen executable was not found: %s" % GC.seqgen_path
            GC.seed_sequences = {line.split()[-1].strip() for line in seqgen_out.splitlines()[1:]}
            letters = set()
            for seq in GC.seed_sequences:
                for c in seq:
                    letters.add(c)
        return GC.seed_sequences.pop()