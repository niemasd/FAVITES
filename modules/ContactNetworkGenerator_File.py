#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkGenerator" module, where the contact network edge list is loaded
from a file
'''
from ContactNetworkGenerator import ContactNetworkGenerator # abstract ContactNetworkGenerator class
import FAVITES_GlobalContext as GC
from os import path

class ContactNetworkGenerator_File(ContactNetworkGenerator):
    '''
    Implement the ``ContactNetworkGenerator'', loading the edge list from file
    '''

    def init():
        pass

    def get_edge_list():
        return [i.strip() for i in open(path.expanduser(GC.contact_network_file)) if len(i.strip()) > 0]