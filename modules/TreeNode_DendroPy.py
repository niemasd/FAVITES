#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TreeNode" module, implemented with DendroPy
'''
from TreeNode import TreeNode # abstract Tree class
import dendropy               # using Dendropy to implement

class TreeNode_DendroPy(TreeNode):
    '''
    Implement the ``Tree`` abstract class using DendroPy

    Attributes
    ----------
    tree : TreeNode
        The DendroPy ``Tree'' object to represent this tree
    end_time : int
        The end time to which this ``TreeNode'' has been evolved
    '''
    def __init__(self):
        import dendropy
        self.tree = dendropy.Tree(seed_node=dendropy.Node(label="root"))
        self.end_time = 0

    def get_end_time(self):
        return self.end_time

def check():
    '''
    Check ``TreeNode_DendroPy`` for validity
    '''
    pass

if __name__ == '__main__':
    '''
    This function is just used for testing purposes. It has no actual function
    in the simulator tool.
    '''
    check()