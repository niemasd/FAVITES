#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SequenceEvolution" module, implemented with Seq-Gen using the GTR model with
a codon model of site-specific rate heterogeneity:

"The user may specify a different rate for each codon position. This can be used
simulate the protein-coding sequences for which the third codon position evolves
faster than the first and second because a substitution at this position is
considerably less likely to cause an amino-acid substitution. Likewise, the
first codon position is expected to evolve slightly faster than the second"
'''
from SequenceEvolution import SequenceEvolution
from SequenceEvolution_SeqGen import SequenceEvolution_SeqGen
import FAVITES_GlobalContext as GC

class SequenceEvolution_GTRCodonSeqGen(SequenceEvolution):
    def cite():
        return GC.CITATION_SEQGEN

    def init():
        GC.seqgen_codon_site1_rate = float(GC.seqgen_codon_site1_rate)
        assert GC.seqgen_codon_site1_rate > 0, "seqgen_codon_site1_rate must be positive"
        GC.seqgen_codon_site2_rate = float(GC.seqgen_codon_site2_rate)
        assert GC.seqgen_codon_site2_rate > 0, "seqgen_codon_site2_rate must be positive"
        GC.seqgen_codon_site3_rate = float(GC.seqgen_codon_site3_rate)
        assert GC.seqgen_codon_site3_rate > 0, "seqgen_codon_site3_rate must be positive"
        GC.seqgen_a_to_c = float(GC.seqgen_a_to_c)
        GC.seqgen_a_to_g = float(GC.seqgen_a_to_g)
        GC.seqgen_a_to_t = float(GC.seqgen_a_to_t)
        GC.seqgen_c_to_g = float(GC.seqgen_c_to_g)
        GC.seqgen_c_to_t = float(GC.seqgen_c_to_t)
        GC.seqgen_g_to_t = float(GC.seqgen_g_to_t)
        GC.seqgen_freq_a = float(GC.seqgen_freq_a)
        GC.seqgen_freq_c = float(GC.seqgen_freq_c)
        GC.seqgen_freq_g = float(GC.seqgen_freq_g)
        GC.seqgen_freq_t = float(GC.seqgen_freq_t)
        GC.seqgen_args = "-mGTR -r %f %f %f %f %f %f -f %f %f %f %f -c %f %f %f" % (GC.seqgen_a_to_c, GC.seqgen_a_to_g, GC.seqgen_a_to_t, GC.seqgen_c_to_g, GC.seqgen_c_to_t, GC.seqgen_g_to_t, GC.seqgen_freq_a, GC.seqgen_freq_c, GC.seqgen_freq_g, GC.seqgen_freq_t, GC.seqgen_codon_site1_rate, GC.seqgen_codon_site2_rate, GC.seqgen_codon_site3_rate)
        SequenceEvolution_SeqGen.init()

    def evolve_to_current_time(node):
        pass

    def finalize():
        SequenceEvolution_SeqGen.finalize()