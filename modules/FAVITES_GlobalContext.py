#! /usr/bin/env python3
'''
Niema Moshiri 2016

Store global variables/functions to be accessible by all FAVITES modules.
'''
import modules.FAVITES_ModuleFactory as MF
from glob import glob
from gzip import open as gopen
from random import uniform,sample
from subprocess import check_output,STDOUT
from itertools import product
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q

# useful constants
FAVITES_VERSION = "1.1.28"
C_INT_MAX = 2147483647
CITATION_ART = 'Huang W., Li L., Myers J.R., Marth G.T. (2012). "ART: a next-generation sequencing read simulator". Bioinformatics. 28(4), 593-594.'
CITATION_DENDROPY = 'Sukumaran J., Holder M.T. (2010). "DendroPy: A Python library for phylogenetic computing". Bioinformatics. 26, 1569-1571.'
CITATION_DUALBIRTH = 'Moshiri N., Mirarab S. (2017). "A Two-State Model of Tree Evolution and its Applications to Alu Retrotransposition". Systematic Biology. 67(3), 1-15.'
CITATION_DWGSIM = 'Homer N. (2011). "DWGSIM" (https://github.com/nh13/DWGSIM).'
CITATION_FAVITES = 'Moshiri N., Ragonnet-Cronin M., Wertheim J.O., Mirarab S. (2018). "FAVITES: simultaneous simulation of transmission networks, phylogenetic trees, and sequences". bioRxiv:297267.'
CITATION_GEMF = 'Sahneh F.D., Vajdi A., Shakeri H., Fan F., Scoglio C. (2016). "GEMFsim: A Stochastic Simulator for the Generalized Epidemic Modeling Framework". arXiv preprint arXiv:1528946.'
CITATION_GRINDER = 'Angly F.E., Willner D., Rohwer F., Hugenholtz P., Tyson G.W. (2012). "Grinder: a versatile amplicon and shotgun sequence simulator". Nucleic Acids Res. 40(12), e94.'
CITATION_HMMER = 'Eddy S.R., Wheeler T.J. (2015). "HMMER Version 3.1b2" (http://hmmer.org/).'
CITATION_MSMS = 'Ewing G., Hermisson J. (2010). "MSMS: a coalescent simulation program including recombination, demographic structure and selection at a single locus". Bioinformatics. 26(16), 2064-2065.'
CITATION_NETWORKX = 'Hagberg A.A., Schult D.A., Swart P.J. (2008). "Exploring network structure, dynamics, and function using NetworkX". Proceedings of the 7th Python in Science Conference (SciPy2008), 11-15.'
CITATION_NUMPY = 'van der Walt S., Colber S.C., Varoquaux G. (2011). "The NumPy Array: A Structure for Efficient Numerical Computation". Computing in Science & Engineering 13, 22-30.'
CITATION_PANGEA = 'Ratmann O., Hodcroft E.B., Pickles M., Cori A., Hall M., Lycett S., Colijn C., Dearlove B., Didelot X., Frost S., Hossain A.S.M.M., Joy J.B., Kendall M., Kuhnert D., Leventhal G.E., Liang R., Plazzotta G., Poon A.F.Y, Rasmussen D.A., Stadler T., Volz E., Weis C., Brown A.J.L., Fraser C. (2016). "Phylogenetic Tools for Generalized HIV-1 Epidemics: Findings from the PANGEA-HIV Methods Comparison". Mol. Biol. Evol. 34(1), 185-203.'
CITATION_PHYLOMMAND = 'Ryberg M. (2016). "Phylommand - a command line software package for phylogenetics [version 1; referees: 2 approved with reservations]". F1000Research 2016, 5:2903 (doi: 10.12688/f1000research.10446.1).'
CITATION_PYVOLVE = 'Spielman S.J., Wilke C.O. (2015). "Pyvolve: A Flexible Python Module for Simulating Sequences along Phylogenies". PLoS One. 10(9), e0139047.'
CITATION_SCIPY = 'Jones E., Oliphant E., Peterson P., et al. (2001). "SciPy: Open Source Scientific Tools for Python" (http://scipy.org/).'
CITATION_SEQGEN = 'Rambaut A., Grassly N. C. (1997). "Seq-Gen: An application for the Monte Carlo simulation of DNA sequence evolution along phylogenetic trees". Comput. Appl. Biosci. 13, 235-238.'
CITATION_TREESWIFT = 'Moshiri N. (2018). "TreeSwift: a massively scalable Python package for trees". bioRxiv:325522.'
COMMUNITY_GENERATORS = ['ContactNetworkGenerator_Communities','ContactNetworkGenerator_Barbell','ContactNetworkGenerator_Caveman','ContactNetworkGenerator_CavemanConnected','ContactNetworkGenerator_CavemanRelaxed','ContactNetworkGenerator_RandomPartitionGraph']

