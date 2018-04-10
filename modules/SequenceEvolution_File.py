#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SequenceEvolution" module, where error-free sequences are given in a
user-specified FASTA file.

Sequence IDs must be in the following format: "N?|INDIVIDUAL|TIME"
where "?" can be any integer (it's ignored), "INDIVIDUAL" is the label of an
infected individual in the contact network, and "TIME" is a sample time for
that individual. For example, N10|7|2.0 is a valid leaf label because N10 is
ignored (but it's N followed by an integer), 7 is the label of an individual in
the contact network, and 2.0 is the time at which individual 7 was sampled.
'''
from SequenceEvolution import SequenceEvolution
import FAVITES_GlobalContext as GC
import modules.FAVITES_ModuleFactory as MF
from os.path import abspath,expanduser

class SequenceEvolution_File(SequenceEvolution):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        assert "ContactNetworkGenerator_File" in str(MF.modules['ContactNetworkGenerator']), "Must use ContactNetworkGenerator_File module"
        assert "EndCriteria_TransmissionFile" in str(MF.modules['EndCriteria']), "Must use EndCriteria_TransmissionFile module"
        assert "NodeAvailability_None" in str(MF.modules['NodeAvailability']), "Must use NodeAvailability_None module"
        assert "NodeEvolution_File" in str(MF.modules['NodeEvolution']), "Must use NodeEvolution_File module"
        assert "NumBranchSample_All" in str(MF.modules['NumBranchSample']), "Must use NumBranchSample_All module"
        assert "NumTimeSample_None" in str(MF.modules['NumTimeSample']), "Must use NumTimeSample_None module"
        assert "SeedSelection_TransmissionFile" in str(MF.modules['SeedSelection']), "Must use SeedSelection_TransmissionFile module"
        assert "SeedSequence_NoSeqs" in str(MF.modules['SeedSequence']), "Must use SeedSequence_NoSeqs module"
        assert "TimeSample_None" in str(MF.modules['TimeSample']), "Must use TimeSample_None module"
        assert "TransmissionNodeSample_TransmissionFile" in str(MF.modules['TransmissionNodeSample']), "Must use TransmissionNodeSample_TransmissionFile module"
        assert "TransmissionTimeSample_TransmissionFile" in str(MF.modules['TransmissionTimeSample']), "Must use TransmissionTimeSample_TransmissionFile module"
        assert "TreeUnit_Same" in str(MF.modules['TreeUnit']), "Must use TreeUnit_Same module"
        GC.errorfree_sequence_file = abspath(expanduser(GC.errorfree_sequence_file.strip()))

    def evolve_to_current_time(node):
        pass

    def finalize():
        if not hasattr(GC,'final_sequences'): # GC.final_sequences[cn_node][t] = set of (label,seq) tuples
            GC.final_sequences = {}
        if GC.errorfree_sequence_file.lower().endswith('.gz'):
            from gzip import open as gopen
            lines = [l.decode().strip() for l in gopen(GC.errorfree_sequence_file)]
        else:
            lines = [l.strip() for l in open(GC.errorfree_sequence_file)]
        lines = [l for l in lines if len(l) != 0]
        if len(lines) == 0:
            return
        seqs = GC.parseFASTA(lines)
        for ID,seq in seqs.items():
            v,n,t = ID.split('|'); t = float(t)
            if v == 'DUMMY':
                continue
            if n not in GC.final_sequences:
                GC.final_sequences[n] = {}
            if t not in GC.final_sequences[n]:
                GC.final_sequences[n][t] = []
            GC.final_sequences[n][t].append((v,seq))