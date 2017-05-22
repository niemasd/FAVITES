#! /usr/bin/env python3
'''
Niema Moshiri 2016

Store global variables/functions to be accessible by all FAVITES modules.
'''
import modules.FAVITES_ModuleFactory as MF
from random import uniform,sample
from time import strftime
from itertools import product
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q

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
        return '(' + str(self.data) + ')'
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
            out += str(curr) + '->'
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
    out = ["NODE\t" + str(node) + "\t." for node in nx_graph.nodes()]
    for u,v in nx_graph.edges():
        out.append("EDGE\t" + str(u) + "\t" + str(v) + "\t.\t" + du)
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

# convert a FAVITES transmission network to the GEXF format
def tn_favites2gexf(cn,tn):
    edges = {(edge.get_from(),edge.get_to()):[0,time+1] for edge in cn.edges_iter()} # include CN edges
    for u,v,t in tn:
        if u != v:
            times = edges[(u,v)]
            for i in range(len(times)):
                if times[i] > t:
                    break
            edges[(u,v)] = times[:i] + [t] + times[i:]
    out = '<?xml version="1.0" encoding="UTF-8"?>\n'
    out += '<gexf xmlns="http://www.gexf.net/1.3" version="1.3" xmlns:viz="http://www.gexf.net/1.3/viz" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.gexf.net/1.3 http://www.gexf.net/1.3/gexf.xsd">\n'
    out += '  <meta lastmodifieddate="' + strftime("%Y/%m/%d") + '">\n'
    out += '    <creator>FAVITES</creator>\n'
    out += '    <description>Transmission network generated by FAVITES (Niema Moshiri 2017)</description>\n'
    out += '  </meta>\n'
    out += '  <graph defaultedgetype="directed" timeformat="double" timerepresentation="interval" mode="dynamic">\n'
    out += '    <attributes class="node" mode="dynamic">\n'
    out += '      <attribute id="infected" title="infected" type="boolean" />\n'
    out += '    </attributes>\n'
    out += '    <attributes class="edge" mode="dynamic">\n'
    out += '      <attribute id="transmission" title="transmission" type="boolean" />\n'
    out += '    </attributes>\n'
    nodes = [node for node in cn.nodes_iter()]
    try:
        nodes.sort(key=lambda x: float(x.get_name()))
    except:
        nodes.sort(key=lambda x: x.get_name())
    out += '    <nodes>\n'
    for node in nodes:
        times = [i[0] for i in node.get_infections()]
        out += '      <node id="'
        out += node.get_name()
        out += '" label="'
        out += node.get_name()
        out += '">\n'
        out += '        <spells>\n'
        out += '          <spell start="0.0" />\n'
        out += '        </spells>\n'
        out += '        <attvalues>\n'
        if len(times) == 0: # uninfected nodes
            out += '          <attvalue for="infected" value="false" start="0.0" end="' + str(time+1) + '" />\n'
        elif times[0] == 0: # seed node
            out += '          <attvalue for="infected" value="true" start="0.0" end="' + str(time+1) + '" />\n'
        else: # regular infected nodes
            out += '          <attvalue for="infected" value="false" start="0.0" end="' + str(times[0]) + '" />\n'
            out += '          <attvalue for="infected" value="true" start="' + str(times[0]) + '" end="' + str(time+1) + '" />\n'
        out += '        </attvalues>\n'
        out += '      </node>\n'
    out += '    </nodes>\n'
    out += '    <edges>\n'
    edge_count = 0
    for u,v in edges:
        times = edges[(u,v)]
        out += '      <edge id="'
        out += str(edge_count)
        edge_count += 1
        out += '" source="'
        out += u.get_name()
        out += '" target="'
        out += v.get_name()
        out += '">\n'
        out += '        <spells>\n'
        out += '          <spell start="0.0" />\n'
        out += '        </spells>\n'
        out += '        <attvalues>\n'
        for i in range(len(times)-1):
            out += '          <attvalue for="transmission" value="' + str(i != 0).lower() + '" start="' + str(times[i]) + '" end="'+str(times[i+1]) + '" />\n'
        out += '        </attvalues>\n'
        out += '      </edge>\n'
    out += '    </edges>\n'
    out += '  </graph>\n'
    out += '</gexf>\n'
    return out

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

