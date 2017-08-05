#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SequenceEvolution" module, implemented with Seq-Gen using the GTR+Gamma model
'''
from SequenceEvolution import SequenceEvolution
from SequenceEvolution_SeqGen import SequenceEvolution_SeqGen
import FAVITES_GlobalContext as GC

class SequenceEvolution_GTRGammaSeqGen(SequenceEvolution):
    def cite():
        return GC.CITATION_SEQGEN

    def init():
        GC.seqgen_gamma_shape = float(GC.seqgen_gamma_shape)
        assert GC.seqgen_gamma_shape > 0, "seqgen_gamma_shape must be positive"
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
        GC.seqgen_args = "-mGTR -a%f -r %f %f %f %f %f %f -f %f %f %f %f" % (GC.seqgen_gamma_shape, GC.seqgen_a_to_c, GC.seqgen_a_to_g, GC.seqgen_a_to_t, GC.seqgen_c_to_g, GC.seqgen_c_to_t, GC.seqgen_g_to_t, GC.seqgen_freq_a, GC.seqgen_freq_c, GC.seqgen_freq_g, GC.seqgen_freq_t)
        if isinstance(GC.seqgen_num_gamma_rate_categories,int) or len(GC.seqgen_num_gamma_rate_categories.strip()) != 0:
            GC.seqgen_num_gamma_rate_categories = int(GC.seqgen_num_gamma_rate_categories)
            assert GC.seqgen_num_gamma_rate_categories > 0, "seqgen_num_gamma_rate_categories must be positive"
            GC.seqgen_args += ("-g%d" % GC.seqgen_num_gamma_rate_categories)
        SequenceEvolution_SeqGen.init()

    def evolve_to_current_time(node):
        pass

    def finalize():
        SequenceEvolution_SeqGen.finalize()