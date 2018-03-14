#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Driver" module
'''
from Driver import Driver
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from datetime import datetime
from gzip import open as gopen
from os.path import abspath,expanduser,isdir,join,getsize
from os import chdir,environ,getcwd,makedirs,rename,walk
from sys import stderr
from time import time

def printMessage(LOG):
    '''
    Print author message
    '''
    title = "FAVITES - FrAmework for VIral Transmission and Evolution Simulation"
    version = "Version %s" % GC.FAVITES_VERSION
    devel = "Niema Moshiri 2017"
    l = max(len(title),len(version),len(devel))
    LOG.writeln("/-%s-\\" % ('-'*l))
    for e in (title,version,devel):
        lpad = int((l-len(e))/2)
        rpad = l - lpad - len(e)
        LOG.writeln("| %s%s%s |" % (lpad*' ',e,rpad*' '))
    LOG.writeln("\\-%s-/\n" % ('-'*l))

class Driver_Default(Driver):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        GC.out_dir = abspath(expanduser(GC.out_dir))
        GC.virus_history = {} # key: virus label; value: list of (time,cn_node) tuples representing the time virus was in cn_node
        GC.PRUNE_TREES = True # by default, we should prune the final trees
        if isinstance(GC.random_number_seed, str):
            GC.random_number_seed = GC.random_number_seed.strip()
            if GC.random_number_seed == "":
                GC.random_number_seed = None
        assert GC.random_number_seed is None or (isinstance(GC.random_number_seed, int) and GC.random_number_seed >= 0), "random_number_seed must be an integer >= 0"
        if isinstance(GC.random_number_seed, int):
            from random import seed as python_random_seed
            python_random_seed(GC.random_number_seed)
        else:
            GC.NUMPY_SEEDED = True # to make sure Numpy doesn't get seeded later

    def run(path, ORIG_CONFIG):
        '''
        Simulation driver. Even if you add your own modules, you probably shouldn't
        need to modify this function. The one clear exception would be if your
        module requires additional user input (e.g. custom evolution model modules),
        which would then require you to call it with the required arguments.
        '''

        # store starting directory
        GC.FAVITES_START_TIME = time()
        GC.FAVITES_DIR = path
        if GC.VERBOSE:
            print('[%s] FAVITES Driver starting' % datetime.now(), file=stderr)
        GC.START_DIR = getcwd()

        # load modules
        for module in MF.modules:
            MF.modules[module].init()
        LOG = MF.modules['Logging']

        # set up environment
        orig_dir = getcwd()
        try:
            makedirs(GC.out_dir)
        except:
            if 'FAVITES_DOCKER' not in environ: # bypass error (Docker makes the folder automatically)
                if isdir(abspath(expanduser(GC.out_dir))):
                    if GC.VERBOSE:
                        print('[%s] Output directory exists: %s' % (datetime.now(), environ['out_dir_print']), file=stderr)
                    response = 'x'
                    while len(response) == 0 or response[0] not in {'y','n'}:
                        response = input("ERROR: Output directory exists. Overwrite? All contents will be deleted. (y/n)").strip().lower()
                    if response[0] == 'y':
                        from shutil import rmtree
                        rmtree(GC.out_dir); makedirs(GC.out_dir)
                    else:
                        exit(-1)
                else:
                    LOG.writeln("ERROR: Unable to create the output directory")
                    exit(-1)
        chdir(GC.out_dir)
        f = open('CONFIG.json','w')
        f.write(ORIG_CONFIG)
        f.close()

        # begin simulation
        printMessage(LOG)
        LOG.writeln("========================   Simulation Process  ========================")
        if GC.VERBOSE:
            print('[%s] Starting simulation' % datetime.now(), file=stderr)
        makedirs("error_free_files", exist_ok=True)
        makedirs("error_free_files/phylogenetic_trees", exist_ok=True)
        makedirs("error_prone_files", exist_ok=True)

        # create ContactNetwork object
        LOG.write("Loading contact network...")
        if GC.VERBOSE:
            print('[%s] Loading contact network' % datetime.now(), file=stderr)
        GC.cn_edge_list = MF.modules['ContactNetworkGenerator'].get_edge_list()
        LOG.writeln(" done")
        LOG.write("Creating ContactNetwork object...")
        if GC.VERBOSE:
            print('[%s] Initializing ContactNetwork object...' % datetime.now(), file=stderr)
        contact_network = MF.modules['ContactNetwork'](GC.cn_edge_list)
        assert isinstance(contact_network, MF.module_abstract_classes['ContactNetwork']), "contact_network is not a ContactNetwork object"
        assert contact_network.num_nodes() > 1, "ContactNetwork must have at least 2 nodes"
        assert contact_network.num_edges() > 0, "ContactNetwork must have at least 1 edge"
        MF.modules['TransmissionNodeSample'].check_contact_network(contact_network)
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
        GC.seed_to_first_virus = {}
        f = gopen('seed_sequences.tsv.gz','wb',9)
        for node in GC.seed_nodes:
            seq = MF.modules['SeedSequence'].generate()
            virus = MF.modules['TreeNode'](time=0.0, seq=seq, contact_network_node=node)
            f.write(('%s\t%s\n' % (virus.get_label(),seq)).encode())
            GC.root_viruses.append(virus)
            node.infect(0.0,virus)
            GC.contact_network.add_transmission(None,node,0.0)
            GC.seed_to_first_virus[node] = virus
        f.write(b'\n'); f.close()
        if isdir('seed_sequences'):
            rename('seed_sequences.tsv.gz','seed_sequences/seed_sequences.tsv.gz')
        LOG.writeln(" done")

        # iterative step of transmissions
        LOG.write("Performing transmission simulations...")
        if GC.VERBOSE:
            print('[%s] Performing transmission iterations' % datetime.now(), file=stderr)
        GC.first_time_transmitting = {}
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
                GC.seed_to_first_virus[v] = virus
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
            if u not in GC.first_time_transmitting:
                GC.first_time_transmitting[u] = GC.time
        GC.transmissions = GC.contact_network.get_transmissions()
        assert isinstance(GC.transmissions, list), "get_transmissions() did not return a list!"
        LOG.writeln(" done")

        # finalize global time
        LOG.write("Finalizing transmission simulations...")
        if GC.VERBOSE:
            print('[%s] Finalizing transmissions/evolution' % datetime.now(), file=stderr)
        MF.modules['EndCriteria'].finalize_time()
        LOG.writeln(" done")

        # write transmission network as edge list
        LOG.write("Writing true transmission network to file...")
        f = gopen('error_free_files/transmission_network.txt.gz','wb',9)
        for e in GC.transmissions:
            f.write(("%s\t%s\t%f\n" % e).encode())
        f.write(b'\n'); f.close()
        LOG.writeln(" done")
        LOG.writeln("True transmission network was written to: %s/error_free_files/transmission_network.txt" % environ['out_dir_print'])
        if GC.VERBOSE:
            print('[%s] Wrote transmission network to file' % datetime.now(), file=stderr)

        # perform patient sampling in time (on all infected nodes; will subsample from this later)
        LOG.write("Sampling patients in time...")
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
        LOG.writeln(" done")

        # evolve to end time
        LOG.write("Evolving trees and sequences to end time...")
        nodes = [node for node in GC.contact_network.get_infected_nodes()]
        for node in nodes:
            MF.modules['NodeEvolution'].evolve_to_current_time(node, finalize=True)
            MF.modules['SequenceEvolution'].evolve_to_current_time(node)
        LOG.writeln(" done")

        # prune sampled trees
        LOG.write("Pruning sampled trees...")
        if GC.PRUNE_TREES:
            if GC.VERBOSE:
                print('[%s] Pruning sampled trees' % datetime.now(), file=stderr)
            GC.prune_sampled_trees()
        GC.pruned_newick_trees_time = [e for e in GC.sampled_trees] # (rootvirus,treestr) tuples
        LOG.writeln(" done")

        # write phylogenetic trees (time) as Newick files
        LOG.write("Writing true phylogenetic trees (time) to files...")
        for i,e in enumerate(GC.pruned_newick_trees_time):
            f = gopen('error_free_files/phylogenetic_trees/tree_%d.time.tre.gz' % i,'wb',9)
            f.write(e[1].encode()); f.write(b'\n')
            f.close()
        LOG.writeln(" done")
        LOG.writeln("True phylogenetic trees (time) were written to: %s/error_free_files/phylogenetic_trees/" % environ['out_dir_print'])
        if GC.VERBOSE:
            print('[%s] Wrote phylogenetic trees (time)' % datetime.now(), file=stderr)

        # convert trees from unit of time to unit of mutation rate
        LOG.write("Converting trees from time to mutation rate...")
        if GC.VERBOSE:
            print('[%s] Converting sampled trees from time to mutation rate' % datetime.now(), file=stderr)
        GC.pruned_newick_trees = [(e[0],MF.modules['TreeUnit'].time_to_mutation_rate(e[1])) for e in GC.pruned_newick_trees_time]
        LOG.writeln(" done")

        # write phylogenetic trees (expected number of mutations) as Newick files
        LOG.write("Writing true phylogenetic trees (expected number of mutations) to files...")
        GC.final_tree_to_root_seq = []
        for i,e in enumerate(GC.pruned_newick_trees):
            f = gopen('error_free_files/phylogenetic_trees/tree_%d.tre.gz' % i,'wb',9)
            f.write(e[1].encode()); f.write(b'\n')
            f.close()
            GC.final_tree_to_root_seq.append(e[0].get_seq())
        LOG.writeln(" done")
        LOG.writeln("True phylogenetic trees (expected number of mutations) were written to: %s/error_free_files/phylogenetic_trees/" % environ['out_dir_print'])
        if GC.VERBOSE:
            print('[%s] Wrote phylogenetic trees (expected number of mutations)' % datetime.now(), file=stderr)

        # merge cluster trees with seed tree (if applicable)
        LOG.write("Merging true cluster phylogenetic trees with true seed tree (if applicable)...")
        GC.merged_trees,GC.merged_trees_time = MF.modules['SeedSequence'].merge_trees()
        for i in range(len(GC.merged_trees)):
            f = gopen('error_free_files/phylogenetic_trees/merged_tree_%d.tre.gz' % i,'wb',9)
            f.write(GC.merged_trees[i].encode()); f.write(b'\n')
            f.close()
            f = gopen('error_free_files/phylogenetic_trees/merged_tree_%d.time.tre.gz' % i,'wb',9)
            f.write(GC.merged_trees_time[i].encode()); f.write(b'\n')
            f.close()
        LOG.writeln(" done")
        if GC.VERBOSE:
            print('[%s] Merged cluster trees with seed tree (if applicable)' % datetime.now(), file=stderr)

        # finalize sequence data
        LOG.write("Finalizing sequence simulations...")
        if GC.VERBOSE:
            print('[%s] Finalizing sequences' % datetime.now(), file=stderr)
        MF.modules['SequenceEvolution'].finalize() # in case the module creates all sequences at the end
        LOG.writeln(" done")

        # write error-free sequence data
        LOG.writeln("Writing final sequence data to file...")
        f = gopen('error_free_files/sequence_data.fasta.gz','wb',9)
        for cn_label in GC.final_sequences:
            for t in GC.final_sequences[cn_label]:
                for l,s in GC.final_sequences[cn_label][t]:
                    f.write((">%s\n%s\n" % (l,s)).encode())
        f.write(b'\n'); f.close()
        LOG.writeln("True sequence data were written to: %s/error_free_files" % environ['out_dir_print'])
        LOG.writeln()
        if GC.VERBOSE:
            print('[%s] Wrote true sequence data' % datetime.now(), file=stderr)

        # introduce real data artifacts
        LOG.writeln("\n=======================   Real Data Artifacts   =======================")

        # subsample the contact network nodes and write sequences to file
        LOG.write("Subsampling contact network nodes...")
        if GC.VERBOSE:
            print('[%s] Subsampling contact network nodes' % datetime.now(), file=stderr)
        GC.subsampled_nodes = MF.modules['NodeAvailability'].subsample_transmission_network()
        if len(GC.subsampled_nodes) != 0:
            f = gopen('error_prone_files/sequence_data_subsampled_errorfree.fasta.gz','wb',9)
            for node in GC.subsampled_nodes:
                cn_label = node.get_name()
                for t in GC.final_sequences[cn_label]:
                    for l,s in GC.final_sequences[cn_label][t]:
                        f.write((">%s\n%s\n" % (l,s)).encode())
            f.write(b'\n'); f.close()
            LOG.writeln(" done")

        # introduce sequencing error
        LOG.write("Simulating sequencing error...")
        for node in GC.subsampled_nodes:
            if GC.VERBOSE:
                print('[%s] Sequencing error for Node %s' % (datetime.now(),str(node)), file=stderr)
            MF.modules['Sequencing'].introduce_sequencing_error(node)
        MF.modules['Sequencing'].finalize()
        LOG.writeln(" done")
        LOG.writeln("Error prone sequence data were written to: %s/error_prone_files" % environ['out_dir_print'])
        LOG.writeln()

        # return to original directory and finish
        chdir(orig_dir)
        if GC.VERBOSE:
            print('[%s] Outputting simulation information' % datetime.now(), file=stderr)
        LOG.writeln("\n===========================   Information   ===========================")
        GC.FAVITES_OUTPUT_SIZE = 0
        for dirpath,dirnames,filenames in walk(GC.out_dir):
            for f in filenames:
                fp = join(dirpath, f)
                GC.FAVITES_OUTPUT_SIZE += getsize(fp)
        LOG.writeln("Output Size (bytes): %d" % GC.FAVITES_OUTPUT_SIZE)
        LOG.writeln("Execution Time (seconds): %d" % time())
        if GC.VERBOSE:
            print('[%s] Outputting list of citations' % datetime.now(), file=stderr)
        LOG.writeln("\n\n============================   Citations   ============================")
        citations = set()
        for module in MF.modules:
            cite = MF.modules[module].cite()
            if isinstance(cite,str):
                citations.add(cite.strip())
            elif isinstance(cite,set) or isinstance(cite,list):
                for c in cite:
                    citations.add(c.strip())
        for citation in sorted(citations):
            LOG.writeln(citation)
        LOG.close()
        if GC.VERBOSE:
            print('[%s] FAVITES Driver finished' % datetime.now(), file=stderr)
