#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TreeNode" module
'''
import abc

class TreeNode(metaclass=abc.ABCMeta):
    '''
    Abstract class defining a ``TreeNode'' object

    Methods
    -------
    add_child(child):
        Add ``child'' to this ``TreeNode'' object's children
    get_children()
        Return a list containing the children of this ``TreeNode'' object
    get_contact_network_node()
        Return the ``ContactNetworkNode'' object in which this ``TreeNode''
        object exists.
    get_edge_length()
        Return the length of the edge that is incident to this ``TreeNode''
    get_label()
        Return the label of this ``TreeNode'' object
    get_parent()
        Return the parent of this ``TreeNode'' object (or None if root)
    get_seq()
        Return the sequence of this ``TreeNode'' object (or None if none)
    get_time()
        Return the time of this ``TreeNode'' object
    init()
        Initialize the module (if need be)
    label_to_node()
        Return a dictionary mapping labels to ``TreeNode'' objects
    leaves()
        Iterate over the leaf descendants of this ``TreeNode'' object
    newick()
        Output the subtree of this ``TreeNode'' object in the Newick format
    set_contact_network_node(node)
        Set the ``ContactNetworkNode'' object in which this ``TreeNode'' object
        exists.
    set_seq(seq)
        Set the sequence of this ``TreeNode'' object
    set_time(time)
        Set the time of this ``TreeNode'' object
    split()
        Create two 0-branch-length children as descendants of this node
    str_to_node(string)
        Returns the TreeNode whose str(node) == string
    '''

    @abc.abstractmethod
    def __init__(self, time, seq=None, parent=None):
        '''
        Construct a new ``TreeNode'' object
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    def init():
        '''
        Initialize the module (if need be)
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    def label_to_node():
        '''
        Return a dictionary mapping labels to ``TreeNode'' objects

        Returns
        -------
        dic : dict
            A dictionary mapping labels to ``TreeNode'' objects
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    def str_to_node(string):
        '''
        Returns the TreeNode whose str(node) == string

        Returns
        -------
        node : TreeNode
            The TreeNode whose str(node) == string
        '''
        pass

    @abc.abstractmethod
    def __eq__(self, other):
        '''
        Overloaded equality check
        '''
        pass

    @abc.abstractmethod
    def __ne__(self, other):
        '''
        Overloaded not equals check
        '''
        pass

    @abc.abstractmethod
    def __lt__(self, other):
        '''
        Overloaded less than check
        '''
        pass

    @abc.abstractmethod
    def __hash__(self):
        '''
        Overloaded hash function
        '''
        pass

    @abc.abstractmethod
    def __str__(self):
        '''
        Overloaded string function
        '''
        pass

    @abc.abstractmethod
    def add_child(self, child):
        '''
        Add ``child'' to this ``TreeNode'' object's children

        Parameters
        ----------
        child : TreeNode
            The ``TreeNode'' object to add to this object's children
        '''
        pass

    @abc.abstractmethod
    def get_children(self):
        '''
        Return a list containing the children of this ``TreeNode'' object

        Returns
        -------
        children : list of TreeNode
            List containing the children of this ``TreeNode'' object
        '''
        pass

    @abc.abstractmethod
    def get_contact_network_node(self):
        '''
        Return the ``ContactNetworkNode'' object in which this ``TreeNode''
        object exists.

        Returns
        -------
        node : ContactNetworkNode
            The ``ContactNetworkNode'' object in which this ``TreeNode'' object
            exists.
        '''
        pass

    @abc.abstractmethod
    def get_edge_length(self):
        '''
        Return the length of the edge that is incident to this ``TreeNode''

        Returns
        -------
        length : float
            The length of the edge that is incident to this ``TreeNode''
        '''
        pass

    @abc.abstractmethod
    def get_parent(self):
        '''
        Return the parent of this ``TreeNode'' object (or None if root)

        Returns
        -------
        parent : TreeNode
            The parent of this ``TreeNode'' object (or None if root)
        '''
        pass

    @abc.abstractmethod
    def get_root(self):
        '''
        Return the root of the tree in which this ``TreeNode'' object exists

        Returns
        -------
        root : TreeNode
            The root of the tree in which this ``TreeNode'' object exists
        '''
        pass

    @abc.abstractmethod
    def get_seq(self):
        '''
        Return the sequence of this ``TreeNode'' object (or None if none)

        Returns
        -------
        seq : str
            The sequence of this ``TreeNode'' object (or None if none)
        '''
        pass

    @abc.abstractmethod
    def leaves(self):
        '''
        Iterate over the leaf descendants of this ``TreeNode'' object
        '''
        pass

    @abc.abstractmethod
    def newick(self, redo=False):
        '''
        Output the subtree of this ``TreeNode'' object in the Newick format

        Parameters
        ----------
        redo : bool
            True if you want to regenerate the newick string even if it has
            already been generated for this ``TreeNode'' object, otherwise
            False (default).

        Returns
        -------
        newick_string : str
            This ``TreeNode'' object's subtree as a Newick string
        '''
        pass

    @abc.abstractmethod
    def set_contact_network_node(self, node):
        '''
        Set the ``ContactNetworkNode'' object in which this ``TreeNode'' object
        exists.

        Parameters
        ----------
        node : ContactNetworkNode
            The ``ContactNetworkNode'' object in which this ``TreeNode'' object
            exists.
        '''
        pass

    @abc.abstractmethod
    def set_seq(self, seq):
        '''
        Set the sequence of this ``TreeNode'' object.

        Parameters
        ----------
        seq : str
            The sequence to set as the sequence of this ``TreeNode'' object
        '''
        pass

    @abc.abstractmethod
    def set_time(self, time):
        '''
        Set the time of this ``TreeNode'' object

        Parameters
        ----------
        time : float
            The time to set for this ``TreeNode'' object
        '''
        pass

    @abc.abstractmethod
    def split(self):
        '''
        Create two 0-branch-length children as descendants of this node

        Useful for if your transmission source contact node only has 1 virus
        object to transmit

        Returns
        -------
        (u,v) : tuple of 2 TreeNode
            The two children of this node (0-length branches)
        '''
        pass
