#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSequence" module, which samples a single viral sequence using a profile HMM
generated from a multiple sequence alignment from some public dataset, then
simulates a coalescent tree with "num_seeds" leaves, and then evolves the
sequence down this tree under a GTR codon model to get seed sequences for each
seed.
'''
from SeedSequence import SeedSequence
from SeedSequence_Virus import SeedSequence_Virus
from SequenceEvolution_GTRGammaSeqGen import SequenceEvolution_GTRGammaSeqGen
import FAVITES_GlobalContext as GC
import modules.FAVITES_ModuleFactory as MF
from subprocess import check_output
from os.path import expanduser
from os import chdir,makedirs
from dendropy import TaxonNamespace
from dendropy.simulate import treesim

OUT_FOLDER = "seed_sequences"
class SeedSequence_VirusCoalescentGTRGamma(SeedSequence):
    def cite():
        return [GC.CITATION_HMMER, GC.CITATION_DENDROPY, GC.CITATION_SEQGEN]

    def init():
        SeedSequence_Virus.init()
        SequenceEvolution_GTRGammaSeqGen.init()
        GC.seed_population = int(GC.seed_population)
        assert "Usage: seq-gen" in check_output(['seq-gen'],stderr=STDOUT).decode(), "seqgen executable was not found: %s" % GC.seqgen_path

    def generate():
        if not hasattr(GC, "seed_sequences"):
            rootseq = SeedSequence_Virus.generate()
            treestr = treesim.pure_kingman_tree(TaxonNamespace([str(i) for i in range(GC.contact_network.num_nodes())]), pop_size=GC.seed_population).as_string(schema='newick')
            treestr = MF.modules['TreeUnit'].time_to_mutation_rate(treestr)
            makedirs(OUT_FOLDER, exist_ok=True)
            seqgen_file = OUT_FOLDER + '/seed.txt'
            f = open(seqgen_file, 'w')
            f.write("1 %d\nROOT %s\n1\n%s" % (len(rootseq),rootseq,treestr))
            f.close()
            command = [GC.seqgen_path,'-or','-k1'] + GC.seqgen_args.split()
            try:
                seqgen_out = check_output(command, stdin=open(seqgen_file), stderr=open(OUT_FOLDER + '/log_seqgen.txt','w')).decode('ascii')
            except CalledProcessError as e:
                chdir(GC.START_DIR)
                f = open('error.log','w'); f.write(e.output); f.close()
                assert False, "Seq-Gen encountered an error"
            GC.seed_sequences = {line.split()[-1].strip() for line in seqgen_out.splitlines()[1:]}
        return GC.seed_sequences.pop()