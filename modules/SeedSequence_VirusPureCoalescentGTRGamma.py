#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSequence" module, which samples a single viral sequence using a profile HMM
generated from a multiple sequence alignment from some public dataset, then
simulates a pure coalescent tree with "num_seeds" leaves, and then evolves the
sequence down this tree under a GTR+Gamma model to get seed sequences for each
seed.
'''
from SeedSequence import SeedSequence
from SeedSequence_Virus import SeedSequence_Virus
from SequenceEvolution_GTRGammaSeqGen import SequenceEvolution_GTRGammaSeqGen
import FAVITES_GlobalContext as GC
import modules.FAVITES_ModuleFactory as MF
from subprocess import check_output,STDOUT
from os.path import expanduser
from os import chdir,makedirs

OUT_FOLDER = "seed_sequences"
class SeedSequence_VirusPureCoalescentGTRGamma(SeedSequence):
    def cite():
        return [GC.CITATION_HMMER, GC.CITATION_DENDROPY, GC.CITATION_SEQGEN]

    def init():
        SeedSequence_Virus.init()
        SequenceEvolution_GTRGammaSeqGen.init()
        GC.seed_population = float(GC.seed_population)
        assert GC.seed_population > 0, "seed_population must be positive"
        GC.check_seqgen_executable()
        try:
            global TaxonNamespace
            from dendropy import TaxonNamespace
            global treesim
            from dendropy.simulate import treesim
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading DendroPy. Install with: pip3 install dendropy"

    def generate():
        if not hasattr(GC, "seed_sequences"):
            rootseq = SeedSequence_Virus.generate()
            treestr = GC.pure_kingman_tree(len(GC.seed_nodes), pop_size=GC.seed_population)
            makedirs(OUT_FOLDER, exist_ok=True)
            f = open(OUT_FOLDER + '/time_tree.tre','w')
            f.write(treestr)
            f.close()
            treestr = MF.modules['TreeUnit'].time_to_mutation_rate(treestr)
            seqgen_file = OUT_FOLDER + '/seed.txt'
            f = open(seqgen_file, 'w')
            f.write("1 %d\nROOT %s\n1\n%s" % (len(rootseq),rootseq,treestr))
            f.close()
            command = [GC.seqgen_path,'-or','-k1']
            if GC.random_number_seed is not None:
                command += ['-z%d'%GC.random_number_seed]
            command += GC.seqgen_args.split()
            try:
                seqgen_out = check_output(command, stdin=open(seqgen_file), stderr=open(OUT_FOLDER + '/log_seqgen.txt','w')).decode('ascii')
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
