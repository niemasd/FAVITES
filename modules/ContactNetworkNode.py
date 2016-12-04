#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkNode" module
'''
import abc # for abstraction

class ContactNetworkNode(metaclass=abc.ABCMeta):
    '''
    Abstract class defining a ``ContactNetworkNode'' object

    Methods
    -------
    get_attribute()
        Return the attribute(s) of this ``ContactNetworkNode'' object
    get_infection()
        Return a list of infection(s) as (time,initial_sequence,tree) tuples
    get_name()
        Return the name of this ``ContactNetworkNode'' object
    infect(time, sequence)
        Infect this ``ContactNetworkNode'' object with ``sequence'' at ``time''
    is_infected()
        Return True if this node is infected, otherwise False
    num_infections()
        Return the number of infections
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
    def infect(self, time, sequence):
        '''
        Infect this ``ContactNetworkNode'' object with ``sequence'' at ``time''.
        Will create the initial ``Tree'' for this infection as well.

        Parameters
        ----------
        time : int
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