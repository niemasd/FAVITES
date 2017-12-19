#! /usr/bin/env python3
'''
Niema Moshiri 2016

"ContactNetworkGenerator" module, where the contact network edge list is loaded
from a file as a binary adjacency matrix where each line is a row and columns
are separated by a user-specified delimiter. Comment lines (starting with '#')
and empty lines are ignored.
'''
from ContactNetworkGenerator import ContactNetworkGenerator
import FAVITES_GlobalContext as GC
from os.path import expanduser

class ContactNetworkGenerator_FileAdjacencyMatrix(ContactNetworkGenerator):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        assert isinstance(GC.contact_network_delimiter, str), "Contact Network Adjacency Matrix delimiter must be a string"

    def get_edge_list():
        lines = [i.strip() for i in open(expanduser(GC.contact_network_file)) if len(i.strip()) > 0 and i.strip()[0] != '#']
        out = ["NODE\t%d\t." % i for i in range(len(lines))]
        for i in range(len(lines)):
            parts = lines[i].split(GC.contact_network_delimiter)
            assert len(parts) == len(lines), "The number of rows and columns must be the same"
            for j in range(len(parts)):
                if parts[j] == '1':
                    out.append("EDGE\t%s\t%s\t.\t%s" % (str(i),str(j),'d'))
                else:
                    assert parts[j] == '0', "Invalid matrix element. Must only contain 1s and 0s"
        return out