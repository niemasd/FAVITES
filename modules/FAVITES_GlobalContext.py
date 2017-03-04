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