#! /usr/bin/env python3
'''
Niema Moshiri 2017

"TimeSample" module, where the end time is returned for nodes who are infected
at the end time, and no sample times are returned for all other nodes
'''
from TimeSample import TimeSample
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class TimeSample_PANGEA(TimeSample):
    def cite():
        return GC.CITATION_PANGEA

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

    def sample_times(node, num_times):
        return []