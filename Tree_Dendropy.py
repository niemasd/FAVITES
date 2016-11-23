#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Tree" module, implemented with DendroPy
'''
from Tree import Tree # abstract Tree class
import dendropy       # using Dendropy to implement

class Tree_DendroPy(Tree):
    '''
    Implement the ``Tree`` abstract class using DendroPy
    '''
    def __init__(self):
        import dendropy
        self.tree = dendropy.Tree(seed_node=dendropy.Node(label="root"))

def check():
    '''
    Check ``Tree_DendroPy`` for validity
    '''
    print("--- Testing Tree_DendroPy Module ---")
    print("Instantiation class: ",end='')
    tree = Tree_DendroPy()
    status = "Success"
    if not isinstance(tree, Tree):
        status = "Failure"
    print(status)

if __name__ == '__main__':
    '''
    This function is just used for testing purposes. It has no actual function
    in the simulator tool.
    '''
    check()