def init(reqs):
    '''
    Initialize global context.

    Parameters
    ----------
    reqs : dict
        Dictionary containing module implementation required variables.
    '''

    global time
    time = 0.0
    for req in reqs:
        globals()[req] = reqs[req]

class Node:
    '''
    Node class, where a node's data attribute is what is stored
    '''
    def __init__(self, data):
        self.data = data
    def __hash__(self):
        return hash(self.data)
    def __eq__(self, other):
        return isinstance(other, Node) and self.data == other.data
    def __ne__(self, other):
        return not self == other
    def __str__(self):
        return '(%s)' % str(self.data)
    def get_data(self):
        return self.data
    def set_data(self, data):
        self.data = data

class SortedLinkedList:
    '''
    Sorted Linked List class (sorted on nodes' priority attribute). If no
    priority is specified, data is used as priority. Sort smallest to largest.
    '''
    def __init__(self):
        self.head = None
        self.size = 0
    def __len__(self):
        return self.size
    def __str__(self):
        out = ''
        curr = self.head
        while curr is not None:
            out += '%s->' % str(curr)
            curr = curr.next
        out += 'X'
        return out

    # add data to list (use data as priority if none is specified)
    def put(self, data, priority=None):
        newNode = Node(data)
        newNode.next = None
        if priority is None:
            newNode.priority = data
        else:
            newNode.priority = priority
        if self.head is None:
            self.head = newNode
        elif self.head.priority > newNode.priority:
            newNode.next = self.head
            self.head = newNode
        else:
            curr = self.head
            while curr.next is not None and newNode.priority > curr.next.priority:
                curr = curr.next
            newNode.next = curr.next
            curr.next = newNode
        self.size += 1

    # iterate over items in list
    def items(self):
        curr = self.head
        while curr is not None:
            yield curr.data
            curr = curr.next

    # remove first instance of data
    def removeFirst(self, data):
        if self.head is None:
            return False
        if self.head.data == data:
            self.head = self.head.next
            self.size -= 1
            return True
        curr = self.head
        while curr.next is not None and curr.next.data != data:
            curr = curr.next
        if curr.next is not None:
            curr.next = curr.next.next
            self.size -= 1
            return True
        else:
            return False

    # remove all instances of data
    def removeAll(self, data):
        while self.head is not None and self.head.data == data:
            self.head = self.head.next
            self.size -= 1
        if self.head is None:
            return
        curr = self.head
        while curr.next is not None:
            if curr.next.data == data:
                curr.next = curr.next.next
                self.size -= 1
            else:
                curr = curr.next

    # get element at front of list
    def getFront(self):
        if self.head is None:
            raise ValueError("Attempting to getFront from an empty list")
        data = self.head.data
        self.head = self.head.next
        self.size -= 1
        return data

# roll a weighted die (keys = faces, values = probabilities)
def roll(orig_die):
    assert len(orig_die) != 0, "Empty weighted die"
    total = float(sum(orig_die.values()))
    die = {face:orig_die[face]/total for face in orig_die}
    faces = sorted(die.keys())
    probs = [die[key] for key in faces]
    cdf = [probs[0]]
    while len(cdf) < len(probs):
        cdf.append(cdf[-1] + probs[len(cdf)])
    num = uniform(0, 1)
    index = 0
    while cdf[index] < num:
        index += 1
    return faces[index]

