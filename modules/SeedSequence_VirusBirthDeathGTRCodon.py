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
from dendropy.simulate import treesim

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
        assert "Usage: seq-gen" in check_output(['seq-gen'],stderr=STDOUT).decode(), "seqgen executable was not found: %s" % GC.seqgen_path

    def generate():
        if not hasattr(GC, "seed_sequences"):
            rootseq = SeedSequence_Virus.generate()
            treestr = treesim.birth_death_tree(birth_rate=GC.seed_birth_rate, death_rate=GC.seed_death_rate, ntax=len(GC.seed_nodes)).as_string(schema='newick')
            treestr = treestr.split(']')[1].strip()
            treestr = MF.modules['TreeUnit'].time_to_mutation_rate(treestr)
            makedirs(OUT_FOLDER, exist_ok=True)
            seqgen_file = OUT_FOLDER + '/seed.txt'
            f = open(seqgen_file, 'w')
            f.write("1 %d\nROOT %s\n1\n%s" % (len(rootseq),rootseq,treestr))
            f.close()
            command = [GC.seqgen_path,'-or','-k1'] + GC.seqgen_args.split()
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