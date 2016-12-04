'''
Niema Moshiri 2016

Store global variables to be accessible by all FAVITES modules.
'''
# ContactNetwork module
from modules.ContactNetwork import ContactNetwork
from modules.ContactNetwork_NetworkX import ContactNetwork_NetworkX

# ContactNetworkEdge module
from modules.ContactNetworkEdge import ContactNetworkEdge
from modules.ContactNetworkEdge_NetworkX import ContactNetworkEdge_NetworkX

# ContactNetworkNode module
from modules.ContactNetworkNode import ContactNetworkNode
from modules.ContactNetworkNode_NetworkX import ContactNetworkNode_NetworkX

# Driver module
from modules.Driver import Driver
from modules.Driver_Default import Driver_Default

# EndCriteria module
from modules.EndCriteria import EndCriteria
from modules.EndCriteria_FirstTimeTransmissions import EndCriteria_FirstTimeTransmissions
from modules.EndCriteria_Time import EndCriteria_Time
from modules.EndCriteria_Transmissions import EndCriteria_Transmissions

# NodeEvolution module
from modules.NodeEvolution import NodeEvolution
from modules.NodeEvolution_Dummy import NodeEvolution_Dummy

# NodeSample module
from modules.NodeSample import NodeSample
from modules.NodeSample_Perfect import NodeSample_Perfect

# PostValidation module
from modules.PostValidation import PostValidation
from modules.PostValidation_Dummy import PostValidation_Dummy

# SeedSelection module
from modules.SeedSelection import SeedSelection
from modules.SeedSelection_Random import SeedSelection_Random

# SeedSequence module
from modules.SeedSequence import SeedSequence
from modules.SeedSequence_Random import SeedSequence_Random

# SourceSample module
from modules.SourceSample import SourceSample
from modules.SourceSample_Dummy import SourceSample_Dummy

# TransmissionNodeSample module
from modules.TransmissionNodeSample import TransmissionNodeSample
from modules.TransmissionNodeSample_Random import TransmissionNodeSample_Random

# TransmissionTimeSample module
from modules.TransmissionTimeSample import TransmissionTimeSample
from modules.TransmissionTimeSample_Fixed import TransmissionTimeSample_Fixed

# Tree module
from modules.Tree import Tree
from modules.Tree_DendroPy import Tree_DendroPy

def init():
    '''
    Initialize global access variables.
    '''
    # dictionary to store which implementations of each module are available
    global list_modules
    list_modules = {
        'ContactNetwork': {
            'NetworkX': ContactNetwork_NetworkX
        },
        'ContactNetworkEdge': {
            'NetworkX': ContactNetworkEdge_NetworkX
        },
        'ContactNetworkNode': {
            'NetworkX': ContactNetworkNode_NetworkX
        },
        'Driver': {
            'Default': Driver_Default
        },
        'EndCriteria': {
            'FirstTimeTransmissions': EndCriteria_FirstTimeTransmissions,
            'Time': EndCriteria_Time,
            'Transmissions': EndCriteria_Transmissions
        },
        'NodeEvolution': {
            'Dummy': NodeEvolution_Dummy
        },
        'NodeSample': {
            'Perfect': NodeSample_Perfect
        },
        'PostValidation': {
            'Dummy': PostValidation_Dummy
        },
        'SeedSelection': {
            'Random': SeedSelection_Random
        },
        'SeedSequence': {
            'Random': SeedSequence_Random
        },
        'SourceSample': {
            'Dummy': SourceSample_Dummy
        },
        'TransmissionNodeSample': {
            'Random': TransmissionNodeSample_Random
        },
        'TransmissionTimeSample': {
            'Fixed': TransmissionTimeSample_Fixed
        },
        'Tree': {
            'DendroPy': Tree_DendroPy
        }
    }

    # dictionary to store which implementation of each module was chosen
    global modules
    modules = {}

    # ContactNetwork object
    global contact_network
    contact_network = None

    # number of seed nodes
    global num_seeds
    num_seeds = None

    # seed sequence length
    global seed_sequence_length
    seed_sequence_length = None

    # global current time
    global time
    time = 0