#! /usr/bin/env python3
'''
Niema Moshiri 2016

Store global variables/functions to be accessible by all FAVITES modules.
'''
from random import uniform

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
def roll(die):
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