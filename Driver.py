#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Driver" module
'''
import argparse                                   # to parse user arguments
from ContactNetwork import ContactNetwork         # ContactNetwork module abstract class
from ContactNetworkNode import ContactNetworkNode # ContactNetworkNode module abstract class
from SeedSelection import SeedSelection           # SeedSelection module abstract class

# default settings
def_ContactNetworkFile   = 'stdin'
def_ContactNetworkModule = 'NetworkX'
def_SeedSelectionModule  = 'Random'
def_SeedSequenceModule   = 'FILL THIS' #TODO FILL THIS!!!

def printMessage():
    '''
    Print author message
    '''
    print("/---------------------------------------------------------------------\\")
    print("| FAVITES - FrAmework for VIral Transmission and Evolution Simulation |")
    print("|                        Moshiri & Mirarab 2016                       |")
    print("\\---------------------------------------------------------------------/")

def parseArgs():
    '''
    Parse user arguments

    Returns
    -------
    user_input : list of user inputs
        * ``user_input['contact_network']'': Input contact network (edge list)

    '''

    # use argparse to parse user arguments
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--ContactNetworkFile',
        default=def_ContactNetworkFile,
        help="Input contact network ('stdin' for standard input)")

    parser.add_argument('--NumSeeds',
        required=True, type=int,
        help="Number of seed infection nodes desired")

    parser.add_argument('--ContactNetworkModule',
        default=def_ContactNetworkModule,
        help="ContactNetwork module implementation")

    parser.add_argument('--SeedSelectionModule',
        default=def_SeedSelectionModule,
        help="SeedSelection module implementation")

    parser.add_argument('--SeedSequenceModule',
        default=def_SeedSequenceModule,
        help="SeedSequence module implementation")
        
    args = parser.parse_args()

    # import modules
    print("=== Modules ===")

    # import ContactNetwork module
    print("ContactNetwork Module: ", end='')
    if args.ContactNetworkModule == 'NetworkX':
        global module_ContactNetwork
        from ContactNetwork_NetworkX import ContactNetwork_NetworkX as module_ContactNetwork
    else:
        print('\n')
        print("ERROR: Invalid choice for ContactNetworkModule: %r" % args.ContactNetworkModule)
        exit(-1)
    assert issubclass(module_ContactNetwork, ContactNetwork), "%r is not a ContactNetwork" % module_ContactNetwork
    print(args.ContactNetworkModule)

    # import SeedSelection module
    print("SeedSelection Module:  ", end='')
    if args.SeedSelectionModule == 'Random':
        global module_SeedSelection
        from SeedSelection_Random import SeedSelection_Random as module_SeedSelection
        module_SeedSelection() # to force Python to check method implementations
    else:
        print('\n')
        print("ERROR: Invalid choice for SeedSelectionModule: %r" % args.SeedSelectionModule)
        exit(-1)
    assert issubclass(module_SeedSelection, SeedSelection), "%r is not a SeedSelection" % module_SeedSelection
    print(args.SeedSelectionModule)

    # import SeedSequence module
    '''
    print("SeedSequence Module:  ", end='')
    if args.SeedSequenceModule == 'FILL THIS': # TODO FILL THIS!!!!!!!
        global module_SeedSequence
        from SeedSequence_FILLTHIS import SeedSequence_FILLTHIS as module_SeedSequence # TODO FILL THIS!!!!!
        module_SeedSequence() # to force Python to check method implementations
    else:
        print('\n')
        print("ERROR: Invalid choice for SeedSelectionModule: %r" % args.SeedSelectionModule)
        exit(-1)
    assert issubclass(module_SeedSelection, SeedSelection), "%r is not a SeedSelection" % module_SeedSelection
    print(args.SeedSelectionModule)
    '''

    print()

    # read input data
    print("=== Input Data ===")
    user_input = {}

    # read in Contact Network and add to input data
    print("Reading contact network from: ", end='')
    user_input['contact_network'] = []
    if args.ContactNetworkFile == 'stdin':
        import sys
        user_input['contact_network'] = [i.strip() for i in sys.stdin if len(i.strip()) > 0]
        print('standard input')
    else:
        user_input['contact_network'] = open(args.ContactNetworkFile).readlines()
        print(args.ContactNetworkFile)

    # add number of seed nodes to input data
    user_input['num_seeds'] = args.NumSeeds

    # return input data
    return user_input

if __name__ == "__main__":
    '''
    Simulation driver
    '''

    # print author message
    printMessage()
    print()

    # parse user arguments
    user_input = parseArgs()

    # create ContactNetwork object from input contact network edge list
    contact_network = module_ContactNetwork(user_input['contact_network'])
    assert isinstance(contact_network, ContactNetwork), "contact_network is not a ContactNetwork object"

    # select seed nodes
    seed_nodes = module_SeedSelection.select_seed_nodes(user_input['num_seeds'],
        contact_network)
    assert isinstance(seed_nodes, list), "seed_nodes is not a list"
    for node in seed_nodes:
        assert isinstance(node, ContactNetworkNode), "seed_nodes contains items that are not ContactNetworkNode objects"
    assert len(seed_nodes) == user_input['num_seeds'], "seed_nodes contains more than NumSeeds nodes"

    # evolve phylogeny + sequences on each seed node
    '''
    for node in seed_nodes:
        SeedSequence.evolve(node)
    '''