#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Viewer": Command Line Interface for FAVITES
'''
import argparse                                           # to parse user arguments
import os                                                 # to handle file stuff
from sys import stdout,stdin                              # standard input/output
import FAVITES_Global                                     # for global access variables
from ContactNetwork import ContactNetwork                 # ContactNetwork module abstract class
from ContactNetworkNode import ContactNetworkNode         # ContactNetworkNode module abstract class
from Driver import Driver                                 # Driver module abstract class
from EndCriteria import EndCriteria                       # EndCriteria module abstract class
from NodeEvolution import NodeEvolution                   # NodeEvolution module abstract class
from NodeSample import NodeSample                         # NodeSample module abstract class
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
def_NodeSampleModule             = 'Perfect'
def_NumSeeds                     = 1
def_OutDir                       = os.getcwd() + "/Output"
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

    parser.add_argument('--OutDir',
        default=def_OutDir,
        help="Output directory")

    parser.add_argument('--NumSeeds',
        default=def_NumSeeds, type=int,
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
        choices=sorted(list(FAVITES_Global.list_modules['ContactNetwork'].keys())),
        help="ContactNetwork module implementation")

    parser.add_argument('--DriverModule',
        default=def_DriverModule,
        choices=sorted(list(FAVITES_Global.list_modules['Driver'].keys())),
        help="Driver module implementation")

    parser.add_argument('--EndCriteriaModule',
        required=True,
        choices=sorted(list(FAVITES_Global.list_modules['EndCriteria'].keys())),
        help="Simulation ending criteria")

    parser.add_argument('--NodeEvolutionModule',
        default=def_NodeEvolutionModule,
        choices=sorted(list(FAVITES_Global.list_modules['NodeEvolution'].keys())),
        help="NodeEvolution module implementation")

    parser.add_argument('--NodeSampleModule',
        default=def_NodeSampleModule,
        choices=sorted(list(FAVITES_Global.list_modules['NodeSample'].keys())),
        help="NodeSample module implementation")

    parser.add_argument('--PostValidationModule',
        default=def_PostValidationModule,
        choices=sorted(list(FAVITES_Global.list_modules['PostValidation'].keys())),
        help="PostValidation module implementation")

    parser.add_argument('--SeedSelectionModule',
        default=def_SeedSelectionModule,
        choices=sorted(list(FAVITES_Global.list_modules['SeedSelection'].keys())),
        help="SeedSelection module implementation")

    parser.add_argument('--SeedSequenceLength',
        default=def_SeedSequenceLength, type=int,
        help="Length of seed sequences")

    parser.add_argument('--SeedSequenceModule',
        default=def_SeedSequenceModule,
        choices=sorted(list(FAVITES_Global.list_modules['SeedSequence'].keys())),
        help="SeedSequence module implementation")

    parser.add_argument('--SourceSampleModule',
        default=def_SourceSampleModule,
        choices=sorted(list(FAVITES_Global.list_modules['SourceSample'].keys())),
        help="SourceSample module implementation")

    parser.add_argument('--TransmissionNodeSampleModule',
        default=def_TransmissionNodeSampleModule,
        choices=sorted(list(FAVITES_Global.list_modules['TransmissionNodeSample'].keys())),
        help="TransmissionNodeSample module implementation")

    parser.add_argument('--TransmissionTimeSampleModule',
        default=def_TransmissionTimeSampleModule,
        choices=sorted(list(FAVITES_Global.list_modules['TransmissionTimeSample'].keys())),
        help="TransmissionTimeSample module implementation")

    parser.add_argument('--TreeModule',
        default=def_TreeModule,
        choices=sorted(list(FAVITES_Global.list_modules['Tree'].keys())),
        help="Tree module implementation")

    args = parser.parse_args()

    # import modules and store in global access variables
    print("=============================   Modules   =============================")

    # read basic user input
    FAVITES_Global.num_seeds = args.NumSeeds
    FAVITES_Global.end_time = args.EndTime
    FAVITES_Global.end_transmissions = args.EndTransmissions
    FAVITES_Global.fixed_transmission_time_delta = args.FixedTransmissionTimeDelta
    FAVITES_Global.out_dir = args.OutDir

    # import ContactNetwork module
    print("ContactNetwork:          ", end='')
    assert args.ContactNetworkModule in FAVITES_Global.list_modules['ContactNetwork'], "%r is not a valid ContactNetwork!" % args.ContactNetworkModule
    module_ContactNetwork = FAVITES_Global.list_modules['ContactNetwork'][args.ContactNetworkModule]
    print(args.ContactNetworkModule)
    assert issubclass(module_ContactNetwork, ContactNetwork), "%r is not a ContactNetwork" % module_ContactNetwork
    FAVITES_Global.modules['ContactNetwork'] = module_ContactNetwork

    # import Driver module
    print("Driver:                  ", end='')
    assert args.DriverModule in FAVITES_Global.list_modules['Driver'], "%r is not a valid Driver!" % args.DriverModule
    module_Driver = FAVITES_Global.list_modules['Driver'][args.DriverModule]
    print(args.DriverModule)
    assert issubclass(module_Driver, Driver), "%r is not a Driver" % module_Driver
    FAVITES_Global.modules['Driver'] = module_Driver

    # import EndCriteria module
    print("EndCriteria:             ", end='')
    assert args.EndCriteriaModule in FAVITES_Global.list_modules['EndCriteria'], "%r is not a valid EndCriteria!" % args.EndCriteriaModule
    module_EndCriteria = FAVITES_Global.list_modules['EndCriteria'][args.EndCriteriaModule]
    print(args.EndCriteriaModule)
    module_EndCriteria() # check for validity
    assert issubclass(module_EndCriteria, EndCriteria), "%r is not an EndCriteria" % module_EndCriteria
    FAVITES_Global.modules['EndCriteria'] = module_EndCriteria

    # import NodeEvolution module
    print("NodeEvolution:           ", end='')
    assert args.NodeEvolutionModule in FAVITES_Global.list_modules['NodeEvolution'], "%r is not a valid NodeEvolution!" % args.NodeEvolutionModule
    module_NodeEvolution = FAVITES_Global.list_modules['NodeEvolution'][args.NodeEvolutionModule]
    print(args.NodeEvolutionModule)
    module_NodeEvolution() # check for validity
    assert issubclass(module_NodeEvolution, NodeEvolution), "%r is not a NodeEvolution" % module_NodeEvolution
    FAVITES_Global.modules['NodeEvolution'] = module_NodeEvolution

    # import NodeSample module
    print("NodeSample:              ", end='')
    assert args.NodeSampleModule in FAVITES_Global.list_modules['NodeSample'], "%r is not a valid NodeSample!" % args.NodeSampleModule
    module_NodeSample = FAVITES_Global.list_modules['NodeSample'][args.NodeSampleModule]
    print(args.NodeSampleModule)
    module_NodeSample() # check for validity
    assert issubclass(module_NodeSample, NodeSample), "%r is not a NodeSample" % module_NodeSample
    FAVITES_Global.modules['NodeSample'] = module_NodeSample

    # import PostValidation module
    print("PostValidation:          ", end='')
    assert args.PostValidationModule in FAVITES_Global.list_modules['PostValidation'], "%r is not a valid PostValidation!" % args.PostValidationModule
    module_PostValidation = FAVITES_Global.list_modules['PostValidation'][args.PostValidationModule]
    print(args.PostValidationModule)
    module_PostValidation() # check for validity
    assert issubclass(module_PostValidation, PostValidation), "%r is not a PostValidation" % module_PostValidation
    FAVITES_Global.modules['PostValidation'] = module_PostValidation

    # import SeedSelection module
    print("SeedSelection:           ", end='')
    assert args.SeedSelectionModule in FAVITES_Global.list_modules['SeedSelection'], "%r is not a valid SeedSelection!" % args.SeedSelectionModule
    module_SeedSelection = FAVITES_Global.list_modules['SeedSelection'][args.SeedSelectionModule]
    print(args.SeedSelectionModule)
    module_SeedSelection() # check for validity
    assert issubclass(module_SeedSelection, SeedSelection), "%r is not a SeedSelection" % module_SeedSelection
    FAVITES_Global.modules['SeedSelection'] = module_SeedSelection

    # import SeedSequence module
    print("SeedSequence:            ", end='')
    assert args.SeedSequenceModule in FAVITES_Global.list_modules['SeedSequence'], "%r is not a valid SeedSequence!" % args.SeedSequenceModule
    module_SeedSequence = FAVITES_Global.list_modules['SeedSequence'][args.SeedSequenceModule]
    print(args.SeedSequenceModule)
    module_SeedSequence() # check for validity
    assert issubclass(module_SeedSequence, SeedSequence), "%r is not a SeedSequence" % module_SeedSequence
    FAVITES_Global.modules['SeedSequence'] = module_SeedSequence

    # import SourceSample module
    print("SourceSample:            ", end='')
    assert args.SourceSampleModule in FAVITES_Global.list_modules['SourceSample'], "%r is not a valid SourceSample!" % args.SourceSampleModule
    module_SourceSample = FAVITES_Global.list_modules['SourceSample'][args.SourceSampleModule]
    print(args.SourceSampleModule)
    module_SourceSample() # check for validity
    assert issubclass(module_SourceSample, SourceSample), "%r is not a SourceSample" % module_SourceSample
    FAVITES_Global.modules['SourceSample'] = module_SourceSample

    # import TransmissionNodeSample module
    print("TransmissionNodeSample:  ", end='')
    assert args.TransmissionNodeSampleModule in FAVITES_Global.list_modules['TransmissionNodeSample'], "%r is not a valid TransmissionNodeSample!" % args.TransmissionNodeSampleModule
    module_TransmissionNodeSample = FAVITES_Global.list_modules['TransmissionNodeSample'][args.TransmissionNodeSampleModule]
    print(args.TransmissionNodeSampleModule)
    module_TransmissionNodeSample() # check for validity
    assert issubclass(module_TransmissionNodeSample, TransmissionNodeSample), "%r is not a TransmissionNodeSample" % module_TransmissionNodeSample
    FAVITES_Global.modules['TransmissionNodeSample'] = module_TransmissionNodeSample

    # import TransmissionTimeSample module
    print("TransmissionTimeSample:  ", end='')
    assert args.TransmissionTimeSampleModule in FAVITES_Global.list_modules['TransmissionTimeSample'], "%r is not a valid TransmissionTimeSample!" % args.TransmissionTimeSampleModule
    module_TransmissionTimeSample = FAVITES_Global.list_modules['TransmissionTimeSample'][args.TransmissionTimeSampleModule]
    print(args.TransmissionTimeSampleModule)
    module_TransmissionTimeSample() # check for validity
    assert issubclass(module_TransmissionTimeSample, TransmissionTimeSample), "%r is not a TransmissionTimeSample" % module_TransmissionTimeSample
    FAVITES_Global.modules['TransmissionTimeSample'] = module_TransmissionTimeSample

    # import Tree module
    print("Tree:                    ", end='')
    assert args.TreeModule in FAVITES_Global.list_modules['Tree'], "%r is not a valid Tree!" % args.TreeModule
    module_Tree = FAVITES_Global.list_modules['Tree'][args.TreeModule]
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
            args.ContactNetworkFile = os.path.expanduser(args.ContactNetworkFile)
        print('%r...' % args.ContactNetworkFile, end='')
        stdout.flush()
        FAVITES_Global.edge_list = [i.strip() for i in open(args.ContactNetworkFile) if len(i.strip()) > 0]
    print(' done')

    # add number of seed nodes to user input
    print("Number of seed nodes:           %d" % args.NumSeeds)

    # add seed sequence length to user input
    FAVITES_Global.seed_sequence_length = args.SeedSequenceLength
    print("Seed sequence length:           %d" % args.SeedSequenceLength)

    # add end time to user input
    if args.EndTime != None:
        print("End time:                       %d" % args.EndTime)

    # add end number of transmissions to user input
    if args.EndTransmissions != None:
        print("End number of transmissions:    %d" % args.EndTransmissions)

    # add fixed time delta to user input
    if args.FixedTransmissionTimeDelta != None:
        print("Fixed transmission time delta:  %d" % args.FixedTransmissionTimeDelta)

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