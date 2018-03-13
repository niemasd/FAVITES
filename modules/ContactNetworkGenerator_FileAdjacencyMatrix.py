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
from gzip import open as gopen
from os.path import abspath,expanduser

class ContactNetworkGenerator_FileAdjacencyMatrix(ContactNetworkGenerator):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        assert isinstance(GC.contact_network_delimiter, str), "Contact Network Adjacency Matrix delimiter must be a string"
        GC.contact_network_file = abspath(expanduser((GC.contact_network_file)))

    def get_edge_list():
        if GC.contact_network_file.lower().endswith('.gz'):
            infile = gopen(GC.contact_network_file)
        else:
            infile = open(GC.contact_network_file)
        lines = [i.strip() for i in infile if len(i.strip()) > 0 and i.strip()[0] != '#']
        edges = set()
        out = ["NODE\t%d\t." % i for i in range(len(lines))]
        for i in range(len(lines)):
            if len(GC.contact_network_delimiter) == 0:
                parts = lines[i]
            else:
                parts = lines[i].split(GC.contact_network_delimiter)
            assert len(parts) == len(lines), "The number of rows and columns must be the same"
            for j in range(len(parts)):
                if parts[j] == '1':
                    edges.add((str(i),str(j)))
                else:
                    assert parts[j] == '0', "Invalid matrix element. Must only contain 1s and 0s"
        output_edges = []
        for u,v in edges:
            if (v,u) in edges:
                output_edges.append((str(min(u,v)),str(max(u,v)),'u'))
            else:
                output_edges.append((str(u),str(v),'d'))
        for e in sorted(output_edges):
            out.append("EDGE\t%s\t%s\t.\t%s" % e)
        f = gopen(expanduser("%s/contact_network.txt.gz" % GC.out_dir),'wb',9)
        f.write('\n'.join(out).encode()); f.write(b'\n')
        f.close()
        return out