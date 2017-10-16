#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkNode" module
'''
import abc

class ContactNetworkNode(metaclass=abc.ABCMeta):
    '''
    Abstract class defining a ``ContactNetworkNode'' object

    Methods
    -------
    add_virus(virus)
        Add ``virus'' to this ``ContactNetworkNode'' (NOT for infection, but for
        viral evolution! Should be at current time)
    cite()
        Return citation string (or None)
    get_attribute()
        Return the attribute(s) of this ``ContactNetworkNode'' object
    get_contact_network()
        Return the ``ContactNetwork'' object this node is in
    get_first_infection_time()
        Returns the first time this node was infected (or None if never)
    get_infections()
        Return a list of infection(s) as (time, virus) tuples
    get_name()
        Return the name of this ``ContactNetworkNode'' object
    infect(time, virus)
        Infect this ``ContactNetworkNode'' object with ``virus'' at ``time''
    init()
        Initialize the module (if need be)
    is_infected()
        Return True if this node is infected, otherwise False
    num_infections()
        Return the number of infections
    remove_virus(virus)
        Remove ``virus'' from this ``ContactNetworkNode'' (should be at current
        time)
    uninfect()
        Remove all viruses from this ``ContactNetworkNode''
    viruses()
        Iterate over the viruses that exist in this ``ContactNetworkNode''
        object at the current time
    '''

    @staticmethod
    @abc.abstractmethod
    def init():
        '''
        Initialize the module (if need be)
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    def cite():
        '''
        Return citation string (or None)

        Returns
        -------
        citation : str
            The citation string (or None)
        '''
        pass

    @abc.abstractmethod
    def __eq__(self, other):
        '''
        Overridden equality check
        '''
        pass

    @abc.abstractmethod
    def __ne__(self, other):
        '''
        Overridden not equals check
        '''
        pass

    @abc.abstractmethod
    def __lt__(self, other):
        '''
        Overridden less than check
        '''
        pass

    @abc.abstractmethod
    def __gt__(self, other):
        '''
        Overridden greater than check
        '''
        pass

    @abc.abstractmethod
    def __le__(self, other):
        '''
        Overridden less than or equal to check
        '''
        pass

    @abc.abstractmethod
    def __ge__(self, other):
        '''
        Overridden greater than or equal to check
        '''
        pass

    @abc.abstractmethod
    def __hash__(self):
        '''
        Overridden hash function
        '''
        pass

    @abc.abstractmethod
    def __str__(self):
        '''
        Overridden string function
        '''
        pass

    @abc.abstractmethod
    def get_name(self):
        '''
        Return the name of this ``ContactNetworkNode'' object

        Returns
        -------
        name : str
            The name of this ``ContactNetworkNode'' object

        '''
        pass

    @abc.abstractmethod
    def get_attribute(self):
        '''
        Return the attribute(s) of this ``ContactNetworkNode'' object

        Returns
        -------
        attribute : str
            The attribute(s) of this ``ContactNetworkNode'' object
        '''
        pass

    @abc.abstractmethod
    def get_contact_network(self):
        '''
        Returns the ``ContactNetwork'' object this node is in

        Returns
        -------
        contact_network : ContactNetwork
            The ``ContactNetwork'' object this node is in
        '''
        pass

    @abc.abstractmethod
    def get_first_infection_time(self):
        '''
        Returns the first time this node was infected (or None if never)

        Returns
        -------
        time : float
            The first time this node was infected (or None if never)
        '''
        pass

    @abc.abstractmethod
    def get_infections(self):
        '''
        Return the infections of this ``ContactNetworkNode'' object. If
        only one infection, the list will contain a single element.

        Returns
        -------
        infections : list of (float, TreeNode) tuples
            The infections of this ``ContactNetworkNode'' object as
            (time, virus) tuples
        '''
        pass

    @abc.abstractmethod
    def num_infections(self):
        '''
        Return the number of infections of this ``ContactNetworkNode'' object.

        Returns
        -------
        num_infections : int
            The number of infections of this ``ContactNetworkNode'' object.
        '''
        pass

    @abc.abstractmethod
    def infect(self, time, sequence):
        '''
        Infect this ``ContactNetworkNode'' object with ``sequence'' at ``time''.
        Will create the initial ``Tree'' for this infection as well.

        Parameters
        ----------
        time : float
            The time of infection
        sequence : str
            The infecting virus sequence
        '''
        pass

    @abc.abstractmethod
    def is_infected(self):
        '''
        Return True if this node is infected, otherwise False

        Returns
        -------
        infected : bool
            True if this node is infected, otherwise False
        '''
        pass

    @abc.abstractmethod
    def add_virus(self, virus):
        '''
        Add ``virus'' to this ``ContactNetworkNode'' (NOT for infection, but for
        viral evolution! Should be at current time)

        Parameters
        ----------
        virus : TreeNode
            The virus to add to this node (should be at current time)
        '''
        pass

    @abc.abstractmethod
    def remove_virus(self, virus):
        '''
        Return ``virus'' from this node

        Parameters
        ----------
        virus : TreeNode
            The virus to remove from this node (should be at current time)
        '''
        pass

    @abc.abstractmethod
    def uninfect(self):
        '''
        Remove all viruses from this ``ContactNetworkNode''
        '''
        pass

    @abc.abstractmethod
    def viruses(self):
        '''
        Iterate over the viruses that exist in this ``ContactNetworkNode''
        object at the current time
        '''
        pass