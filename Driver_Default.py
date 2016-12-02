#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Driver" module
'''
import FAVITES_Global                             # for global access variables
from Driver import Driver                         # Driver module abstract class
from ContactNetwork import ContactNetwork         # ContactNetwork module abstract class
from ContactNetworkNode import ContactNetworkNode # ContactNetworkNode module abstract class
from NodeEvolution import NodeEvolution           # NodeEvolution module abstract class
from SeedSelection import SeedSelection           # SeedSelection module abstract class
from SeedSequence import SeedSequence             # SeedSequence module abstract class
from Tree import Tree                             # Tree module abstract class
from sys import stdout                            # to flush print buffer

class Driver_Default(Driver):
    def run():
        '''
        Simulation driver. Even if you add your own modules, you probably shouldn't
        need to modify this function. The one clear exception would be if your
        module requires additional user input (e.g. custom evolution model modules),
        which would then require you to call it with the required arguments.
        '''

        # begin simulation
        print("===========================   Simulations   ===========================")

        # create ContactNetwork object from input contact network edge list
        print("Creating ContactNetwork object...", end='')
        stdout.flush()
        contact_network = FAVITES_Global.modules['ContactNetwork'](FAVITES_Global.edge_list)
        assert isinstance(contact_network, ContactNetwork), "contact_network is not a ContactNetwork object"
        FAVITES_Global.contact_network = contact_network
        print(" done")

        # select seed nodes
        print("Selecting seed nodes...", end='')
        stdout.flush()
        seed_nodes = FAVITES_Global.modules['SeedSelection'].select_seed_nodes()
        assert isinstance(seed_nodes, list), "seed_nodes is not a list"
        for node in seed_nodes:
            assert isinstance(node, ContactNetworkNode), "seed_nodes contains items that are not ContactNetworkNode objects"
        assert len(seed_nodes) == FAVITES_Global.num_seeds, "seed_nodes contains a different number of nodes than NumSeeds"
        print(" done")

        # infect seed nodes
        print("Infecting seed nodes...", end='')
        stdout.flush()
        for node in seed_nodes:
            seq = FAVITES_Global.modules['SeedSequence'].generate()
            node.infect(0,seq)
            FAVITES_Global.contact_network.add_to_infected(node)
        print(" done")

        # iterative step of transmissions
        print("Performing transmission simulations...", end='')
        stdout.flush()
        while FAVITES_Global.modules['EndCriteria'].not_done():
            u,v = FAVITES_Global.modules['TransmissionNodeSample'].sample_nodes()
            t = FAVITES_Global.modules['TransmissionTimeSample'].sample_time(u,v)
            assert t >= FAVITES_Global.time, "Transmission cannot go back in time!"
            FAVITES_Global.time = t
            FAVITES_Global.modules['NodeEvolution'].evolve_to_current_time(u)
            seq = FAVITES_Global.modules['SourceSample'].sample_virus(u)
            v.infect(FAVITES_Global.time, seq)
            FAVITES_Global.contact_network.add_transmission(u,v,t)
        print(" done")