#! /usr/bin/env python3
'''
Niema Moshiri 2016

"NodeEvolution" module, dummy implementation
'''
from NodeEvolution import NodeEvolution # abstract NodeEvolution class
from sys import stderr                  # to write to standard error

class NodeEvolution_Dummy(NodeEvolution):
    def evolve(node, module_Tree):
        print('\nWARNING: Using dummy NodeEvolution implementation!\n', file=stderr)
        node.add_infection_tree(module_Tree())