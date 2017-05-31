#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Driver" module
'''
from Driver import Driver
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from os.path import expanduser
from os import getcwd,makedirs,chdir
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

        # store starting directory
        GC.START_DIR = getcwd()

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
            if u == v: # u = v implies uninfection (recovery or death)
                u.uninfect()
                GC.contact_network.add_transmission(u,u,GC.time)
                continue
            MF.modules['NodeEvolution'].evolve_to_current_time(u)
            MF.modules['NodeEvolution'].evolve_to_current_time(v)
            virus = MF.modules['SourceSample'].sample_virus(u)
            u.remove_virus(virus)
            if not u.is_infected():
                GC.contact_network.remove_from_infected(u)
            v.infect(GC.time, virus)
            GC.contact_network.add_to_infected(v)
            GC.contact_network.add_transmission(u,v,GC.time)
        GC.transmissions = GC.contact_network.get_transmissions()
        assert isinstance(GC.transmissions, list), "get_transmissions() did not return a list!"
        LOG.writeln(" done")

        # finalize global time
        LOG.write("Finalizing transmission and evolution simulations...")
        MF.modules['EndCriteria'].finalize_time()
        nodes = [node for node in GC.contact_network.get_infected_nodes()]
        for node in nodes:
            MF.modules['NodeEvolution'].evolve_to_current_time(node, finalize=True)
            MF.modules['SequenceEvolution'].evolve_to_current_time(node)

        # perform patient sampling in time (on all infected nodes; will subsample from this later)
        GC.cn_sample_times = {}
        GC.sampled_trees = set()
        for node in GC.contact_network.nodes_iter():
            num_times = MF.modules['NumTimeSample'].sample_num_times(node)
            assert num_times >= 0, "Encountered negative number of sampling events"
            times = MF.modules['TimeSample'].sample_times(node, num_times)
            for t in times:
                assert t <= GC.time, "Encountered a patient sampling time larger than the global end time"
            GC.cn_sample_times[node] = times
            if len(times) != 0:
                for leaf in node.viruses():
                    GC.sampled_trees.add(leaf.get_root())
        GC.sampled_trees = list(GC.sampled_trees)
        GC.prune_sampled_trees()
        LOG.writeln(" done")

        # finalize sequence data
        LOG.write("Finalizing sequence simulations...")
        MF.modules['SequenceEvolution'].finalize() # in case the module creates all sequences at the end
        LOG.writeln(" done\n")

        # output error-free files
        LOG.writeln("\n========================   Simulation Output   ========================")

        # post-validation of transmission network
        LOG.write("Scoring final transmission network...")
        for u,v,t in GC.transmissions:
            assert isinstance(u, MF.module_abstract_classes['ContactNetworkNode']), "get_transmissions() contains an invalid transmission event"
            assert isinstance(v, MF.module_abstract_classes['ContactNetworkNode']), "get_transmissions() contains an invalid transmission event"
            assert isinstance(t, float), "get_transmissions() contains an invalid transmission event"
        score = str(MF.modules['PostValidation'].score_transmission_network())
        LOG.writeln(" done")
        LOG.writeln("Transmission network had a final score of: %s" % score)

        # write transmission network as edge list
        LOG.write("Writing true transmission network to file...")
        true_transmission_network = '\n'.join([("%s\t%s\t%d" % e) for e in GC.transmissions])
        f = open('error_free_files/transmission_network.txt','w')
        for e in GC.transmissions:
            f.write("%s\t%s\t%f\n" % e)
        f.close()
        f = open('error_free_files/transmission_network.gexf','w')
        f.write(GC.tn_favites2gexf(contact_network,GC.transmissions))
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
        leaves = GC.get_leaves(GC.sampled_trees) # returns dictionary where keys are CN nodes and values are set of tree leaves
        for cn_node in leaves:
            seqs = [leaf.get_seq() for leaf in leaves[cn_node]]
            for seq in seqs:
                assert seq is not None, "Encountered a leaf without a sequence!"
            score = str(MF.modules['PostValidation'].score_sequences(seqs))
            LOG.writeln("Sequence data from individual %r had a final score of: %s" % (cn_node.get_name(),score))

        # write sequence data as FASTA files
        LOG.write("Writing true sequence data to files...")
        for cn_node in sorted(leaves.keys()):
            times = {}
            for leaf in leaves[cn_node]:
                t = leaf.get_time()
                if t not in times:
                    times[t] = {leaf}
                else:
                    times[t].add(leaf)
            for t in times:
                f = open('error_free_files/sequence_data/seqs_n%s_t%f.fasta' % (cn_node.get_name(),t), 'w')
                for leaf in times[t]:
                    f.write('>%s\n%s\n' % (str(leaf),leaf.get_seq()))
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