# convert a NetworkX graph to a FAVITES edge list
def nx2favites(nx_graph, du):
    out = ["NODE\t%s\t." % str(node) for node in nx_graph.nodes()]
    for u,v in nx_graph.edges():
        out.append("EDGE\t%s\t%s\t.\t%s" % (str(u),str(v),du))
    return out

# convert a FAVITES edge list to the GML format
def favites2gml(edge_list):
    # parse FAVITES edge list
    nodes = {} # nodes[node_label] = (id, attributes) tuple (attributes = list of str)
    edges = [] # edges[i] = (u,v,attributes) tuple (attributes = list of str)
    id2node = {} # convert node ID to node label
    for line in edge_list:
        line = line.strip()
        if len(line) == 0 or line[0] == '#':
            continue
        parts = line.split('\t')

        # this is a node
        if parts[0] == 'NODE':
            name = parts[1]
            if name in nodes:
                raise ValueError("Node %r already exists!" % name)
            if parts[2] == '.':
                attr = []
            else:
                attr = parts[2].split(',')
            ID = len(nodes)+1
            nodes[name] = (ID,attr)
            id2node[ID] = name

        # this is an edge
        elif parts[0] == 'EDGE':
            uName = parts[1]
            if uName not in nodes:
                raise ValueError("Node %r does not exist!" % uName)
            vName = parts[2]
            if vName not in nodes:
                raise ValueError("Node %r does not exist!" % vName)
            if parts[3] == '.':
                attr = []
            else:
                attr = parts[3].split(',')
            edges.append((uName,vName,attr))
            if parts[4] == 'u': # undirected edge, so add v to u too
                edges.append((vName,uName,attr))

        # invalid type
        else:
            raise ValueError("Invalid type in list: %r" % parts[0])

    # print graph as GML
    out = "graph [\n"
    for node in nodes:
        ID,attr = nodes[node]
        out += "\tnode [\n\t\tid "
        out += str(ID)
        out += '\n\t\tlabel "'
        out += node
        out += '"\n'
        for i in range(len(attr)):
            out += "\t\tattribute"
            out += str(i+1)
            out += ' "'
            out += attr[i]
            out += '"\n'
        out += "\t]\n"
    for u,v,attr in edges:
        out += "\tedge [\n\t\tsource "
        out += str(nodes[u][0])
        out += "\n\t\ttarget "
        out += str(nodes[v][0])
        out += "\n"
        for i in range(len(attr)):
            out += "\t\tattribute"
            out += str(i+1)
            out += ' "'
            out += attr[i]
            out += '"\n'
        out += "\t]\n"
    out += "]"
    return out,id2node

# parse FASTA file (single-line or multi-line)
def parseFASTA(f):
    seqs = {}
    currID = None
    currSeq = ''
    for line in f:
        l = line.strip()
        if len(l) == 0:
            continue
        if l[0] == '>':
            if currID is not None:
                seqs[currID] = currSeq
                currSeq = ''
            currID = l[1:]
        else:
            currSeq += l.replace(' ','').replace('\t','')
    seqs[currID] = currSeq
    return seqs

# generate all k-mers of a given alphabet
def generate_all_kmers(k, alphabet):
    return [e for e in map(''.join, product(alphabet, repeat=k))]

# Let L = L0, L1, L2, ... be rates, and let X = X0, X1, X2, ... be exponential random variables where Xi has rate Li. Return the probability that Xi is the minimum of X
def prob_exp_min(i, L):
    assert i >= 0 and i < len(L), "Invalid index i. Must be 0 <= i < |L|"
    return L[i]/sum(L)

