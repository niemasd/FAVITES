#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Viewer": Command Line Interface for FAVITES
'''
import argparse                                           # to parse user arguments
from os.path import expanduser                            # to open paths with '~'
from sys import stdout,stdin                              # standard input/output
import FAVITES_Global                                     # for global access variables
from ContactNetwork import ContactNetwork                 # ContactNetwork module abstract class
from ContactNetworkNode import ContactNetworkNode         # ContactNetworkNode module abstract class
from Driver import Driver                                 # Driver module abstract class
from EndCriteria import EndCriteria                       # EndCriteria module abstract class
from NodeEvolution import NodeEvolution                   # NodeEvolution module abstract class
from PostValidation import PostValidation                 # PostValidation module abstract class
from SeedSelection import SeedSelection                   # SeedSelection module abstract class
from SeedSequence import SeedSequence                     # SeedSequence module abstract class
from SourceSample import SourceSample                     # SourceSample module abstract class
from TransmissionNodeSample import TransmissionNodeSample # TransmissionNodeSample module abstract class
from TransmissionTimeSample import TransmissionTimeSample # TransmissionTimeSample module abstract class
from Tree import Tree                                     # Tree module abstract class

# default settings
def_ContactNetworkFile           = 'stdin'
def_ContactNetworkModule         = 'NetworkX'
def_DriverModule                 = 'Default'
def_NodeEvolutionModule          = 'Dummy' # TODO: Create actual NodeEvolution module implementation
def_PostValidationModule         = 'Dummy' # TODO: Create actual PostValidation module implementation
def_SeedSelectionModule          = 'Random'
def_SeedSequenceLength           = 100
def_SeedSequenceModule           = 'Random'
def_SourceSampleModule           = 'Dummy' # TODO: Create actual SourceSample module implementation
def_TransmissionNodeSampleModule = 'Random'
def_TransmissionTimeSampleModule = 'Fixed'
def_TreeModule                   = 'DendroPy'

def printMessage():
    '''
    Print author message
    '''
    print("/---------------------------------------------------------------------\\")
    print("| FAVITES - FrAmework for VIral Transmission and Evolution Simulation |")
    print("|                        Moshiri & Mirarab 2016                       |")
    print("\\---------------------------------------------------------------------/")

def check_geZero(t):
    '''
    Check if t is an integer >= 0

    Parameters
    ----------
    t : int
        Variable to check
    '''
    try:
        t = int(t)
    except:
        raise argparse.ArgumentTypeError("invalid int value: %r" % t)
    if t < 0:
        raise argparse.ArgumentTypeError("%s is not >= 0" % t)
    return t

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
        default=None, type=check_geZero,
        help="End time stopping criterion of simulation")

    parser.add_argument('--EndTransmissions',
        default=None, type=check_geZero,
        help="Number of transmission events stopping criterion of simulation")

    parser.add_argument('--FixedTransmissionTimeDelta',
        default=None, type=check_geZero,
        help="Time delta for fixed transmission time sampling")

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

    parser.add_argument('--PostValidationModule',
        default=def_PostValidationModule,
        choices=FAVITES_Global.list_modules['PostValidation'],
        help="PostValidation module implementation")

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

    parser.add_argument('--SourceSampleModule',
        default=def_SourceSampleModule,
        choices=FAVITES_Global.list_modules['SourceSample'],
        help="SourceSample module implementation")

    parser.add_argument('--TransmissionNodeSampleModule',
        default=def_TransmissionNodeSampleModule,
        choices=FAVITES_Global.list_modules['TransmissionNodeSample'],
        help="TransmissionNodeSample module implementation")

    parser.add_argument('--TransmissionTimeSampleModule',
        default=def_TransmissionTimeSampleModule,
        choices=FAVITES_Global.list_modules['TransmissionTimeSample'],
        help="TransmissionTimeSample module implementation")

    parser.add_argument('--TreeModule',
        default=def_TreeModule,
        choices=FAVITES_Global.list_modules['Tree'],
        help="Tree module implementation")

    args = parser.parse_args()

    # import modules and store in global access variables
    print("=============================   Modules   =============================")

    # import ContactNetwork module
    print("ContactNetwork Module:         ", end='')
    if args.ContactNetworkModule == 'NetworkX':
        from ContactNetwork_NetworkX import ContactNetwork_NetworkX as module_ContactNetwork
    else:
        print('\n')
        print("ERROR: Invalid choice for ContactNetworkModule: %r" % args.ContactNetworkModule)
        exit(-1)
    print(args.ContactNetworkModule)
    assert issubclass(module_ContactNetwork, ContactNetwork), "%r is not a ContactNetwork" % module_ContactNetwork
    FAVITES_Global.modules['ContactNetwork'] = module_ContactNetwork

    # import Driver module
    print("Driver                 Module: ", end='')
    if args.DriverModule == 'Default':
        from Driver_Default import Driver_Default as module_Driver
    else:
        print('\n')
        print("ERROR: Invalid choice for DriverModule: %r" % args.DriverModule)
        exit(-1)
    print(args.DriverModule)
    assert issubclass(module_Driver, Driver), "%r is not a Driver" % module_Driver
    FAVITES_Global.modules['Driver'] = module_Driver

    # import EndCriteria module
    print("EndCriteria            Module: ", end='')
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
    elif args.EndCriteriaModule == 'FirstTimeTransmissions':
        if args.EndTime == None:
            print('\n')
            print("ERROR: EndCriteria_FirstTimeTransmissions requires both --EndTime and --EndTransmissions stopping criteria")
            exit(-1)
        else:
            FAVITES_Global.end_time = args.EndTime
        if args.EndTransmissions == None:
            print('\n')
            print("ERROR: EndCriteria_FirstTimeTransmissions requires both --EndTime and --EndTransmissions stopping criteria")
            exit(-1)
        else:
            FAVITES_Global.end_transmissions = args.EndTransmissions
        from EndCriteria_FirstTimeTransmissions import EndCriteria_FirstTimeTransmissions as module_EndCriteria
    else:
        print('\n')
        print("ERROR: Invalid choice for EndCriteriaModule: %r" % args.EndCriteriaModule)
        exit(-1)
    print(args.EndCriteriaModule)
    module_EndCriteria() # to force Python to check method implementations
    assert issubclass(module_EndCriteria, EndCriteria), "%r is not an EndCriteria" % module_EndCriteria
    FAVITES_Global.modules['EndCriteria'] = module_EndCriteria

    # import NodeEvolution module
    print("NodeEvolution          Module: ", end='')
    if args.NodeEvolutionModule == 'Dummy':
        from NodeEvolution_Dummy import NodeEvolution_Dummy as module_NodeEvolution
    else:
        print('\n')
        print("ERROR: Invalid choice for NodeEvolutionModule: %r" % args.NodeEvolutionModule)
        exit(-1)
    module_NodeEvolution() # to force Python to check method implementations
    print(args.NodeEvolutionModule)
    assert issubclass(module_NodeEvolution, NodeEvolution), "%r is not a NodeEvolution" % module_NodeEvolution
    FAVITES_Global.modules['NodeEvolution'] = module_NodeEvolution

    # import PostValidation module
    print("PostValidation         Module: ", end='')
    if args.PostValidationModule == 'Dummy':
        from PostValidation_Dummy import PostValidation_Dummy as module_PostValidation
    else:
        print('\n')
        print("ERROR: Invalid choice for PostValidationModule: %r" % args.PostValidationModule)
        exit(-1)
    module_PostValidation() # to force Python to check method implementations
    print(args.PostValidationModule)
    assert issubclass(module_PostValidation, PostValidation), "%r is not a PostValidation" % module_PostValidation
    FAVITES_Global.modules['PostValidation'] = module_PostValidation

    # import SeedSelection module
    print("SeedSelection          Module: ", end='')
    if args.SeedSelectionModule == 'Random':
        from SeedSelection_Random import SeedSelection_Random as module_SeedSelection
    else:
        print('\n')
        print("ERROR: Invalid choice for SeedSelectionModule: %r" % args.SeedSelectionModule)
        exit(-1)
    module_SeedSelection() # to force Python to check method implementations
    print(args.SeedSelectionModule)
    assert issubclass(module_SeedSelection, SeedSelection), "%r is not a SeedSelection" % module_SeedSelection
    FAVITES_Global.modules['SeedSelection'] = module_SeedSelection

    # import SeedSequence module
    print("SeedSequence           Module: ", end='')
    if args.SeedSequenceModule == 'Random':
        from SeedSequence_Random import SeedSequence_Random as module_SeedSequence
    else:
        print('\n')
        print("ERROR: Invalid choice for SeedSequenceModule: %r" % args.SeedSequenceModule)
        exit(-1)
    module_SeedSequence() # to force Python to check method implementations
    print(args.SeedSequenceModule)
    assert issubclass(module_SeedSequence, SeedSequence), "%r is not a SeedSequence" % module_SeedSequence
    FAVITES_Global.modules['SeedSequence'] = module_SeedSequence

    # import SourceSample module
    print("SourceSample           Module: ", end='')
    if args.SourceSampleModule == 'Dummy':
        from SourceSample_Dummy import SourceSample_Dummy as module_SourceSample
    else:
        print('\n')
        print("ERROR: Invalid choice for SourceSampleModule: %r" % args.SourceSampleModule)
        exit(-1)
    module_SourceSample() # to force Python to check method implementations
    print(args.SourceSampleModule)
    assert issubclass(module_SourceSample, SourceSample), "%r is not a SourceSample" % module_SourceSample
    FAVITES_Global.modules['SourceSample'] = module_SourceSample

    # import TransmissionNodeSample module
    print("TransmissionNodeSample Module: ", end='')
    if args.TransmissionNodeSampleModule == 'Random':
        from TransmissionNodeSample_Random import TransmissionNodeSample_Random as module_TransmissionNodeSample
    else:
        print('\n')
        print("ERROR: Invalid choice for TransmissionNodeSampleModule: %r" % args.TransmissionNodeSampleModule)
        exit(-1)
    print(args.TransmissionNodeSampleModule)
    module_TransmissionNodeSample() # to force Python to check method implementations
    assert issubclass(module_TransmissionNodeSample, TransmissionNodeSample), "%r is not a TransmissionNodeSample" % module_TransmissionNodeSample
    FAVITES_Global.modules['TransmissionNodeSample'] = module_TransmissionNodeSample

    # import TransmissionTimeSample module
    print("TransmissionTimeSample Module: ", end='')
    if args.TransmissionTimeSampleModule == 'Fixed':
        if args.FixedTransmissionTimeDelta == None:
            print('\n')
            print("ERROR: TransmissionTimeSample_Fixed requires --FixedTransmissionTimeDelta")
            exit(-1)
        else:
            FAVITES_Global.fixed_transmission_time_delta = args.FixedTransmissionTimeDelta
        from TransmissionTimeSample_Fixed import TransmissionTimeSample_Fixed as module_TransmissionTimeSample
    else:
        print('\n')
        print("ERROR: Invalid choice for TransmissionTimeSampleModule: %r" % args.TransmissionTimeSampleModule)
        exit(-1)
    print(args.TransmissionTimeSampleModule)
    module_TransmissionTimeSample() # to force Python to check method implementations
    assert issubclass(module_TransmissionTimeSample, TransmissionTimeSample), "%r is not a TransmissionTimeSample" % module_TransmissionTimeSample
    FAVITES_Global.modules['TransmissionTimeSample'] = module_TransmissionTimeSample

    # import Tree module
    print("Tree                   Module: ", end='')
    if args.TreeModule == 'DendroPy':
        from Tree_DendroPy import Tree_DendroPy as module_Tree
    else:
        print('\n')
        print("ERROR: Invalid choice for TreeModule: %r" % args.TreeModule)
        exit(-1)
    print(args.TreeModule)
    assert issubclass(module_Tree, Tree), "%r is not a Tree" % module_Tree
    FAVITES_Global.modules['Tree'] = module_Tree

    print()

    # read input data
    print("============================   User Data   ============================")

    # read in Contact Network and add to input data
    print("Reading contact network from ", end='')
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