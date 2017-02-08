#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SequenceEvolution" module, implemented with Pyvolve.

If you want to use the Pyvolve default
pyvolve_custom_model_parameters_dictionary values for your model type, pass an
empty dictionary (i.e., {}) for "pyvolve_custom_model_parameters_dictionary" in
the config file.

For the "pyvolve_state_frequencies_class" paramater in the config file, you must
specify one of the StateFrequencies classes of Pyvolve. You must also specify
"pyvolve_state_frequencies_parameters_dictionary" in the config file. No matter
which StateFrequencies class you choose, the dictionary must have the key
"alphabet", which must have a value of "nucleotide", "amino_acid", or "codon".
If you chose the EqualFrequencies or RandomFrequencies class, you can add the
optional key "restrict", whose value is in the same format as the "restrict"
parameter as described in the Pyvolve manual. If you chose the CustomFrequencies
class, the dictionary must have the key "freq_dict", whose value is the
frequency dictionary as specified in the Pyvolve manual. For the sake of
simplicity of the tool, we do not allow you to choose the ReadFrequencies or
EmpiricalModelFrequencies classes, and we do not allow you to run the
compute_frequencies() function; instead, we ask that you compute the frequencies
prior to the simulation process and pass them in via the allowed options.
'''
from SequenceEvolution import SequenceEvolution
import FAVITES_GlobalContext as GC
import modules.FAVITES_ModuleFactory as MF
import pyvolve
from os import makedirs

class SequenceEvolution_Pyvolve(SequenceEvolution):
    def init():
        # config validity checks
        GC.pyvolve_model_type = GC.pyvolve_model_type.strip()
        GC.pyvolve_state_frequencies_class = GC.pyvolve_state_frequencies_class.strip()
        assert GC.pyvolve_state_frequencies_class in ["EqualFrequencies","RandomFrequencies","CustomFrequencies"], 'Unsupported Pyvolve model_type selected. Choose "EqualFrequencies", "RandomFrequencies", or "CustomFrequencies"'
        assert isinstance(GC.pyvolve_custom_model_parameters_dictionary, dict), "Specified pyvolve_custom_model_parameters_dictionary is not a dictionary"
        assert isinstance(GC.pyvolve_state_frequencies_parameters_dictionary, dict), "Specified pyvolve_state_frequencies_parameters_dictionary is not a dictionary"
        assert "alphabet" in GC.pyvolve_state_frequencies_parameters_dictionary, 'Specified pyvolve_state_frequencies_parameters_dictionary does not contain mandatory "alphabet" key'
        assert GC.pyvolve_state_frequencies_parameters_dictionary["alphabet"] in ["nucleotide","amino_acid","codon"], 'Specified pyvolve_state_frequencies_parameters_dictionary has an invalid value for "alphabet" (must be "nucleotide", "amino_acid", or "codon")'
        if GC.pyvolve_state_frequencies_class == "CustomFrequencies":
            assert "freq_dict" in GC.pyvolve_state_frequencies_parameters_dictionary, 'Pyvolve CustomFrequencies class must have the "freq_dict" key in its pyvolve_state_frequencies_parameters_dictionary (and its value must be in the same format as the Pyvolve manual)'
            assert isinstance(GC.pyvolve_state_frequencies_parameters_dictionary["freq_dict"], dict), 'Value of "freq_dict" in pyvolve_state_frequencies_parameters_dictionary is not a dictionary'

        # set up Pyvolve
        if GC.pyvolve_custom_model_parameters_dictionary == {}:
            GC.pyvolve_model = pyvolve.Model(GC.pyvolve_model_type)
        else:
            GC.pyvolve_model = pyvolve.Model(GC.pyvolve_model_type, GC.pyvolve_custom_model_parameters_dictionary)
        GC.pyvolve_f = None
        if "restrict" in GC.pyvolve_state_frequencies_parameters_dictionary:
            if GC.pyvolve_state_frequencies_class == "EqualFrequencies":
                GC.pyvolve_f = pyvolve.EqualFrequencies(GC.pyvolve_state_frequencies_parameters_dictionary["alphabet"], restrict=GC.pyvolve_state_frequencies_parameters_dictionary["restrict"])
            elif GC.pyvolve_state_frequencies_class == "RandomFrequencies":
                GC.pyvolve_f = pyvolve.RandomFrequencies(GC.pyvolve_state_frequencies_parameters_dictionary["alphabet"], restrict=GC.pyvolve_state_frequencies_parameters_dictionary["restrict"])
        elif GC.pyvolve_state_frequencies_class == "EqualFrequencies":
            GC.pyvolve_f = pyvolve.EqualFrequencies(GC.pyvolve_state_frequencies_parameters_dictionary["alphabet"])
        elif GC.pyvolve_state_frequencies_class == "RandomFrequencies":
            GC.pyvolve_f = pyvolve.RandomFrequencies(GC.pyvolve_state_frequencies_parameters_dictionary["alphabet"])
        elif GC.pyvolve_state_frequencies_class == "CustomFrequencies":
            GC.pyvolve_f = pyvolve.CustomFrequencies(GC.pyvolve_state_frequencies_parameters_dictionary["alphabet"], freq_dict=GC.pyvolve_state_frequencies_parameters_dictionary["freq_dict"])
        else:
            assert False, "Invalid Pyvolve StateFrequencies class specified"
        assert GC.pyvolve_f is not None, "Something went wrong in setting up the Pyvolve StateFrequencies class"

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