# helper for BirthDeath and DualBirth
def treenode_add_child(parent_treenode, child_dpnode, cn_node):
    if parent_treenode.get_time() >= time:
        parent_treenode.set_time(time)
        cn_node.add_virus(parent_treenode)
        return
    newnode = MF.modules['TreeNode'](time=parent_treenode.get_time()+child_dpnode.edge_length, contact_network_node=cn_node)
    parent_treenode.add_child(newnode)
    try:
        children = child_dpnode.children # TreeSwift
    except AttributeError:
        children = child_dpnode.child_nodes() # DendroPy
    for c in children:
        treenode_add_child(newnode,c,cn_node)
    if len(children) == 0:
        newnode.set_time(time)
        cn_node.add_virus(newnode)

# prune sampled phylogenetic trees
def prune_sampled_trees():
    # if a NodeEvolution module already created pruned trees, do nothing (make sure to create and update GC.leaves_at_sample_time!)
    if 'sampled_trees' in globals():
        return

    # otherwise, prune the sampled trees
    global leaves_at_sample_time
    leaves_at_sample_time = {} # leaves_at_sample_time[cn_node][time] = set of TreeNode
    global sampled_trees
    sampled_trees = set()
    TreeNode = MF.modules['TreeNode']
    # check if required sample variables exist
    try:
        cn_sample_times
    except NameError:
        assert False, "GC.cn_sample_times doesn't exist!"
    try:
        root_viruses
    except NameError:
        assert False, "GC.root_viruses doesn't exist!"

    # prune sampled trees
    all_cn_sample_times = {inner for outer in cn_sample_times.values() for inner in outer}
    for index in range(len(root_viruses)):
        WAS_SAMPLED = False
        final_tree_leaves = set()
        present_at_time = {t:set() for t in all_cn_sample_times}
        desired_times = {}
        stack = [root_viruses[index]]
        while len(stack) != 0:
            curr = stack.pop()
            for t in all_cn_sample_times:
                if curr.get_time() >= t:
                    curr_parent = curr.get_parent()
                    if curr_parent is None or curr_parent.get_time() < t:
                        present_at_time[t].add(curr)
            for c in curr.get_children():
                stack.append(c)
        for person in cn_sample_times:
            assert len(cn_sample_times[person]) != 0, "Encountered individual with no sample times!"
            for t in cn_sample_times[person]:
                possible_viruses = [u for u in present_at_time[t] if u.get_contact_network_node() == person]
                num_to_sample = min(len(possible_viruses), MF.modules['NumBranchSample'].sample_num_branches(person,t))
                if num_to_sample != 0:
                    sampled_viruses = sample(possible_viruses, num_to_sample)
                    final_tree_leaves.update(sampled_viruses)
                    for virus in sampled_viruses:
                        if virus not in desired_times:
                            desired_times[virus] = [t]
                        else:
                            desired_times[virus].append(t)
        for leaf in final_tree_leaves:
            curr = leaf
            while curr != None:
                curr.has_sampled_descendant = True
                curr = curr.get_parent()
        if not hasattr(root_viruses[index],"has_sampled_descendant"):
            continue
        stack = [root_viruses[index]]
        while len(stack) != 0:
            curr = stack.pop()
            children = [c for c in curr.get_children()]
            if curr in desired_times:
                curr_times = sorted(desired_times[curr], reverse=True)
                while (len(children) != 0 and len(curr_times) > 0) or (len(children) == 0 and len(curr_times) > 1):
                    t = curr_times.pop()
                    newnode = TreeNode(time=t, seq=curr.get_seq(), contact_network_node=curr.get_contact_network_node())
                    curr_parent = curr.get_parent()
                    newnode.set_parent(curr_parent)
                    if curr_parent is not None:
                        curr_parent.remove_child(curr)
                        curr_parent.add_child(newnode)
                    else:
                        newnode.set_seq(root_viruses[index].get_seq())
                        root_viruses[index] = newnode
                        newnode.set_parent(None)
                        curr.set_root(root_viruses[index])
                    newnode.set_root(root_viruses[index])
                    newnode.add_child(curr)
                    curr.set_parent(newnode)
                    newnode2 = TreeNode(time=t, seq=curr.get_seq(), contact_network_node=curr.get_contact_network_node())
                    newnode2.set_root(root_viruses[index])
                    newnode2.set_parent(newnode)
                    newnode.add_child(newnode2)
                if len(children) == 0:
                    curr.set_time(curr_times[0])
                del desired_times[curr]
                stack.append(curr)
                continue
            curr.set_root(root_viruses[index])
            assert len(children) in {0,1,2}, "Invalid number of children"
            if len(children) == 0:
                continue
            elif len(children) == 1:
                curr_parent = curr.get_parent()
                if curr_parent is not None:
                    curr_parent.remove_child(curr)
                    curr_parent.add_child(children[0])
                else:
                    children[0].set_seq(root_viruses[index].get_seq())
                    root_viruses[index] = children[0]
                    children[0].set_parent(None)
                stack.append(children[0])
                continue
            elif len(children) == 2:
                if hasattr(children[0], 'has_sampled_descendant') and hasattr(children[1], 'has_sampled_descendant'):
                    stack += children
                elif hasattr(children[0], 'has_sampled_descendant'):
                    curr.remove_child(children[1])
                    stack.append(curr)
                elif hasattr(children[1], 'has_sampled_descendant'):
                    curr.remove_child(children[0])
                    stack.append(curr)
                else:
                    curr.remove_child(children[0])
                    curr.remove_child(children[1])

        # update leaves_at_sample_time (IMPORTANT!)
        stack = [root_viruses[index]]
        while(len(stack) != 0):
            curr = stack.pop()
            children = [c for c in curr.get_children()]
            if len(children) == 0:
                cn_node = curr.get_contact_network_node()
                time = curr.get_time()
                if cn_node not in leaves_at_sample_time:
                    leaves_at_sample_time[cn_node] = {}
                if time not in leaves_at_sample_time[cn_node]:
                    leaves_at_sample_time[cn_node][time] = set()
                leaves_at_sample_time[cn_node][time].add(curr)
            else:
                stack += children

        # finished
        sampled_trees.add((root_viruses[index],root_viruses[index].newick()))

