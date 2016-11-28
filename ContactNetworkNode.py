#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworNode" module
'''
import abc # for abstraction

class ContactNetworkNode(metaclass=abc.ABCMeta):
    '''
    Abstract class defining a ``ContactNetworkNode`` object

    Methods
    -------
    get_name()
        Return the name of this ``ContactNetworkNode'' object
    get_attribute()
        Return the attribute of this ``ContactNetworkNode'' object

    '''

    @abc.abstractmethod
    def get_name(self):
        '''
        Return the name of this ``ContactNetworkNode'' object

        '''
        pass

    @abc.abstractmethod
    def get_attribute(self):
        '''
        Return the attribute of this ``ContactNetworkNode'' object

        '''
        pass