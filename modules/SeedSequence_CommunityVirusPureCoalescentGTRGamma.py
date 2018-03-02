#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSequence" module, which samples a single viral sequence using a profile HMM
generated from a multiple sequence alignment from some public dataset, then
simulates a pure coalescent tree for each community's seed individuals,
then coalesces the roots of each community's tree via pure coalescent,
and then evolves the sequence down the resulting tree under a GTR+Gamma model to
get seed sequences for each seed.
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
class SeedSequence_CommunityVirusPureCoalescentGTRGamma(SeedSequence):
    def cite():
        return [GC.CITATION_HMMER, GC.CITATION_DENDROPY, GC.CITATION_SEQGEN]

    def init():
        assert MF.modules['ContactNetworkGenerator'].__name__ in GC.COMMUNITY_GENERATORS, "Must use a ContactNetworkGenerator that creates communities (%s)" % ', '.join(sorted(GC.COMMUNITY_GENERATORS))
        SeedSequence_Virus.init()
        SequenceEvolution_GTRGammaSeqGen.init()
        GC.community_root_population = float(GC.community_root_population)
        assert GC.community_root_population > 0, "community_root_population must be a positive float"
        assert isinstance(GC.community_seed_populations, list), "community_seed_populations must be a list of positive floats"
        for i in range(len(GC.community_seed_populations)):
            GC.community_seed_populations[i] = float(GC.community_seed_populations[i])
            assert GC.community_seed_populations[i] > 0, "community_seed_populations must be a list of positive floats"
        GC.check_seqgen_executable()
        try:
            global dendropy
            import dendropy
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading DendroPy. Install with: pip3 install dendropy"

    def generate():
        if not hasattr(GC, "seed_sequences"):
            assert len(GC.community_seed_populations) == len(GC.cn_communities), "The length of community_seed_populations does not match the number of communities"
            seed_nodes_str = {n.get_name() for n in GC.seed_nodes}
            community_trees = []
            leaf_num = 0
            for i in range(len(GC.cn_communities)):
                community_seeds = [n for n in GC.cn_communities[i] if n in seed_nodes_str]
                if len(community_seeds) != 0:
                    t = dendropy.Tree.get(data=GC.pure_kingman_tree(len(community_seeds), pop_size=GC.community_seed_populations[i]),schema='newick')
                    for n in t.leaf_node_iter():
                        n.taxon = dendropy.datamodel.taxonmodel.Taxon(str(leaf_num))
                        leaf_num += 1
                community_trees.append(t)
            assert len(community_trees) != 0, "No community seed trees produced"
            if len(community_trees) == 1:
                treestr = community_trees[0].as_string(schema='newick')
            else:
                t = dendropy.Tree.get(data=GC.pure_kingman_tree(len(community_trees), pop_size=GC.community_root_population),schema='newick')
                for n in t.leaf_node_iter():
                    n.add_child(community_trees.pop().seed_node)
                t.suppress_unifurcations()
                treestr = t.as_string(schema='newick')
            rootseq = SeedSequence_Virus.generate()
            makedirs(OUT_FOLDER, exist_ok=True)
            f = open(OUT_FOLDER + '/time_tree.tre','w')
            f.write(treestr)
            f.close()
            treestr = MF.modules['TreeUnit'].time_to_mutation_rate(treestr)
            seqgen_file = OUT_FOLDER + '/seed.txt'
            f = open(seqgen_file, 'w')
            f.write("1 %d\nROOT %s\n1\n%s" % (len(rootseq),rootseq,treestr))
            f.close()
            command = [GC.seqgen_path,'-or','-k1'] + GC.seqgen_args.split()
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
