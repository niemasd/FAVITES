#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Driver" module
'''
import modules.FAVITES_ModuleFactory as MF                       # for global access variables
import FAVITES_GlobalContext as GC
from Driver import Driver                         # Driver module abstract class
import os                                                 # to write output files
from sys import stdout                                    # to flush print buffer

class Driver_Default(Driver):
    def init():
        GC.out_dir = os.path.expanduser(GC.out_dir)

    def run():
        '''
        Simulation driver. Even if you add your own modules, you probably shouldn't
        need to modify this function. The one clear exception would be if your
        module requires additional user input (e.g. custom evolution model modules),
        which would then require you to call it with the required arguments.
        '''

        # begin simulation
        print("\n========================   Simulation Process  ========================")
        print("Initializing modules...", end='')
        for module in MF.modules:
            MF.modules[module].init()
        print(" done")
        print("Beginning simulations...")
        orig_dir = os.getcwd()
        print("Attempting to create the user-specified output directory: %r..." % GC.out_dir, end='')
        stdout.flush()
        try:
            os.makedirs(GC.out_dir)
            pass
        except:
            print("ERROR: Unable to create the output directory. Perhaps it already exists?")
            exit(-1)
        os.chdir(GC.out_dir)
        os.makedirs("error_free_files")
        os.makedirs("error_free_files/phylogenetic_trees")
        os.makedirs("error_free_files/sequence_data")
        os.makedirs("error_prone_files")
        os.makedirs("error_prone_files/sequence_data")
        print(" done")

        # create ContactNetwork object from input contact network edge list
        print("Loading contact network edge list...", end='')
        stdout.flush()
        edge_list = MF.modules['ContactNetworkGenerator'].get_edge_list()
        print(" done")
        print("Creating ContactNetwork object...", end='')
        contact_network = MF.modules['ContactNetwork'](edge_list)
        assert isinstance(contact_network, MF.module_abstract_classes['ContactNetwork']), "contact_network is not a ContactNetwork object"
        GC.contact_network = contact_network
        print(" done")

        # select seed nodes
        print("Selecting seed nodes...", end='')
        stdout.flush()
        seed_nodes,seed_times = MF.modules['SeedSelection'].select_seeds()
        assert isinstance(seed_nodes, list), "seed_nodes is not a list"
        for node in seed_nodes:
            assert isinstance(node, MF.module_abstract_classes['ContactNetworkNode']), "seed_nodes contains items that are not ContactNetworkNode objects"
        assert len(seed_nodes) == GC.num_seeds, "seed_nodes contains a different number of nodes than NumSeeds"
        print(" done")

        # infect seed nodes
        print("Infecting seed nodes...", end='')
        stdout.flush()
        GC.root_viruses = []
        for i,node in enumerate(seed_nodes):
            seq = MF.modules['SeedSequence'].generate()
            virus = MF.modules['TreeNode'](time=0.0, seq=seq, contact_network_node=node)
            GC.root_viruses.append(virus)
            node.infect(seed_times[i],virus)
            GC.contact_network.add_to_infected(node)
        print(" done")

        # iterative step of transmissions
        print("Performing transmission simulations...", end='')
        stdout.flush()
        while True:
            t = MF.modules['TransmissionTimeSample'].sample_time()
            assert t >= GC.time, "Transmission cannot go back in time!"
            GC.time = t
            if MF.modules['EndCriteria'].done():
                break
            u,v = MF.modules['TransmissionNodeSample'].sample_nodes(t)
            MF.modules['NodeEvolution'].evolve_to_current_time(u)
            virus = MF.modules['SourceSample'].sample_virus(u)
            u.remove_virus(virus)
            v.infect(GC.time, virus)
            GC.contact_network.add_to_infected(v)
            GC.contact_network.add_transmission(u,v,t)
        print(" done")

        # finalize global time
        print("Finalizing simulations...", end='')
        stdout.flush()
        MF.modules['EndCriteria'].finalize_time()
        nodes = [node for node in GC.contact_network.get_infected_nodes()]
        for node in nodes:
            MF.modules['NodeEvolution'].evolve_to_current_time(node, finalize=True)
            MF.modules['SequenceEvolution'].evolve_to_current_time(node)
        MF.modules['SequenceEvolution'].finalize() # in case the module creates all sequences at the end
        print(" done\n")

        # get leaves
        leaves = [[leaf for leaf in node.viruses()] for node in nodes]
        for l in leaves:
            for leaf in l:
                assert abs(leaf.get_time()-GC.time) < 0.0000000000001, "Encountered a tree with leaves not at end time!"

        # output error-free files
        print("\n========================   Simulation Output   ========================")

        # post-validation of transmission network
        print("Scoring final transmission network...", end='')
        stdout.flush()
        transmissions = GC.contact_network.get_transmissions()
        assert isinstance(transmissions, list), "get_transmissions() did not return a list!"
        for u,v,t in transmissions:
            assert isinstance(u, MF.module_abstract_classes['ContactNetworkNode']), "get_transmissions() contains an invalid transmission event"
            assert isinstance(v, MF.module_abstract_classes['ContactNetworkNode']), "get_transmissions() contains an invalid transmission event"
            assert isinstance(t, float), "get_transmissions() contains an invalid transmission event"
        score = str(MF.modules['PostValidation'].score_transmission_network())
        print(" done")
        print("Transmission network had a final score of: %s" % score)

        # write transmission network as edge list
        print("Writing true transmission network to file...", end='')
        stdout.flush()
        true_transmission_network = '\n'.join([("%s\t%s\t%d" % e) for e in transmissions])
        f = open('error_free_files/transmission_network.txt','w')
        for e in transmissions:
            f.write("%s\t%s\t%d\n" % e)
        f.close()
        print(" done")
        print("True transmission network was written to: %s/error_free_files/transmission_network.txt" % GC.out_dir)
        print()

        # post-validation of phylogenetic trees
        print("Scoring final phylogenetic trees...")
        stdout.flush()
        true_trees = [root.newick() for root in GC.root_viruses]
        scores = [0 for i in range(len(true_trees))]
        for i,tree in enumerate(true_trees):
            scores[i] = str(MF.modules['PostValidation'].score_phylogenetic_tree(tree))
            print("Phylogenetic tree %d had a final score of: %s" % (i,scores[i]))

        # write phylogenetic trees as Newick files
        print("Writing true phylogenetic trees to files...", end='')
        stdout.flush()
        for i,tree in enumerate(true_trees):
            f = open('error_free_files/phylogenetic_trees/tree_%d.tre' % i,'w')
            f.write(tree)
            f.close()
        print(" done")
        print("True phylogenetic trees were written to: %s/error_free_files/phylogenetic_trees/" % GC.out_dir)
        print()

        # post-validation of sequence data
        print("Scoring final sequence data...")
        stdout.flush()
        seq_data = [[leaf.get_seq() for leaf in l] for l in leaves]
        for seqs in seq_data:
            for seq in seqs:
                assert seq is not None, "Encountered a leaf without a sequence!"
        scores = [0 for i in range(len(seq_data))]
        for i,seqs in enumerate(seq_data):
            scores[i] = str(MF.modules['PostValidation'].score_sequences(seqs))
            print("Sequence data from individual %r had a final score of: %s" % (nodes[i].get_name(),scores[i]))

        # write sequence data as FASTA files
        print("Writing true sequence data to files...", end='')
        stdout.flush()
        for i,seqs in enumerate(seq_data):
            f = open('error_free_files/sequence_data/seqs_%s.fasta' % nodes[i].get_name(), 'w')
            for j,seq in enumerate(seqs):
                f.write('>%s\n%s\n' % (leaves[i][j].get_label(),seq))
            f.close()
        print(" done")
        print("True sequence data were written to: %s/error_free_files/sequence_data/" % GC.out_dir)
        print()

        # introduce real data artifacts
        print("\n=======================   Real Data Artifacts   =======================")

        # subsample the transmission network
        print("Subsampling transmission network...", end='')
        subsampled_transmissions = MF.modules['NodeSample'].subsample_transmission_network()
        for node in subsampled_transmissions:
            assert isinstance(u, MF.module_abstract_classes['ContactNetworkNode']), "subsample_transmission_network() contains an invalid transmission event"
            assert isinstance(v, MF.module_abstract_classes['ContactNetworkNode']), "subsample_transmission_network() contains an invalid transmission event"
            assert isinstance(t, float), "subsample_transmission_network() contains an invalid transmission event"
        print(" done")
        print("Writing subsampled transmission network to file...", end='')
        stdout.flush()
        subsampled_transmission_network = '\n'.join([("%s\t%s\t%d" % e) for e in subsampled_transmissions])
        f = open('error_prone_files/transmission_network.txt','w')
        for e in subsampled_transmissions:
            f.write("%s\t%s\t%d\n" % e)
        f.close()
        print(" done")
        print("Subsampled transmission network was written to: %s/error_prone_files/transmission_network.txt" % GC.out_dir)

        # introduce sequencing error
        print("Introducing sequence data sampling error...",end='')
        subsampled_nodes = set()
        for u,v,t in subsampled_transmissions:
            subsampled_nodes.add(u)
            subsampled_nodes.add(v)
        for i,node in enumerate(subsampled_nodes):
            MF.modules['Sequencing'].introduce_sequencing_error(node)
        print(" done")
        print("Error prone sequence data were written to: %s/error_prone_files/sequence_data/" % GC.out_dir)

        # return to original directory
        os.chdir(orig_dir)