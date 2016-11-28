#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Driver" module
'''
import argparse # to parse user arguments
from ContactNetwork import ContactNetwork

def parseArgs():
    '''
    Parse user arguments
    '''

    # use argparse to parse user arguments
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--ContactNetworkModule', default='NetworkX', help='ContactNetwork module implementation')
    args = parser.parse_args()

    # import modules
    print("=== Modules ===")

    # import ContactNetwork module
    print("ContactNetwork Module: ", end='')
    if args.ContactNetworkModule == 'NetworkX':
        global module_ContactNetwork
        from ContactNetwork_NetworkX import ContactNetwork_NetworkX as module_ContactNetwork
        assert issubclass(module_ContactNetwork, ContactNetwork), "%r is not a ContactNetwork" % module_ContactNetwork
        print("NetworkX")

if __name__ == "__main__":
    '''
    Simulation driver
    '''

    # parse user arguments
    parseArgs()

    # create ContactNetwork object
    #contact_network = module_ContactNetwork()