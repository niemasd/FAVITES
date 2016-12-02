#! /usr/bin/env python3
'''
Niema Moshiri 2016

"NodeEvolution" module, dummy implementation
'''
import FAVITES_Global                   # for global access variables
from NodeEvolution import NodeEvolution # abstract NodeEvolution class

class NodeEvolution_Dummy(NodeEvolution):
    def evolve_to_current_time(node):
        print('\nWARNING: Using dummy NodeEvolution implementation!')