# PANGEA module check
def pangea_module_check():
    assert "ContactNetwork_PANGEA" in str(MF.modules['ContactNetwork']), "Must use ContactNetwork_PANGEA module"
    assert "ContactNetworkGenerator_PANGEA" in str(MF.modules['ContactNetworkGenerator']), "Must use ContactNetworkGenerator_PANGEA module"
    assert "EndCriteria_Instant" in str(MF.modules['EndCriteria']), "Must use EndCriteria_Instant module"
    assert "NodeEvolution_PANGEA" in str(MF.modules['NodeEvolution']), "Must use NodeEvolution_PANGEA module"
    assert "NodeAvailability_PANGEA" in str(MF.modules['NodeAvailability']), "Must use NodeAvailability_PANGEA module"
    assert "NumBranchSample_All" in str(MF.modules['NumBranchSample']), "Must use NumBranchSample_All module"
    assert "NumTimeSample_PANGEA" in str(MF.modules['NumTimeSample']), "Must use NumTimeSample_PANGEA module"
    assert "SeedSelection_PANGEA" in str(MF.modules['SeedSelection']), "Must use SeedSelection_PANGEA module"
    assert "SeedSequence_PANGEA" in str(MF.modules['SeedSequence']), "Must use SeedSequence_PANGEA module"
    assert "SequenceEvolution_PANGEA" in str(MF.modules['SequenceEvolution']), "Must use SequenceEvolution_PANGEA module"
    assert "SourceSample_PANGEA" in str(MF.modules['SourceSample']), "Must use SourceSample_PANGEA module"
    assert "TimeSample_PANGEA" in str(MF.modules['TimeSample']), "Must use TimeSample_PANGEA module"
    assert "TransmissionNodeSample_PANGEA" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_PANGEA module"
    assert "TransmissionTimeSample_PANGEA" in str(MF.modules['TransmissionTimeSample']), "Must use TransmissionTimeSample_PANGEA module"
    assert "TreeUnit_Same" in str(MF.modules['TreeUnit']), "Must use TreeUnit_Same module"

