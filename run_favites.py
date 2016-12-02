#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Viewer": Command Line Interface for FAVITES
'''
import argparse                                   # to parse user arguments
from os.path import expanduser                    # to open paths with '~'
from sys import stdout,stdin                      # standard input/output
import FAVITES_Global                             # for global access variables
from ContactNetwork import ContactNetwork         # ContactNetwork module abstract class
from ContactNetworkNode import ContactNetworkNode # ContactNetworkNode module abstract class
from Driver import Driver                         # Driver module abstract class
from EndCriteria import EndCriteria               # EndCriteria module abstract class
from NodeEvolution import NodeEvolution           # NodeEvolution module abstract class
from SeedSelection import SeedSelection           # SeedSelection module abstract class
from SeedSequence import SeedSequence             # SeedSequence module abstract class
from Tree import Tree                             # Tree module abstract class

# default settings
def_ContactNetworkFile   = 'stdin'
def_ContactNetworkModule = 'NetworkX'
def_DriverModule         = 'Default'
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

    parser.add_argument('--EndTime',
        default=None, type=int,
        help="End time stopping criterion of simulation. Needed for EndCriteria_Time")

    parser.add_argument('--EndTransmissions',
        default=None, type=int,
        help="Number of transmission events stopping criterion of simulation. Needed for EndCriteria_Transmissions")

    parser.add_argument('--ContactNetworkModule',
        default=def_ContactNetworkModule,
        choices=FAVITES_Global.list_modules['ContactNetwork'],
        help="ContactNetwork module implementation")

    parser.add_argument('--DriverModule',
        default=def_DriverModule,
        choices=FAVITES_Global.list_modules['Driver'],
        help="Driver module implementation")

    parser.add_argument('--EndCriteriaModule',
        required=True,
        choices=FAVITES_Global.list_modules['EndCriteria'],
        help="Simulation ending criteria")

    parser.add_argument('--NodeEvolutionModule',
        default=def_NodeEvolutionModule,
        choices=FAVITES_Global.list_modules['NodeEvolution'],
        help="NodeEvolution module implementation")

    parser.add_argument('--SeedSelectionModule',
        default=def_SeedSelectionModule,
        choices=FAVITES_Global.list_modules['SeedSelection'],
        help="SeedSelection module implementation")

    parser.add_argument('--SeedSequenceLength',
        default=def_SeedSequenceLength, type=int,
        help="Length of seed sequences")

    parser.add_argument('--SeedSequenceModule',
        default=def_SeedSequenceModule,
        choices=FAVITES_Global.list_modules['SeedSequence'],
        help="SeedSequence module implementation")

    parser.add_argument('--TreeModule',
        default=def_TreeModule,
        choices=FAVITES_Global.list_modules['Tree'],
        help="Tree module implementation")

    args = parser.parse_args()

    # import modules and store in global access variables
    print("=============================   Modules   =============================")

    # import ContactNetwork module
    print("ContactNetwork Module: ", end='')
    stdout.flush()
    if args.ContactNetworkModule == 'NetworkX':
        from ContactNetwork_NetworkX import ContactNetwork_NetworkX as module_ContactNetwork
    else:
        print('\n')
        print("ERROR: Invalid choice for ContactNetworkModule: %r" % args.ContactNetworkModule)
        exit(-1)
    assert issubclass(module_ContactNetwork, ContactNetwork), "%r is not a ContactNetwork" % module_ContactNetwork
    print(args.ContactNetworkModule)
    FAVITES_Global.modules['ContactNetwork'] = module_ContactNetwork

    # import Driver module
    print("Driver         Module: ", end='')
    stdout.flush()
    if args.DriverModule == 'Default':
        from Driver_Default import Driver_Default as module_Driver
    else:
        print('\n')
        print("ERROR: Invalid choice for DriverModule: %r" % args.DriverModule)
        exit(-1)
    assert issubclass(module_Driver, Driver), "%r is not a Driver" % module_Driver
    print(args.DriverModule)
    FAVITES_Global.modules['Driver'] = module_Driver

    # import EndCriteria module
    print("EndCriteria    Module: ", end='')
    stdout.flush()
    if args.EndCriteriaModule == 'Time':
        if args.EndTime == None:
            print('\n')
            print("ERROR: EndCriteria_Time requires --EndTime stopping criterion")
            exit(-1)
        else:
            FAVITES_Global.end_time = args.EndTime
        if args.EndTransmissions != None:
            print('\n')
            print("ERROR: --EndTransmissions was specified for EndCriteria_Time. Only use --EndTime")
            exit(-1)
        from EndCriteria_Time import EndCriteria_Time as module_EndCriteria
    elif args.EndCriteriaModule == 'Transmissions':
        if args.EndTransmissions == None:
            print('\n')
            print("ERROR: EndCriteria_Transmissions requires --EndTransmissions stopping criterion")
            exit(-1)
        else:
            FAVITES_Global.end_transmissions = args.EndTransmissions
        if args.EndTime != None:
            print('\n')
            print("ERROR: --EndTime was specified for EndCriteria_Transmissions. Only use --EndTransmissions")
            exit(-1)
        from EndCriteria_Transmissions import EndCriteria_Transmissions as module_EndCriteria
    else:
        print('\n')
        print("ERROR: Invalid choice for EndCriteriaModule: %r" % args.EndCriteriaModule)
        exit(-1)
    module_EndCriteria() # to force Python to check method implementations
    assert issubclass(module_EndCriteria, EndCriteria), "%r is not an EndCriteria" % module_EndCriteria
    print(args.EndCriteriaModule)
    FAVITES_Global.modules['EndCriteria'] = module_EndCriteria

    # import NodeEvolution module
    print("NodeEvolution  Module: ", end='')
    stdout.flush()
    if args.NodeEvolutionModule == 'Dummy':
        from NodeEvolution_Dummy import NodeEvolution_Dummy as module_NodeEvolution
    else:
        print('\n')
        print("ERROR: Invalid choice for NodeEvolutionModule: %r" % args.NodeEvolutionModule)
        exit(-1)
    module_NodeEvolution() # to force Python to check method implementations
    assert issubclass(module_NodeEvolution, NodeEvolution), "%r is not a NodeEvolution" % module_NodeEvolution
    print(args.NodeEvolutionModule)
    FAVITES_Global.modules['NodeEvolution'] = module_NodeEvolution

    # import SeedSelection module
    print("SeedSelection  Module: ", end='')
    stdout.flush()
    if args.SeedSelectionModule == 'Random':
        from SeedSelection_Random import SeedSelection_Random as module_SeedSelection
    else:
        print('\n')
        print("ERROR: Invalid choice for SeedSelectionModule: %r" % args.SeedSelectionModule)
        exit(-1)
    module_SeedSelection() # to force Python to check method implementations
    assert issubclass(module_SeedSelection, SeedSelection), "%r is not a SeedSelection" % module_SeedSelection
    print(args.SeedSelectionModule)
    FAVITES_Global.modules['SeedSelection'] = module_SeedSelection

    # import SeedSequence module
    print("SeedSequence   Module: ", end='')
    stdout.flush()
    if args.SeedSequenceModule == 'Random':
        from SeedSequence_Random import SeedSequence_Random as module_SeedSequence
    else:
        print('\n')
        print("ERROR: Invalid choice for SeedSequenceModule: %r" % args.SeedSequenceModule)
        exit(-1)
    module_SeedSequence() # to force Python to check method implementations
    assert issubclass(module_SeedSequence, SeedSequence), "%r is not a SeedSequence" % module_SeedSequence
    print(args.SeedSequenceModule)
    FAVITES_Global.modules['SeedSequence'] = module_SeedSequence

    # import Tree module
    print("Tree           Module: ", end='')
    stdout.flush()
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
    stdout.flush()
    if args.ContactNetworkFile == 'stdin':
        print('standard input...', end='')
        stdout.flush()
        FAVITES_Global.edge_list = [i.strip() for i in stdin if len(i.strip()) > 0]
    else:
        if args.ContactNetworkFile[0] == '~':
            args.ContactNetworkFile = expanduser(args.ContactNetworkFile)
        print('%r...' % args.ContactNetworkFile, end='')
        stdout.flush()
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
    FAVITES_Global.modules['Driver'].run()