#! /usr/bin/env python3
'''
Niema Moshiri 2016

"NodeEvolution" module, dummy implementation
'''
from NodeEvolution import NodeEvolution # abstract NodeEvolution class

class NodeEvolution_Dummy(NodeEvolution):
    def evolve_to_current_time(node):
        #print('\nWARNING: Using dummy NodeEvolution implementation!')
        pass