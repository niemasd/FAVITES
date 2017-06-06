#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TreeNode" module, implemented simply using pointers
'''
from TreeNode import TreeNode
import FAVITES_GlobalContext as GC
from sys import setrecursionlimit
setrecursionlimit(100000)

class TreeNode_Simple(TreeNode):
    '''
    Implement the ``TreeNode`` abstract class simply using pointers

    Attributes
    ----------
    num_nodes : int
        The total number of nodes that have ever been created
    '''
    num_nodes = 0

    def cite():
        return GC.CITATION_FAVITES

    def init():
        GC.label_to_node = {}

    def label_to_node():
        return GC.label_to_node

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
        if hasattr(GC,"label_to_node"): # for initialization
            GC.label_to_node[self.get_label()] = self

    def __str__(self): # label|contact network node|time
        return self.get_label() + '|' + str(self.get_contact_network_node()) + '|' + str(self.get_time())

    def str_to_node(string):
        return GC.label_to_node[string.split('|')[0]]

    def __hash__(self):
        return self.num

    def __eq__(self, other):
        return isinstance(other, TreeNode_Simple) and self.num == other.num

    def __ne__(self, other):
        return not isinstance(other, TreeNode_Simple) or self.num != other.num

    def __lt__(self, other):
        return self.time < other.time

    def add_child(self, child):
        self.children.add(child)
        child.parent = self
        child.root = self.root

    def split(self):
        c1 = TreeNode_Simple(time=self.time, seq=self.seq, contact_network_node=self.contact_network_node)
        c2 = TreeNode_Simple(time=self.time, seq=self.seq, contact_network_node=self.contact_network_node)
        self.add_child(c1)
        self.add_child(c2)
        self.contact_network_node.remove_virus(self)
        self.contact_network_node.add_virus(c1)
        self.contact_network_node.add_virus(c2)
        return c1,c2

    def get_children(self):
        return self.children

    def remove_child(self, child):
        self.children.discard(child)

    def get_edge_length(self):
        assert self.time >= self.parent.get_time(), "A TreeNode object's time cannot be less than its parent's time"
        return self.time - self.parent.get_time()

    def get_label(self):
        return "N" + str(self.num)

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    def get_root(self):
        return self.root

    def set_root(self, newroot):
        self.root = newroot

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
        q = [self]
        while len(q) > 0:
            curr = q.pop()
            if len(curr.children) == 0:
                yield curr
            else:
                q.extend(curr.children)

    def newick(self, redo=False):
        # try to fix single-child nodes
        if len(self.children) == 1:
            child = list(self.children)[0]
            if self.parent is None:
                child.parent = None
            else:
                child.parent = self.parent
            return child.newick()

        # error message for invalid number of children
        assert len(self.children) == 0 or len(self.children) == 2, "Encountered node (%s) with number of children != 0 or 2: %d (parent: %s)" % (str(self),len(self.children),str(self.get_parent()))

        # if leaf
        if len(self.children) == 0:
            if self.parent == None: # one-node tree
                return '(' + str(self) + ':' + str(self.time) + ');'
            else:
                return str(self)

        # if internal node
        else:
            parts = [child.newick() + ':' + str(child.get_edge_length()) for child in self.children]
            out = '(' + ','.join(parts) + ')' + str(self)
            if self.parent == None: # if root, need semicolon (entire tree)
                out += ':' + str(self.time) + ';'
            return out

    def replace_content(self, other):
        self.seq = other.seq
        self.parent = other.parent
        self.root = other.root
        self.children = other.children
        self.time = other.time
        self.contact_network_node = other.contact_network_node
        self.num = other.num

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