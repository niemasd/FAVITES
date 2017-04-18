#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkGenerator" module, where the contact network edge list is loaded
from a file
'''
from ContactNetworkGenerator import ContactNetworkGenerator
import FAVITES_GlobalContext as GC
from os.path import expanduser

class ContactNetworkGenerator_File(ContactNetworkGenerator):
    def init():
        pass

    def get_edge_list():
        return [i.strip() for i in open(expanduser(GC.contact_network_file)) if len(i.strip()) > 0]