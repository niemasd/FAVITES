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
        lines = [i.strip() for i in open(expanduser(GC.contact_network_file)) if len(i.strip()) > 0 and i.strip()[0] != '#']
        for line in lines:
            parts = [e.strip() for e in line.split()]
            assert parts[0] in {'NODE','EDGE'}, "Invalid contact network format. First column must be NODE or EDGE"
            if parts[0] == 'NODE':
                assert len(parts) == 3, "Invalid contact network format. NODE rows must have 3 columns"
            else:
                assert len(parts) == 5, "Invalid contact network format. EDGE rows must have 4 columns"
        return lines