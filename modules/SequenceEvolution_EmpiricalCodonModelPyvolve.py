#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SequenceEvolution" module, implemented using an Empirical Codon Model with
Pyvolve.
'''
from SequenceEvolution import SequenceEvolution
from SequenceEvolution_Pyvolve import SequenceEvolution_Pyvolve
import FAVITES_GlobalContext as GC
import modules.FAVITES_ModuleFactory as MF
from datetime import datetime
from os import makedirs
from sys import stderr

class SequenceEvolution_EmpiricalCodonModelPyvolve(SequenceEvolution):
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
        GC.ecm_type = GC.ecm_type.strip()
        if GC.ecm_type == 'restricted':
            GC.ecm_type = 'ECMrest'
        elif GC.ecm_type == 'unrestricted':
            GC.ecm_type = 'ECMunrest'
        else:
            assert False, 'ecm_type must be "restricted" or "unrestricted"'
        if isinstance(GC.ecm_alpha, str):
            GC.ecm_alpha = GC.ecm_alpha.strip()
            if len(GC.ecm_alpha) != 0:
                custom_model_params['alpha'] = float(GC.ecm_alpha)
        else:
            custom_model_params['alpha'] = float(GC.ecm_alpha)
        if isinstance(GC.ecm_beta, str):
            GC.ecm_beta = GC.ecm_beta.strip()
            if len(GC.ecm_beta) != 0:
                custom_model_params['beta'] = float(GC.ecm_beta)
        else:
            custom_model_params['beta'] = float(GC.ecm_beta)
        if isinstance(GC.ecm_omega, str):
            GC.ecm_omega = GC.ecm_omega.strip()
            if len(GC.ecm_omega) != 0:
                custom_model_params['omega'] = float(GC.ecm_omega)
        else:
            custom_model_params['omega'] = float(GC.ecm_omega)
        assert isinstance(GC.ecm_codon_frequencies_dictionary, dict), "Specified ecm_codon_frequencies_dictionary is not a dictionary"
        if len(GC.ecm_codon_frequencies_dictionary) != 0:
            codons = set(GC.generate_all_kmers(3,'ACGT'))
            codons.difference_update({'TGA','TAA','TAG'}) # remove STOP codons
            for key in GC.ecm_codon_frequencies_dictionary:
                assert key in codons, "%s is not a valid codon for ecm_codon_frequencies_dictionary. Only include 3-mers of the DNA alphabet, excluding the STOP codons (TGA, TAA, and TAG)"
            assert abs(sum(GC.ecm_codon_frequencies_dictionary.values()) - 1) < 0.000000001, "Frequencies in ecm_codon_frequencies_dictionary must sum to 1"
            custom_model_params['state_freqs'] = GC.ecm_codon_frequencies_dictionary

        # set up Pyvolve
        if len(custom_model_params) == 0:
            GC.pyvolve_model = pyvolve.Model(GC.ecm_type)
        else:
            GC.pyvolve_model = pyvolve.Model(GC.ecm_type, custom_model_params)

    def evolve_to_current_time(node):
        pass

    def finalize():
        SequenceEvolution_Pyvolve.finalize()