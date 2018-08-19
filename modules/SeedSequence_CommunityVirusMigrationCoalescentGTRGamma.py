#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SeedSequence" module, which samples a single viral sequence using a profile HMM
generated from a multiple sequence alignment from some public dataset, then
simulates a coalescent tree in which each leaf is a seed individual and
migration is allowed across communities in the coalescent model at a
user-specified rate, and then evolves the sequence down the resulting tree under
a GTR+Gamma model to get seed sequences for each seed.
'''
from SeedSequence import SeedSequence
from SeedSequence_Virus import SeedSequence_Virus
from SequenceEvolution_GTRGammaSeqGen import SequenceEvolution_GTRGammaSeqGen
import FAVITES_GlobalContext as GC
import modules.FAVITES_ModuleFactory as MF
from subprocess import CalledProcessError,check_output,STDOUT
from os.path import expanduser
from os import chdir,makedirs

OUT_FOLDER = "seed_sequences"
class SeedSequence_CommunityVirusMigrationCoalescentGTRGamma(SeedSequence):
    def cite():
        return [GC.CITATION_HMMER, GC.CITATION_MSMS, GC.CITATION_SEQGEN]

    def init():
        GC.msms_path = expanduser(GC.msms_path.strip())
        assert MF.modules['ContactNetworkGenerator'].__name__ in GC.COMMUNITY_GENERATORS, "Must use a ContactNetworkGenerator that creates communities (%s)" % ', '.join(sorted(GC.COMMUNITY_GENERATORS))
        SeedSequence_Virus.init()
        SequenceEvolution_GTRGammaSeqGen.init()
        GC.community_seed_scaled_mutation_rate = float(GC.community_seed_scaled_mutation_rate)
        assert GC.community_seed_scaled_mutation_rate > 0, "community_seed_scaled_mutation_rate must be positive"
        assert isinstance(GC.community_seed_populations, list), "community_seed_populations must be a list of positive integers"
        for i in range(len(GC.community_seed_populations)):
            GC.community_seed_populations[i] = int(GC.community_seed_populations[i])
            assert GC.community_seed_populations[i] > 0, "community_seed_populations must be a list of positive integers"
        assert isinstance(GC.community_seed_migration_rates, dict), "community_seed_migration_rates must be a dictionary of dictionaries of floats"
        try:
            for i in range(len(GC.community_seed_populations)):
                for j in range(len(GC.community_seed_migration_rates)):
                    if i == j:
                        assert i not in GC.community_seed_migration_rates[i] or float(GC.community_seed_migration_rates[i][i]) == 0., "Non-zero self-migration rate found in community_seed_migration_rates"
                    else:
                        GC.community_seed_migration_rates[i][j] = float(GC.community_seed_migration_rates[i][j])
                        assert GC.community_seed_migration_rates[i][j] >= 0, "Migration rates in community_seed_migration_rates must be at least 0"
        except KeyError:
            assert False, "Malformed community_seed_migration_rates dictionary. See FAVITES Wiki for usage information"
        GC.check_seqgen_executable()

    def generate():
        if not hasattr(GC, "seed_sequences"):
            assert len(GC.community_seed_populations) == len(GC.cn_communities), "The length of community_seed_populations does not match the number of communities"
            seed_nodes_str = {n.get_name() for n in GC.seed_nodes}
            command = [GC.msms_path, str(len(GC.seed_nodes)), '1', '-T', '-t', str(GC.community_seed_scaled_mutation_rate), '-I', str(len(GC.cn_communities))]
            s = 0
            for c in GC.cn_communities:
                num = len([n for n in c if n in seed_nodes_str]); s += num
                command.append(str(num))
            assert s == len(GC.seed_nodes), "Number of seed nodes in communities unequal to total number of seed nodes"
            command.append('1')
            for i,n in enumerate(GC.community_seed_populations):
                command += ['-n', str(i), str(n)]
            command.append('-ma')
            for i in range(len(GC.community_seed_populations)):
                for j in range(len(GC.community_seed_migration_rates)):
                    if i == j:
                        command.append('x')
                    else:
                        command.append(str(GC.community_seed_migration_rates[i][j]))
            if GC.random_number_seed is not None:
                command += ['-seed', str(GC.random_number_seed)]
            try:
                treestr = check_output(command).decode().split('//')[1].split(';')[0].split(']')[1].strip() + ';'
            except CalledProcessError as e:
                chdir(GC.START_DIR)
                assert False, "msms failed to run: %s" % str(e)
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
            command = [GC.seqgen_path,'-or','-k1']
            if GC.random_number_seed is not None:
                command += ['-z%d'%GC.random_number_seed]
                GC.random_number_seed += 1
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
