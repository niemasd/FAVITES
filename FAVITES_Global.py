'''
Niema Moshiri 2016

Store global variables to be accessible by all FAVITES modules.
'''
# ContactNetwork module
from ContactNetwork import ContactNetwork
from ContactNetwork_NetworkX import ContactNetwork_NetworkX

# ContactNetworkEdge module
from ContactNetworkEdge import ContactNetworkEdge
from ContactNetworkEdge_NetworkX import ContactNetworkEdge_NetworkX

# ContactNetworkNode module
from ContactNetworkNode import ContactNetworkNode
from ContactNetworkNode_NetworkX import ContactNetworkNode_NetworkX

# Driver module
from Driver import Driver
from Driver_Default import Driver_Default

# EndCriteria module
from EndCriteria import EndCriteria
from EndCriteria_FirstTimeTransmissions import EndCriteria_FirstTimeTransmissions
from EndCriteria_Time import EndCriteria_Time
from EndCriteria_Transmissions import EndCriteria_Transmissions

# NodeEvolution module
from NodeEvolution import NodeEvolution
from NodeEvolution_Dummy import NodeEvolution_Dummy

# NodeSample module
from NodeSample import NodeSample
from NodeSample_Perfect import NodeSample_Perfect

# PostValidation module
from PostValidation import PostValidation
from PostValidation_Dummy import PostValidation_Dummy

# SeedSelection module
from SeedSelection import SeedSelection
from SeedSelection_Random import SeedSelection_Random

# SeedSequence module
from SeedSequence import SeedSequence
from SeedSequence_Random import SeedSequence_Random

# SourceSample module
from SourceSample import SourceSample
from SourceSample_Dummy import SourceSample_Dummy

# TransmissionNodeSample module
from TransmissionNodeSample import TransmissionNodeSample
from TransmissionNodeSample_Random import TransmissionNodeSample_Random

# TransmissionTimeSample module
from TransmissionTimeSample import TransmissionTimeSample
from TransmissionTimeSample_Fixed import TransmissionTimeSample_Fixed

# Tree module
from Tree import Tree
from Tree_DendroPy import Tree_DendroPy

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