# fix single-child nodes by attaching child to parent
def fix_single_child_nodes(root):
    stack = [root]
    while len(stack) != 0:
        curr = stack.pop()
        children = [c for c in curr.get_children()]
        if len(children) == 1:
            if curr.get_parent() is not None:
                curr.get_parent().remove_child(curr)
                curr.add_child(children[0])
            else:
                curr.replace_content(children[0])
        for c in children:
            stack.append(c)

# prune sampled phylogenetic trees
def prune_sampled_trees():
    TreeNode = MF.modules['TreeNode']
    # check if required sample variables exist
    try:
        cn_sample_times
    except NameError:
        assert False, "GC.cn_sample_times doesn't exist!"
    try:
        sampled_trees
    except NameError:
        assert False, "GC.sampled_trees doesn't exist!"

    # prune sampled trees
    all_cn_sample_times = {inner for outer in cn_sample_times.values() for inner in outer}
    for index in range(len(sampled_trees)):
        #print(sampled_trees[index].newick())
        final_tree_leaves = set()
        present_at_time = {t:set() for t in all_cn_sample_times}
        desired_times = {}
        stack = [sampled_trees[index]]
        while len(stack) != 0:
            curr = stack.pop()
            for t in all_cn_sample_times:
                if curr.get_time() >= t:
                    if curr.get_parent() is None or curr.get_parent().get_time() < t:
                        present_at_time[t].add(curr)
            for c in curr.get_children():
                stack.append(c)
        for person in cn_sample_times:
            if len(cn_sample_times[person]) == 0:
                continue
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
        stack = [sampled_trees[index]]
        while len(stack) != 0:
            curr = stack.pop()
            children = [c for c in curr.get_children()]
            if curr in desired_times:
                curr_times = sorted(desired_times[curr], reverse=True)
                while (len(children) != 0 and len(curr_times) > 0) or (len(children) == 0 and len(curr_times) > 1):
                    t = curr_times.pop()
                    newnode = TreeNode(time=t, seq=curr.get_seq(), contact_network_node=curr.get_contact_network_node())
                    newnode.set_parent(curr.get_parent())
                    if curr.get_parent() is not None:
                        curr.get_parent().remove_child(curr)
                        curr.get_parent().add_child(newnode)
                    else:
                        sampled_trees[index] = newnode
                    newnode.add_child(curr)
                    newnode2 = TreeNode(time=t, seq=curr.get_seq(), contact_network_node=curr.get_contact_network_node())
                    newnode2.set_parent(newnode)
                    newnode.add_child(newnode2)
                if len(children) == 0:
                    curr.set_time(curr_times[0])
                del desired_times[curr]
                stack.append(curr)
                continue
            assert len(children) in {0,1,2}, "Invalid number of children"
            if len(children) == 0:
                continue
            if len(children) == 1:
                if curr.get_parent() is not None:
                    curr.get_parent().remove_child(curr)
                    curr.get_parent().add_child(children[0])
                else:
                    sampled_trees[index] = children[0]
                stack.append(children[0])
                continue
            elif len(children) == 2:
                if hasattr(children[0], 'has_sampled_descendant') and hasattr(children[1], 'has_sampled_descendant'):
                    stack += children
                    continue
                elif hasattr(children[0], 'has_sampled_descendant'):
                    curr.remove_child(children[1])
                    stack.append(curr)
                elif hasattr(children[1], 'has_sampled_descendant'):
                    curr.remove_child(children[0])
                    stack.append(curr)
                else:
                    curr.remove_child(children[0])
                    curr.remove_child(children[1])
                continue
        fix_single_child_nodes(sampled_trees[index])
        #print(sampled_trees[index].newick(),end='\n\n')

# returns dictionary where keys are CN nodes and values are set of tree leaves
def get_leaves(roots):
    leaves = {}
    for root in roots:
        stack = [root]
        while len(stack) != 0:
            curr = stack.pop()
            children = [c for c in curr.get_children()]
            if len(children) == 0:
                cn_node = curr.get_contact_network_node()
                if cn_node not in leaves:
                    leaves[cn_node] = set()
                leaves[cn_node].add(curr)
            else:
                stack += children
    return leaves