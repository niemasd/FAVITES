#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Driver" module
'''
from Driver import Driver
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from os.path import expanduser
from os import getcwd
from os import makedirs
from os import chdir
from sys import stdout

class Driver_Default(Driver):
    def init():
        GC.out_dir = expanduser(GC.out_dir)

    def run():
        '''
        Simulation driver. Even if you add your own modules, you probably shouldn't
        need to modify this function. The one clear exception would be if your
        module requires additional user input (e.g. custom evolution model modules),
        which would then require you to call it with the required arguments.
        '''

        # load modules
        for module in MF.modules:
            MF.modules[module].init()
        LOG = MF.modules['Logging']

        # begin simulation
        LOG.writeln("\n========================   Simulation Process  ========================")
        LOG.writeln("Beginning simulation...")
        orig_dir = getcwd()
        LOG.write("Attempting to create the user-specified output directory: %r..." % GC.out_dir)
        try:
            makedirs(GC.out_dir)
            pass
        except:
            LOG.writeln("\nERROR: Unable to create the output directory. Perhaps it already exists?")
            exit(-1)
        chdir(GC.out_dir)
        makedirs("error_free_files")
        makedirs("error_free_files/phylogenetic_trees")
        makedirs("error_free_files/sequence_data")
        makedirs("error_prone_files")
        makedirs("error_prone_files/sequence_data")
        LOG.writeln(" done")

        # create ContactNetwork object from input contact network edge list
        LOG.write("Loading contact network edge list...")
        GC.cn_edge_list = MF.modules['ContactNetworkGenerator'].get_edge_list()
        LOG.writeln(" done")
        LOG.write("Creating ContactNetwork object...")
        contact_network = MF.modules['ContactNetwork'](GC.cn_edge_list)
        assert isinstance(contact_network, MF.module_abstract_classes['ContactNetwork']), "contact_network is not a ContactNetwork object"
        GC.contact_network = contact_network
        LOG.writeln(" done")

        # select seed nodes
        LOG.write("Selecting seed nodes...")
        GC.seed_nodes = MF.modules['SeedSelection'].select_seeds()
        assert isinstance(GC.seed_nodes, list), "seed_nodes is not a list"
        for node in GC.seed_nodes:
            assert isinstance(node, MF.module_abstract_classes['ContactNetworkNode']), "seed_nodes contains items that are not ContactNetworkNode objects"
        LOG.writeln(" done")

        # infect seed nodes
        LOG.write("Infecting seed nodes...")
        GC.root_viruses = []
        for i,node in enumerate(GC.seed_nodes):
            seq = MF.modules['SeedSequence'].generate()
            virus = MF.modules['TreeNode'](time=0.0, seq=seq, contact_network_node=node)
            GC.root_viruses.append(virus)
            node.infect(0.0,virus)
            GC.contact_network.add_to_infected(node)
        LOG.writeln(" done")

        # iterative step of transmissions
        LOG.write("Performing transmission simulations...")
        while True:
            t = MF.modules['TransmissionTimeSample'].sample_time()
            if t is None or MF.modules['EndCriteria'].done():
                break
            assert t >= GC.time, "Transmission cannot go back in time!"
            u,v = MF.modules['TransmissionNodeSample'].sample_nodes(t)
            if u is None or v is None or MF.modules['EndCriteria'].done():
                break
            GC.time = t
            MF.modules['NodeEvolution'].evolve_to_current_time(u)
            MF.modules['NodeEvolution'].evolve_to_current_time(v)
            virus = MF.modules['SourceSample'].sample_virus(u)
            u.remove_virus(virus)
            if not u.is_infected():
                GC.contact_network.remove_from_infected(u)
            v.infect(GC.time, virus)
            GC.contact_network.add_to_infected(v)
            GC.contact_network.add_transmission(u,v,GC.time)
        LOG.writeln(" done")

        # finalize global time
        LOG.write("Finalizing simulations...")
        MF.modules['EndCriteria'].finalize_time()
        nodes = [node for node in GC.contact_network.get_infected_nodes()]
        for node in nodes:
            MF.modules['NodeEvolution'].evolve_to_current_time(node, finalize=True)
            MF.modules['SequenceEvolution'].evolve_to_current_time(node)
        MF.modules['SequenceEvolution'].finalize() # in case the module creates all sequences at the end
        LOG.writeln(" done\n")

        # get leaves
        leaves = [[leaf for leaf in node.viruses()] for node in nodes]
        for l in leaves:
            for leaf in l:
                assert abs(leaf.get_time()-GC.time) < 0.0000000000001, "Encountered a tree with leaves not at end time!"

        # output error-free files
        LOG.writeln("\n========================   Simulation Output   ========================")

        # post-validation of transmission network
        LOG.write("Scoring final transmission network...")
        transmissions = GC.contact_network.get_transmissions()
        assert isinstance(transmissions, list), "get_transmissions() did not return a list!"
        for u,v,t in transmissions:
            assert isinstance(u, MF.module_abstract_classes['ContactNetworkNode']), "get_transmissions() contains an invalid transmission event"
            assert isinstance(v, MF.module_abstract_classes['ContactNetworkNode']), "get_transmissions() contains an invalid transmission event"
            assert isinstance(t, float), "get_transmissions() contains an invalid transmission event"
        score = str(MF.modules['PostValidation'].score_transmission_network())
        LOG.writeln(" done")
        LOG.writeln("Transmission network had a final score of: %s" % score)

        # write transmission network as edge list
        LOG.write("Writing true transmission network to file...")
        true_transmission_network = '\n'.join([("%s\t%s\t%d" % e) for e in transmissions])
        f = open('error_free_files/transmission_network.txt','w')
        for e in transmissions:
            f.write("%s\t%s\t%f\n" % e)
        f.close()
        f = open('error_free_files/transmission_network.gexf','w')
        f.write(GC.tn_favites2gexf(contact_network,transmissions))
        f.close()
        LOG.writeln(" done")
        LOG.writeln("True transmission network was written to: %s/error_free_files/transmission_network.txt" % GC.out_dir)
        LOG.writeln()

        # post-validation of phylogenetic trees
        LOG.writeln("Scoring final phylogenetic trees...")
        true_trees = [root.newick() for root in GC.root_viruses]
        scores = [0 for i in range(len(true_trees))]
        for i,tree in enumerate(true_trees):
            scores[i] = str(MF.modules['PostValidation'].score_phylogenetic_tree(tree))
            LOG.writeln("Phylogenetic tree %d had a final score of: %s" % (i,scores[i]))

        # write phylogenetic trees as Newick files
        LOG.write("Writing true phylogenetic trees to files...")
        for i,tree in enumerate(true_trees):
            f = open('error_free_files/phylogenetic_trees/tree_%d.tre' % i,'w')
            f.write(tree)
            f.close()
        LOG.writeln(" done")
        LOG.writeln("True phylogenetic trees were written to: %s/error_free_files/phylogenetic_trees/" % GC.out_dir)
        LOG.writeln()

        # post-validation of sequence data
        LOG.writeln("Scoring final sequence data...")
        seq_data = [[leaf.get_seq() for leaf in l] for l in leaves]
        for seqs in seq_data:
            for seq in seqs:
                assert seq is not None, "Encountered a leaf without a sequence!"
        scores = [0 for i in range(len(seq_data))]
        for i,seqs in enumerate(seq_data):
            scores[i] = str(MF.modules['PostValidation'].score_sequences(seqs))
            LOG.writeln("Sequence data from individual %r had a final score of: %s" % (nodes[i].get_name(),scores[i]))

        # write sequence data as FASTA files
        LOG.write("Writing true sequence data to files...")
        for i,seqs in enumerate(seq_data):
            f = open('error_free_files/sequence_data/seqs_%s.fasta' % nodes[i].get_name(), 'w')
            for j,seq in enumerate(seqs):
                f.write('>%s\n%s\n' % (leaves[i][j].get_label(),seq))
            f.close()
        LOG.writeln(" done")
        LOG.writeln("True sequence data were written to: %s/error_free_files/sequence_data/" % GC.out_dir)
        LOG.writeln()

        # introduce real data artifacts
        LOG.writeln("\n=======================   Real Data Artifacts   =======================")

        # subsample the contact network nodes
        LOG.write("Subsampling contact network nodes...")
        subsampled_nodes = MF.modules['NodeSample'].subsample_transmission_network()
        LOG.writeln(" done")

        # introduce sequencing error
        LOG.write("Simulating sequencing error...")
        for node in subsampled_nodes:
            MF.modules['Sequencing'].introduce_sequencing_error(node)
        LOG.writeln(" done")
        LOG.writeln("Error prone sequence data were written to: %s/error_prone_files/sequence_data/" % GC.out_dir)

        # return to original directory
        chdir(orig_dir)
        LOG.close()