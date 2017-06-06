#! /usr/bin/env python3
'''
Niema Moshiri 2016

"NodeAvailability" module, using the PANGEA HIV Simulation Model
(https://github.com/olli0601/PANGEA.HIV.sim)
'''
from NodeAvailability import NodeAvailability
from ContactNetworkNode_PANGEA import ContactNetworkNode_PANGEA as Node
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from glob import glob

class NodeAvailability_PANGEA(NodeAvailability):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        assert "ContactNetwork_PANGEA" in str(MF.modules['ContactNetwork']), "Must use ContactNetwork_PANGEA module"
        assert "ContactNetworkGenerator_PANGEA" in str(MF.modules['ContactNetworkGenerator']), "Must use ContactNetworkGenerator_PANGEA module"
        assert "EndCriteria_Instant" in str(MF.modules['EndCriteria']), "Must use EndCriteria_Instant module"
        assert "NodeEvolution_PANGEA" in str(MF.modules['NodeEvolution']), "Must use NodeEvolution_PANGEA module"
        assert "NodeAvailability_PANGEA" in str(MF.modules['NodeAvailability']), "Must use NodeAvailability_PANGEA module"
        assert "NumBranchSample_All" in str(MF.modules['NumBranchSample']), "Must use NumBranchSample_All module"
        assert "NumTimeSample_PANGEA" in str(MF.modules['NumTimeSample']), "Must use NumTimeSample_PANGEA module"
        assert "PostValidation_Dummy" in str(MF.modules['PostValidation']), "Must use PostValidation_Dummy module"
        assert "SeedSelection_PANGEA" in str(MF.modules['SeedSelection']), "Must use SeedSelection_PANGEA module"
        assert "SeedSequence_PANGEA" in str(MF.modules['SeedSequence']), "Must use SeedSequence_PANGEA module"
        assert "SequenceEvolution_PANGEA" in str(MF.modules['SequenceEvolution']), "Must use SequenceEvolution_PANGEA module"
        assert "SourceSample_PANGEA" in str(MF.modules['SourceSample']), "Must use SourceSample_PANGEA module"
        assert "TimeSample_PANGEA" in str(MF.modules['TimeSample']), "Must use TimeSample_PANGEA module"
        assert "TransmissionNodeSample_PANGEA" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_PANGEA module"
        assert "TransmissionTimeSample_PANGEA" in str(MF.modules['TransmissionTimeSample']), "Must use TransmissionTimeSample_PANGEA module"

    def subsample_transmission_network():
        out = set()
        for f in glob(GC.out_dir + "/error_free_files/sequence_data/seqs_*"):
            out.add(Node(None,f.split('/')[-1][5:-6],None))
        return out