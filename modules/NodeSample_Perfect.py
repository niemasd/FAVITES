#! /usr/bin/env python3
'''
Niema Moshiri 2016

"NodeSample" module, perfect sampling
'''
from modules import FAVITES_Global        # for global access variables
from modules.NodeSample import NodeSample # abstract NodeSample class

class NodeSample_Perfect(NodeSample):
    def subsample_transmission_network():
        return FAVITES_Global.contact_network.get_transmissions()