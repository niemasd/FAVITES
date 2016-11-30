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
    get_name()
        Return the name of this ``ContactNetworkNode'' object
    get_virus_seqs()
        Return a list of virus sequences in this ``ContactNetworkNode'' object
    infect(time, sequence)
        Infect this ``ContactNetworkNode'' object with ``sequence'' at ``time''

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
        Return the infection time(s) of this ``ContactNetworkNode'' object. If
        only one infection, the list will contain a single element.

        Returns
        -------
        times : list of int
            The infection time(s) of this ``ContactNetworkNode'' object
        '''
        pass

    @abc.abstractmethod
    def infect(self, time, sequence):
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