#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TreeNode" module, implemented simply using pointers
'''
from TreeNode import TreeNode # abstract Tree class
import FAVITES_GlobalContext as GC

class TreeNode_Simple(TreeNode):
    '''
    Implement the ``TreeNode`` abstract class simply using pointers

    Attributes
    ----------
    num_nodes : int
        The total number of nodes that have ever been created
    '''
    num_nodes = 0

    def init():
        pass

    def __init__(self, time=None, contact_network_node=None, seq=None):
        '''
        Note that time and contact_network_node are actually required
        parameters! They are set to "None" so that the abstract method
        implementation check can be done successfully.
        '''
        self.seq = seq
        self.parent = None
        self.root = self
        self.children = set()
        self.time = time
        self.contact_network_node = contact_network_node
        self.num = TreeNode_Simple.num_nodes
        TreeNode_Simple.num_nodes += 1

    def __hash__(self):
        return hash(id(self))

    def __eq__(self, other):
        return id(self) == id(other)

    def __ne__(self, other):
        return not self == other

    def add_child(self, child):
        self.children.add(child)
        child.parent = self
        child.root = self.root

    def get_children(self):
        return self.children

    def get_edge_length(self):
        return self.time - self.parent.get_time()

    def get_label(self):
        if len(self.children) == 0:
            return "L" + str(self.num)
        else:
            return "I" + str(self.num)

    def get_parent(self):
        return self.parent

    def get_root(self):
        return self.root

    def get_seq(self):
        return self.seq

    def set_seq(self, seq):
        self.seq = seq

    def get_time(self):
        return self.time

    def set_time(self, time):
        self.time = time

    def get_contact_network_node(self):
        return self.contact_network_node

    def set_contact_network_node(self, node):
        self.contact_network_node = node

    def leaves(self):
        if len(self.children) == 0:
            yield self
        else:
            for child in self.children:
                yield from child.leaves()

    def newick(self):
        # if leaf
        if len(self.children) == 0:
            return self.get_label()

        # if internal node
        else:
            parts = [child.newick() + ':' + str(child.get_edge_length()) for child in self.children]
            out = '(' + ','.join(parts) + ')' + self.get_label()
            if self.parent == None: # if root, need semicolon (entire tree)
                out += ';'
            return out

def check():
    '''
    Check ``TreeNode_Simple`` for validity
    '''
    pass

if __name__ == '__main__':
    '''
    This function is just used for testing purposes. It has no actual function
    in the simulator tool.
    '''
    check()