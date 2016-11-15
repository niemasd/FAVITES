#! /usr/bin/env python
'''
Niema Moshiri 2016

"Tree" module
'''
from abc import ABCMeta, abstractmethod # for abstraction

class Tree:
    '''
    Abstract class defining a Tree object
    '''
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        '''
        Construct a new Tree object

        :return: None
        '''
        pass

class Tree_Dendropy(Tree):
    '''
    Implement the Tree abstract class using Dendropy
    '''
    def __init__(self):
        '''
        Construct a new Tree object using Dendropy

        :return: None
        '''
        import dendropy
        self.tree = dendropy.Tree(seed_node=dendropy.Node(label="root"))

def check():
    '''
    Check all Tree classes for validity

    :return: None
    '''
    print("--- Testing Tree Module ---")

    # Test Tree_Dendropy class
    print("Tree_Dendropy class: "),
    tree = Tree_Dendropy()
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