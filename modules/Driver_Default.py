#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Driver" module
'''
from modules import FAVITES_Global                        # for global access variables
from modules.Driver import Driver                         # Driver module abstract class
from modules.ContactNetwork import ContactNetwork         # ContactNetwork module abstract class
from modules.ContactNetworkNode import ContactNetworkNode # ContactNetworkNode module abstract class
from modules.NodeEvolution import NodeEvolution           # NodeEvolution module abstract class
from modules.NodeSample import NodeSample                 # NodeSample module abstract class
from modules.SeedSelection import SeedSelection           # SeedSelection module abstract class
from modules.SeedSequence import SeedSequence             # SeedSequence module abstract class
from modules.Tree import Tree                             # Tree module abstract class
import os                                                 # to write output files
from sys import stdout                                    # to flush print buffer

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
        orig_dir = os.getcwd()
        out_dir = FAVITES_Global.out_dir
        try:
            #os.makedirs(out_dir) # TODO UNCOMMENT WHEN DONE!!!
            pass # TODO REMOVE THIS WHEN DONE!!!
        except:
            print("ERROR: Unable to create output folder in current directory. Perhaps it already exists?")
            exit(-1)
        #os.chdir(out_dir) # TODO UNCOMMENT WHEN DONE!!!
        #os.makedirs("error_free_files") # TODO UNCOMMENT WHEN DONE!!!
        #os.makedirs("error_prone_files") # TODO UNCOMMENT WHEN DONE!!!

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

        # evolve all infected nodes to final time
        print("Evolving all nodes to final time...", end='')
        for node in FAVITES_Global.contact_network.get_infected_nodes():
            FAVITES_Global.modules['NodeEvolution'].evolve_to_current_time(node)
        print(" done")

        # output error-free files
        print("\n========================   Simulation Output   ========================")

        # post-validation of transmission network
        print("Scoring final transmission network...", end='')
        score = FAVITES_Global.modules['PostValidation'].score_transmission_network()
        print(" done")
        print("Transmission network had a final score of: %f" % score)

        # write transmission network as edge list
        print("Writing true transmission network to file...", end='')
        transmissions = FAVITES_Global.contact_network.get_transmissions()
        assert isinstance(transmissions, list), "get_transmissions() did not return a list!"
        for u,v,t in transmissions:
            assert isinstance(u, ContactNetworkNode), "get_transmissions() contains an invalid transmission event"
            assert isinstance(v, ContactNetworkNode), "get_transmissions() contains an invalid transmission event"
            assert isinstance(t, int), "get_transmissions() contains an invalid transmission event"
        true_transmission_network = '\n'.join([("%s\t%s\t%d" % e) for e in transmissions])
        #f = open('error_free_files/transmission_network.txt','w')
        #f.write(true_transmission_network)
        #f.close()
        print(" done")
        print("True transmission network was written to: %s/Output/error_free_files/transmission_network.txt" % orig_dir)

        # introduce real data artifacts
        print("\n=======================   Real Data Artifacts   =======================")

        # subsample the transmission network
        print("Subsampling transmission network...", end='')
        subsampled_transmissions = FAVITES_Global.modules['NodeSample'].subsample_transmission_network()
        for u,v,t in subsampled_transmissions:
            assert isinstance(u, ContactNetworkNode), "subsample_transmission_network() contains an invalid transmission event"
            assert isinstance(v, ContactNetworkNode), "subsample_transmission_network() contains an invalid transmission event"
            assert isinstance(t, int), "subsample_transmission_network() contains an invalid transmission event"
        print(" done")
        print("Writing subsampled transmission network to file...", end='')
        subsampled_transmission_network = '\n'.join([("%s\t%s\t%d" % e) for e in subsampled_transmissions])
        #f = open('error_prone_files/transmission_network.txt','w')
        #f.write(subsampled_transmission_network)
        #f.close()
        print(" done")
        print("Subsampled transmission network was written to: %s/Output/error_prone_files/transmission_network.txt" % orig_dir)

        # return to original directory
        os.chdir(orig_dir)