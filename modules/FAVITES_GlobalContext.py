#! /usr/bin/env python3
'''
Niema Moshiri 2016

Store global variables to be accessible by all FAVITES modules.
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