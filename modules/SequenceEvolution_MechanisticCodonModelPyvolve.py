#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SequenceEvolution" module, implemented using a Mechanistic Codon Model with
Pyvolve.
'''
from SequenceEvolution import SequenceEvolution
import FAVITES_GlobalContext as GC
import modules.FAVITES_ModuleFactory as MF
from os import makedirs

class SequenceEvolution_MechanisticCodonModelPyvolve(SequenceEvolution):
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
        GC.mcm_style = GC.mcm_style.strip()
        assert GC.mcm_style in {'GY','MG'}
        if isinstance(GC.mcm_alpha, str):
            GC.mcm_alpha = GC.mcm_alpha.strip()
            if len(GC.mcm_alpha) != 0:
                custom_model_params['alpha'] = float(GC.mcm_alpha)
        else:
            custom_model_params['alpha'] = float(GC.mcm_alpha)
        if isinstance(GC.mcm_beta, str):
            GC.mcm_beta = GC.mcm_beta.strip()
            if len(GC.mcm_beta) != 0:
                custom_model_params['beta'] = float(GC.mcm_beta)
        else:
            custom_model_params['beta'] = float(GC.mcm_beta)
        if isinstance(GC.mcm_omega, str):
            GC.mcm_omega = GC.mcm_omega.strip()
            if len(GC.mcm_omega) != 0:
                custom_model_params['omega'] = float(GC.mcm_omega)
        else:
            custom_model_params['omega'] = float(GC.mcm_omega)
        if isinstance(GC.mcm_kappa, str):
            GC.mcm_kappa = GC.mcm_kappa.strip()
            if len(GC.mcm_kappa) != 0:
                custom_model_params['kappa'] = float(GC.mcm_kappa)
        else:
            custom_model_params['kappa'] = float(GC.mcm_kappa)
        assert isinstance(GC.mcm_codon_frequencies_dictionary, dict), "Specified mcm_codon_frequencies_dictionary is not a dictionary"
        if len(GC.mcm_codon_frequencies_dictionary) != 0:
            codons = set(GC.generate_all_kmers(3,'ACGT'))
            codons.difference_update({'TGA','TAA','TAG'}) # remove STOP codons
            for key in GC.mcm_codon_frequencies_dictionary:
                assert key in codons, "%s is not a valid codon for mcm_codon_frequencies_dictionary. Only include 3-mers of the DNA alphabet, excluding the STOP codons (TGA, TAA, and TAG)"
            assert abs(sum(GC.mcm_codon_frequencies_dictionary.values()) - 1) < 0.000000001, "Frequencies in mcm_codon_frequencies_dictionary must sum to 1"
            custom_model_params['state_freqs'] = GC.mcm_codon_frequencies_dictionary
        assert isinstance(GC.mcm_mutation_rates_dictionary, dict), "Specified mcm_mutation_rates_dictionary is not a dictionary"
        if len(GC.mcm_mutation_rates_dictionary) != 0:
            custom_model_params['mu'] = GC.mcm_mutation_rates_dictionary
        assert 'beta' in custom_model_params or 'omega' in custom_model_params, "Must specify a dN value using either mcm_beta or mcm_omega"
        assert not ('kappa' in custom_model_params and 'mcm_mutation_rates_dictionary' in custom_model_params), "Cannot use custom values for both mcm_kappa and mcm_mutation_rates_dictionary: only one of the two"

        # set up Pyvolve
        if len(custom_model_params) == 0:
            GC.pyvolve_model = pyvolve.Model(GC.mcm_style, neutral_scaling=True)
        else:
            GC.pyvolve_model = pyvolve.Model(GC.mcm_style, custom_model_params, neutral_scaling=True)

    def evolve_to_current_time(node):
        pass

    def finalize():
        makedirs("pyvolve_output")
        label_to_node = MF.modules['TreeNode'].label_to_node()
        roots = [root for root in GC.root_viruses]
        for root in roots:
            label = root.get_label()
            tree = pyvolve.read_tree(tree=root.newick())
            partition = pyvolve.Partition(models=GC.pyvolve_model, root_sequence=root.get_seq())
            evolver = pyvolve.Evolver(partitions=partition, tree=tree)
            ratefile = "pyvolve_output/" + label + "_ratefile.txt" # set each to None to not generate these files
            infofile = "pyvolve_output/" + label + "_infofile.txt"
            seqfile  = "pyvolve_output/" + label + "_seqfile.fasta"
            evolver(ratefile=ratefile, infofile=infofile, seqfile=seqfile)
            seqs = evolver.get_sequences() # use anc=True to get internal sequences as well
            for label in seqs:
                label_to_node[label].set_seq(seqs[label])