# merge seed/cluster trees generated using SeqGen seed sequence modules
def merge_trees_seqgen():
    from queue import Queue
    try:
        global read_tree_newick
        from treeswift import read_tree_newick
    except:
        from os import chdir
        chdir(GC.START_DIR)
        assert False, "Error loading TreeSwift. Install with: pip3 install treeswift"
    seed_tree = read_tree_newick(open('seed_sequences/seed.txt').read().strip().splitlines()[-1].strip())
    seed_leaves = {}
    for leaf in seed_tree.traverse_leaves():
        seed_leaves[str(leaf)] = leaf
    seed_tree_time = read_tree_newick('seed_sequences/time_tree.tre')
    seed_leaves_time = {}
    for leaf in seed_tree_time.traverse_leaves():
        seed_leaves_time[str(leaf)] = leaf
    seq_to_seed_leaf = {}
    for line in open('seed_sequences/seqgen.out').read().strip().splitlines()[1:]:
        leaf,seq = line.strip().split()
        if seq not in seq_to_seed_leaf:
            seq_to_seed_leaf[seq] = {leaf}
        else:
            seq_to_seed_leaf[seq].add(leaf)
    seed_leaf_to_tree = {}
    seed_leaf_to_tree_time = {}
    its = 0
    for treefile in glob('error_free_files/phylogenetic_trees/*.tre.gz'):
        if '.time.' in treefile:
            continue
        its += 1
        treenum = int(treefile.split('/')[-1].split('_')[1].split('.')[0])
        seed_leaf = seq_to_seed_leaf[final_tree_to_root_seq[treenum]].pop()
        seed_leaf_to_tree[seed_leaf] = read_tree_newick(treefile)
        seed_leaf_to_tree_time[seed_leaf] = read_tree_newick(treefile.replace('.tre','.time.tre'))
    to_prune = Queue()
    for leaf in seed_leaves:
        if leaf in seed_leaf_to_tree: # if this seed's cluster was sampled (so tree exists)
            seed_leaves[leaf].add_child(seed_leaf_to_tree[leaf].root)
            seed_leaves_time[leaf].add_child(seed_leaf_to_tree_time[leaf].root)
        else: # if not, delete this seed leaf
            to_prune.put(seed_leaves[leaf])
            to_prune.put(seed_leaves_time[leaf])
    merged_tree_exists = True
    while not to_prune.empty():
        leaf = to_prune.get()
        parent = leaf.parent
        if parent is not None:
            parent.remove_child(leaf)
            if len(parent.children) == 0:
                if parent.is_root():
                    merged_tree_exists = False; break
                else:
                    to_prune.put(parent)
    if merged_tree_exists:
        seed_tree.suppress_unifurcations()
        seed_tree_time.suppress_unifurcations()
        return [str(seed_tree)],[str(seed_tree_time)]
    else:
        return [],[]

# generate a Mean Coalescent tree (return as Newick string)
def mean_kingman_tree(num_leaves, pop_size):
    from dendropy.simulate import treesim
    from dendropy import TaxonNamespace
    return treesim.mean_kingman_tree(TaxonNamespace([str(i) for i in range(num_leaves)]), pop_size=pop_size).as_string(schema='newick')

# generate a Pure Coalescent tree (return as Newick string)
def pure_kingman_tree(num_leaves, pop_size):
    from dendropy.simulate import treesim
    from dendropy import TaxonNamespace
    import random as rng
    return treesim.pure_kingman_tree(TaxonNamespace([str(i) for i in range(num_leaves)]), pop_size=pop_size, rng=rng).as_string(schema='newick')

# Seq-Gen executable check
def check_seqgen_executable():
    try:
        s = check_output([seqgen_path,'-h'],stderr=STDOUT).decode()
    except Exception as e:
        s = str(e)
    assert "Usage: seq-gen" in s, "seqgen executable was not found: %s" % seqgen_path

# check if string would be safe for eval()
def check_eval_str(s):
    if "'" in s or '"' in s:
        return False
    return True
