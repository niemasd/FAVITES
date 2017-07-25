#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SequenceEvolution" module, implemented using a Nucleotide Model with Pyvolve.
'''
from SequenceEvolution import SequenceEvolution
from SequenceEvolution_Pyvolve import SequenceEvolution_Pyvolve
import FAVITES_GlobalContext as GC

class SequenceEvolution_NucleotideModelPyvolve(SequenceEvolution):
    def cite():
        return GC.CITATION_PYVOLVE

    def init():
        try:
            global pyvolve
            import pyvolve
        except:
            from os import chdir
            chdir(GC.START_DIR)
            assert False, "Error loading Pyvolve. Install with: pip3 install pyvolve"
        # config validity checks
        custom_model_params = {}
        if isinstance(GC.nuc_kappa, str):
            GC.nuc_kappa = GC.nuc_kappa.strip()
            if len(GC.nuc_kappa) != 0:
                custom_model_params['kappa'] = float(GC.nuc_kappa)
        else:
            custom_model_params['kappa'] = float(GC.nuc_kappa)
        assert isinstance(GC.nuc_frequencies_dictionary, dict), "Specified nuc_frequencies_dictionary is not a dictionary"
        if len(GC.nuc_frequencies_dictionary) != 0:
            for key in GC.nuc_frequencies_dictionary:
                assert key in {'A','C','G','T'}, "%s is not a valid codon for nuc_frequencies_dictionary. Only DNA nucleotides (A, C, G, or T)"
            assert abs(sum(GC.nuc_frequencies_dictionary.values()) - 1) < 0.000000001, "Frequencies in nuc_frequencies_dictionary must sum to 1"
            custom_model_params['state_freqs'] = GC.nuc_frequencies_dictionary
        assert isinstance(GC.nuc_mutation_rates_dictionary, dict), "Specified nuc_mutation_rates_dictionary is not a dictionary"
        if len(GC.nuc_mutation_rates_dictionary) != 0:
            custom_model_params['mu'] = GC.nuc_mutation_rates_dictionary
        assert not ('kappa' in custom_model_params and 'nuc_mutation_rates_dictionary' in custom_model_params), "Cannot use custom values for both nuc_kappa and nuc_mutation_rates_dictionary: only one of the two"

        # set up Pyvolve
        if len(custom_model_params) == 0:
            GC.pyvolve_model = pyvolve.Model("nucleotide")
        else:
            GC.pyvolve_model = pyvolve.Model("nucleotide", custom_model_params)

    def evolve_to_current_time(node):
        pass

    def finalize():
        SequenceEvolution_Pyvolve.finalize()