#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Viewer": Command Line Interface for FAVITES
'''
import argparse                                   # to parse user arguments
from os.path import expanduser                    # to open paths with '~'
import FAVITES_Global                             # for global access variables
import Driver_Default                             # default Driver module
from ContactNetwork import ContactNetwork         # ContactNetwork module abstract class
from ContactNetworkNode import ContactNetworkNode # ContactNetworkNode module abstract class
from NodeEvolution import NodeEvolution           # NodeEvolution module abstract class
from SeedSelection import SeedSelection           # SeedSelection module abstract class
from SeedSequence import SeedSequence             # SeedSequence module abstract class
from Tree import Tree                             # Tree module abstract class

# default settings
def_ContactNetworkFile   = 'stdin'
def_ContactNetworkModule = 'NetworkX'
def_NodeEvolutionModule  = 'Dummy' # TODO: Create actual NodeEvolution module implementation
def_SeedSelectionModule  = 'Random'
def_SeedSequenceLength   = 100
def_SeedSequenceModule   = 'Random'
def_TreeModule           = 'DendroPy'

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
    Parse user arguments. As a developer, if you create any of your own module
    implementations, you should modify the corresponding module argument parser
    and "import ____ module" section of this function accordingly.

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

    parser.add_argument('--NodeEvolutionModule',
        default=def_NodeEvolutionModule,
        help="NodeEvolution module implementation")

    parser.add_argument('--SeedSelectionModule',
        default=def_SeedSelectionModule,
        help="SeedSelection module implementation")

    parser.add_argument('--SeedSequenceLength',
        default=def_SeedSequenceLength, type=int,
        help="Length of seed sequences")

    parser.add_argument('--SeedSequenceModule',
        default=def_SeedSequenceModule,
        help="SeedSequence module implementation")

    parser.add_argument('--TreeModule',
        default=def_TreeModule,
        help="Tree module implementation")

    args = parser.parse_args()

    # import modules and store in global access variables
    print("=============================   Modules   =============================")

    # import ContactNetwork module
    print("ContactNetwork Module: ", end='')
    global module_ContactNetwork
    if args.ContactNetworkModule == 'NetworkX':
        from ContactNetwork_NetworkX import ContactNetwork_NetworkX as module_ContactNetwork
    else:
        print('\n')
        print("ERROR: Invalid choice for ContactNetworkModule: %r" % args.ContactNetworkModule)
        exit(-1)
    assert issubclass(module_ContactNetwork, ContactNetwork), "%r is not a ContactNetwork" % module_ContactNetwork
    print(args.ContactNetworkModule)
    FAVITES_Global.modules['ContactNetwork'] = module_ContactNetwork

    # import NodeEvolution module
    print("NodeEvolution  Module: ", end='')
    global module_NodeEvolution
    if args.NodeEvolutionModule == 'Dummy':
        from NodeEvolution_Dummy import NodeEvolution_Dummy as module_NodeEvolution
    else:
        print('\n')
        print("ERROR: Invalid choice for NodeEvolutionModule: %r" % args.NodeEvolutionModule)
        exit(-1)
    assert issubclass(module_NodeEvolution, NodeEvolution), "%r is not a NodeEvolution" % module_NodeEvolution
    print(args.NodeEvolutionModule)
    FAVITES_Global.modules['NodeEvolution'] = module_NodeEvolution

    # import SeedSelection module
    print("SeedSelection  Module: ", end='')
    global module_SeedSelection
    if args.SeedSelectionModule == 'Random':
        from SeedSelection_Random import SeedSelection_Random as module_SeedSelection
        module_SeedSelection() # to force Python to check method implementations
    else:
        print('\n')
        print("ERROR: Invalid choice for SeedSelectionModule: %r" % args.SeedSelectionModule)
        exit(-1)
    assert issubclass(module_SeedSelection, SeedSelection), "%r is not a SeedSelection" % module_SeedSelection
    print(args.SeedSelectionModule)
    FAVITES_Global.modules['SeedSelection'] = module_SeedSelection

    # import SeedSequence module
    print("SeedSequence   Module: ", end='')
    global module_SeedSequence
    if args.SeedSequenceModule == 'Random':
        from SeedSequence_Random import SeedSequence_Random as module_SeedSequence
        module_SeedSequence() # to force Python to check method implementations
    else:
        print('\n')
        print("ERROR: Invalid choice for SeedSequenceModule: %r" % args.SeedSequenceModule)
        exit(-1)
    assert issubclass(module_SeedSequence, SeedSequence), "%r is not a SeedSequence" % module_SeedSequence
    print(args.SeedSequenceModule)
    FAVITES_Global.modules['SeedSequence'] = module_SeedSequence

    # import Tree module
    print("Tree           Module: ", end='')
    global module_Tree
    if args.TreeModule == 'DendroPy':
        from Tree_DendroPy import Tree_DendroPy as module_Tree
    else:
        print('\n')
        print("ERROR: Invalid choice for TreeModule: %r" % args.TreeModule)
        exit(-1)
    assert issubclass(module_Tree, Tree), "%r is not a Tree" % module_Tree
    print(args.TreeModule)
    FAVITES_Global.modules['Tree'] = module_Tree

    print()

    # read input data
    print("============================   User Data   ============================")

    # read in Contact Network and add to input data
    print("Reading contact network from ", end='')
    if args.ContactNetworkFile == 'stdin':
        print('standard input...', end='')
        import sys
        FAVITES_Global.edge_list = [i.strip() for i in sys.stdin if len(i.strip()) > 0]
    else:
        if args.ContactNetworkFile[0] == '~':
            args.ContactNetworkFile = expanduser(args.ContactNetworkFile)
        print('%r...' % args.ContactNetworkFile, end='')
        FAVITES_Global.edge_list = [i.strip() for i in open(args.ContactNetworkFile) if len(i.strip()) > 0]
    print(' done')

    # add number of seed nodes to input data
    FAVITES_Global.num_seeds = args.NumSeeds
    print("Number of seed nodes: %d" % args.NumSeeds)

    # # add seed sequence length to input data
    FAVITES_Global.seed_sequence_length = args.SeedSequenceLength
    print("Seed sequence length: %d" % args.SeedSequenceLength)

    # return input data
    print()

if __name__ == "__main__":
    # print author message
    printMessage()
    print()

    # initialize global access variables
    FAVITES_Global.init()

    # parse user arguments
    parseArgs()

    # run Driver
    Driver_Default.run()