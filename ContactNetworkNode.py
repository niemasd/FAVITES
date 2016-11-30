#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworNode" module
'''
import abc # for abstraction

class ContactNetworkNode(metaclass=abc.ABCMeta):
    '''
    Abstract class defining a ``ContactNetworkNode'' object

    Methods
    -------
    get_attribute()
        Return the attribute(s) of this ``ContactNetworkNode'' object
    get_infections()
        Return a list of infections as (time,sequence) tuples
    get_infection_trees()
        Return a list of ``Tree'' objects, where ``get_infection_trees()[i]''
        corresponds to ``get_infections()[i]''
    get_name()
        Return the name of this ``ContactNetworkNode'' object
    infect(time, sequence)
        Infect this ``ContactNetworkNode'' object with ``sequence'' at ``time''
    num_infections()
        Return the number of infections
    num_infection_trees()
        Return the number of infection trees
    '''

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
    def get_infections(self):
        '''
        Return the infections of this ``ContactNetworkNode'' object. If
        only one infection, the list will contain a single element.

        Returns
        -------
        infections : list of tuples
            The infections of this ``ContactNetworkNode'' object as
            (time,sequence) tuples
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
    def get_infection_trees(self):
        '''
        Return a list of ``Tree'' objects, where ``get_infection_trees()[i]''
        corresponds to ``get_infections()[i]''

        Returns
        -------
        trees : list of Tree
            List of ``Tree'' objects, where ``trees[i]'' corresponds to
            ``get_infections()[i]''
        '''
        pass

    @abc.abstractmethod
    def num_infection_trees(self):
        '''
        Return the number of infection trees

        Returns
        -------
        num_infection_trees : int
            The number of infection trees
        '''
        pass

    @abc.abstractmethod
    def add_infection(self, time, sequence):
        '''
        Infect this ``ContactNetworkNode'' object with ``sequence'' at ``time''

        Parameters
        ----------
        time : int
            The time of infection
        sequence : str
            The infecting virus sequence
        '''
        pass

    @abc.abstractmethod
    def add_infection_tree(self, tree):
        '''
        Add tree that corresponds to ``infection[i]''

        Parameters
        ----------
        tree : Tree
            The tree corresponding to ``infection[i]''
        '''
        pass