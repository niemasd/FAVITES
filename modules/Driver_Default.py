#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Driver" module
'''
from Driver import Driver
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from datetime import datetime
from os.path import expanduser
from os import environ,getcwd,makedirs,chdir
from sys import stderr

def printMessage(LOG):
    '''
    Print author message
    '''
    LOG.writeln("/---------------------------------------------------------------------\\")
    LOG.writeln("| FAVITES - FrAmework for VIral Transmission and Evolution Simulation |")
    LOG.writeln("|                        Moshiri & Mirarab 2016                       |")
    LOG.writeln("\\---------------------------------------------------------------------/\n")

class Driver_Default(Driver):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        GC.out_dir = expanduser(GC.out_dir)
        print(GC.VERBOSE)
        print(GC.OUT_DIR_PRINT)
        if not hasattr(GC,'OUT_DIR_PRINT'):
            GC.OUT_DIR_PRINT = GC.out_dir
        GC.virus_history = {} # key: virus label; value: list of (time,cn_node) tuples representing the time virus was in cn_node

    def run():
        '''
        Simulation driver. Even if you add your own modules, you probably shouldn't
        need to modify this function. The one clear exception would be if your
        module requires additional user input (e.g. custom evolution model modules),
        which would then require you to call it with the required arguments.
        '''

        # store starting directory
        if GC.VERBOSE:
            print('[%s] FAVITES Driver starting' % datetime.now(), file=stderr)
        GC.START_DIR = getcwd()

        # load modules
        for module in MF.modules:
            MF.modules[module].init()
        LOG = MF.modules['Logging']
        printMessage(LOG)

        # begin simulation
        LOG.writeln("\n========================   Simulation Process  ========================")
        LOG.writeln("Beginning simulation...")
        if GC.VERBOSE:
            print('[%s] Starting simulation' % datetime.now(), file=stderr)
        orig_dir = getcwd()
        LOG.write("Attempting to create the user-specified output directory: %r..." % GC.OUT_DIR_PRINT)
        try:
            makedirs(GC.out_dir)
            pass
        except:
            if 'FAVITES_DOCKER' not in environ: # bypass error (Docker makes the folder automatically)
                LOG.writeln("\nERROR: Unable to create the output directory. Perhaps it already exists?")
                if GC.VERBOSE:
                    print('[%s] Output directory exists: %s' % (datetime.now(), GC.OUT_DIR_PRINT), file=stderr)
                exit(-1)
        if GC.VERBOSE:
            print('[%s] Output directory: %s' % (datetime.now(), GC.OUT_DIR_PRINT), file=stderr)
        chdir(GC.out_dir)
        makedirs("error_free_files")
        makedirs("error_free_files/phylogenetic_trees")
        makedirs("error_free_files/sequence_data")
        makedirs("error_prone_files")
        makedirs("error_prone_files/sequence_data")
        LOG.writeln(" done")

        # create ContactNetwork object from input contact network edge list
        LOG.write("Loading contact network edge list...")
        if GC.VERBOSE:
            print('[%s] Loading contact network' % datetime.now(), file=stderr)
        GC.cn_edge_list = MF.modules['ContactNetworkGenerator'].get_edge_list()
        LOG.writeln(" done")
        LOG.write("Creating ContactNetwork object...")
        if GC.VERBOSE:
            print('[%s] Initializing ContactNetwork object...' % datetime.now(), file=stderr)
        contact_network = MF.modules['ContactNetwork'](GC.cn_edge_list)
        assert isinstance(contact_network, MF.module_abstract_classes['ContactNetwork']), "contact_network is not a ContactNetwork object"
        GC.contact_network = contact_network
        LOG.writeln(" done")

        # select seed nodes
        LOG.write("Selecting seed nodes...")
        if GC.VERBOSE:
            print('[%s] Selecting seed nodes' % datetime.now(), file=stderr)
        GC.seed_nodes = MF.modules['SeedSelection'].select_seeds()
        assert isinstance(GC.seed_nodes, list) or isinstance(GC.seed_nodes, set), "seed_nodes is not a list nor a set"
        for node in GC.seed_nodes:
            if GC.VERBOSE:
                print('[%s] Seed\tTime 0\tNode %s' % (datetime.now(), str(node)), file=stderr)
            assert isinstance(node, MF.module_abstract_classes['ContactNetworkNode']), "seed_nodes contains items that are not ContactNetworkNode objects"
        LOG.writeln(" done")

        # infect seed nodes
        LOG.write("Infecting seed nodes...")
        if GC.VERBOSE:
            print('[%s] Infecting seed nodes' % datetime.now(), file=stderr)
        GC.root_viruses = []
        for node in GC.seed_nodes:
            seq = MF.modules['SeedSequence'].generate()
            virus = MF.modules['TreeNode'](time=0.0, seq=seq, contact_network_node=node)
            GC.root_viruses.append(virus)
            node.infect(0.0,virus)
            GC.contact_network.add_transmission(None,node,0.0)
        LOG.writeln(" done")

        # iterative step of transmissions
        LOG.write("Performing transmission simulations...")
        if GC.VERBOSE:
            print('[%s] Performing transmission iterations' % datetime.now(), file=stderr)
        while True:
            t = MF.modules['TransmissionTimeSample'].sample_time()
            if t is None or MF.modules['EndCriteria'].done():
                break
            assert t >= GC.time, "Transmission cannot go back in time!"
            u,v = MF.modules['TransmissionNodeSample'].sample_nodes(t)
            if (u is None and v is None) or MF.modules['EndCriteria'].done():
                break
            GC.time = t
            if u == v: # u = v implies uninfection (recovery or death)
                u.uninfect()
                GC.contact_network.add_transmission(u,u,GC.time)
                continue
            elif u is None: # u = None implies seed infection at time t > 0
                seq = MF.modules['SeedSequence'].generate()
                virus = MF.modules['TreeNode'](time=GC.time, seq=seq, contact_network_node=v)
                GC.root_viruses.append(virus)
                v.infect(GC.time,virus)
                GC.contact_network.add_transmission(None,v,GC.time)
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
        if GC.VERBOSE:
            print('[%s] Finalizing transmissions/evolution' % datetime.now(), file=stderr)
        MF.modules['EndCriteria'].finalize_time()
        nodes = [node for node in GC.contact_network.get_infected_nodes()]
        for node in nodes:
            MF.modules['NodeEvolution'].evolve_to_current_time(node, finalize=True)
            MF.modules['SequenceEvolution'].evolve_to_current_time(node)

        # perform patient sampling in time (on all infected nodes; will subsample from this later)
        GC.cn_sample_times = {}
        if GC.VERBOSE:
            print('[%s] Performing person sampling (sequencing)' % datetime.now(), file=stderr)
        for node in GC.contact_network.nodes_iter():
            num_times = MF.modules['NumTimeSample'].sample_num_times(node)
            assert num_times >= 0, "Encountered negative number of sampling events"
            times = MF.modules['TimeSample'].sample_times(node, num_times)
            for t in times:
                assert t <= GC.time, "Encountered a patient sampling time larger than the global end time"
            if len(times) != 0:
                GC.cn_sample_times[node] = times
                if GC.VERBOSE:
                    print('[%s] Node %s sampled at times %s' % (datetime.now(),str(node),str(times)), file=stderr)
            elif GC.VERBOSE:
                print('[%s] Node %s not sampled' % (datetime.now(),str(node)), file=stderr)
        if GC.VERBOSE:
            print('[%s] Pruning sampled trees' % datetime.now(), file=stderr)
        GC.prune_sampled_trees()
        pruned_newick_trees_time = [(root,root.newick()) for root in GC.sampled_trees]

        # convert trees from unit of time to unit of mutation rate
        if GC.VERBOSE:
            print('[%s] Converting sampled trees from time to mutation rate' % datetime.now(), file=stderr)
        GC.pruned_newick_trees = [(root,MF.modules['TreeUnit'].time_to_mutation_rate(treestr_time)) for root,treestr_time in pruned_newick_trees_time]
        LOG.writeln(" done")

        # finalize sequence data
        LOG.write("Finalizing sequence simulations...")
        if GC.VERBOSE:
            print('[%s] Finalizing sequences' % datetime.now(), file=stderr)
        MF.modules['SequenceEvolution'].finalize() # in case the module creates all sequences at the end
        LOG.writeln(" done\n")

        # output error-free files
        LOG.writeln("\n========================   Simulation Output   ========================")

        # post-validation of transmission network
        LOG.write("Scoring final transmission network...")
        for u,v,t in GC.transmissions:
            assert u is None or isinstance(u, MF.module_abstract_classes['ContactNetworkNode']), "get_transmissions() contains an invalid transmission event"
            assert isinstance(v, MF.module_abstract_classes['ContactNetworkNode']), "get_transmissions() contains an invalid transmission event"
            assert isinstance(t, float), "get_transmissions() contains an invalid transmission event"
        score = str(MF.modules['PostValidation'].score_transmission_network())
        LOG.writeln(" done")
        LOG.writeln("Transmission network had a final score of: %s" % score)
        if GC.VERBOSE:
            print('[%s] Transmission network score: %s' % (datetime.now(),score), file=stderr)

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
        LOG.writeln("True transmission network was written to: %s/error_free_files/transmission_network.txt" % GC.OUT_DIR_PRINT)
        LOG.writeln()
        if GC.VERBOSE:
            print('[%s] Wrote transmission network to file' % datetime.now(), file=stderr)

        # post-validation of phylogenetic trees
        LOG.writeln("Scoring final phylogenetic trees...")
        scores = [0 for i in range(len(GC.sampled_trees))]
        for i,e in enumerate(GC.pruned_newick_trees):
            scores[i] = str(MF.modules['PostValidation'].score_phylogenetic_tree(e[1]))
            LOG.writeln("Phylogenetic tree %d had a final score of: %s" % (i,scores[i]))
            if GC.VERBOSE:
                print('[%s] Phylogenetic tree %d score: %s' % (datetime.now(),i,scores[i]), file=stderr)

        # write phylogenetic trees as Newick files
        LOG.write("Writing true phylogenetic trees to files...")
        for i,e in enumerate(GC.pruned_newick_trees):
            f = open('error_free_files/phylogenetic_trees/tree_%d.tre' % i,'w')
            f.write(e[1])
            f.close()
        LOG.writeln(" done")
        LOG.writeln("True phylogenetic trees were written to: %s/error_free_files/phylogenetic_trees/" % GC.OUT_DIR_PRINT)
        LOG.writeln()
        if GC.VERBOSE:
            print('[%s] Wrote phylogenetic trees' % datetime.now(), file=stderr)

        # post-validation of sequence data
        LOG.writeln("Scoring final sequence data...")
        leaves = GC.get_leaves(GC.sampled_trees) # returns dictionary where keys are CN nodes and values are set of tree leaves
        for cn_node in leaves:
            seqs = [leaf.get_seq() for leaf in leaves[cn_node]]
            for seq in seqs:
                assert seq is not None, "Encountered a leaf without a sequence!"
            score = str(MF.modules['PostValidation'].score_sequences(seqs))
            LOG.writeln("Sequence data from individual %r had a final score of: %s" % (cn_node.get_name(),score))
            if GC.VERBOSE:
                print('[%s] Sequence data from Node %s score: %s' % (datetime.now(),str(cn_node),score), file=stderr)

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
        LOG.writeln("True sequence data were written to: %s/error_free_files/sequence_data/" % GC.OUT_DIR_PRINT)
        LOG.writeln()
        if GC.VERBOSE:
            print('[%s] Wrote true sequence data' % datetime.now(), file=stderr)

        # introduce real data artifacts
        LOG.writeln("\n=======================   Real Data Artifacts   =======================")

        # subsample the contact network nodes
        LOG.write("Subsampling contact network nodes...")
        if GC.VERBOSE:
            print('[%s] Subsampling contact network nodes' % datetime.now(), file=stderr)
        subsampled_nodes = MF.modules['NodeAvailability'].subsample_transmission_network()
        LOG.writeln(" done")

        # introduce sequencing error
        LOG.write("Simulating sequencing error...")
        for node in subsampled_nodes:
            if GC.VERBOSE:
                print('[%s] Sequencing error for Node %s' % (datetime.now(),str(node)), file=stderr)
            MF.modules['Sequencing'].introduce_sequencing_error(node)
        LOG.writeln(" done")
        LOG.writeln("Error prone sequence data were written to: %s/error_prone_files/sequence_data/" % GC.OUT_DIR_PRINT)
        LOG.writeln()

        # return to original directory and finish
        chdir(orig_dir)
        if GC.VERBOSE:
            print('[%s] Outputting list of citations' % datetime.now(), file=stderr)
        LOG.writeln("\n============================   Citations   ============================")
        citations = {MF.modules[module].cite().strip() for module in MF.modules if MF.modules[module].cite() is not None and len(MF.modules[module].cite().strip()) != 0}
        for citation in sorted(citations):
            LOG.writeln(citation)
        LOG.close()
        if GC.VERBOSE:
            print('[%s] FAVITES Driver finished' % datetime.now(), file=stderr)