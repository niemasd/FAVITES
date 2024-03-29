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
from datetime import datetime
from os import makedirs
from sys import stderr
from sys import modules as sysmodules

class SequenceEvolution_Pyvolve(SequenceEvolution):
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
        GC.pyvolve_model_type = GC.pyvolve_model_type.strip()
        GC.pyvolve_state_frequencies_class = GC.pyvolve_state_frequencies_class.strip()
        assert GC.pyvolve_state_frequencies_class in {"EqualFrequencies","RandomFrequencies","CustomFrequencies"}, 'Unsupported Pyvolve state_frequencies_class selected. Choose "EqualFrequencies", "RandomFrequencies", or "CustomFrequencies"'
        assert isinstance(GC.pyvolve_custom_model_parameters_dictionary, dict), "Specified pyvolve_custom_model_parameters_dictionary is not a dictionary"
        assert isinstance(GC.pyvolve_state_frequencies_parameters_dictionary, dict), "Specified pyvolve_state_frequencies_parameters_dictionary is not a dictionary"
        assert "alphabet" in GC.pyvolve_state_frequencies_parameters_dictionary, 'Specified pyvolve_state_frequencies_parameters_dictionary does not contain mandatory "alphabet" key'
        assert GC.pyvolve_state_frequencies_parameters_dictionary["alphabet"] in {"nucleotide","amino_acid","codon"}, 'Specified pyvolve_state_frequencies_parameters_dictionary has an invalid value for "alphabet" (must be "nucleotide", "amino_acid", or "codon")'
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
        if GC.random_number_seed is not None:
            from warnings import warn
            warn("random_number_seed specified, but Pyvolve does not support seeding its random generator")
        makedirs("pyvolve_output", exist_ok=True)
        label_to_node = MF.modules['TreeNode'].label_to_node()
        for root,treestr in GC.pruned_newick_trees:
            # run Pyvolve
            treestr = treestr.strip()
            label = root.get_label()
            rootseq = root.get_seq()
            if GC.VERBOSE:
                print('[%s] Pyvolve evolving sequences on tree: %s' % (datetime.now(),treestr), file=stderr)
                print('[%s] Pyvolve root sequence: %s' % (datetime.now(),rootseq), file=stderr)
            if treestr != '(':
                treestr = '(%s);' % treestr[:-1]
            try:
                tree = pyvolve.read_tree(tree=treestr)
                partition = pyvolve.Partition(models=GC.pyvolve_model, root_sequence=rootseq)
                evolver = pyvolve.Evolver(partitions=partition, tree=tree)
            except NameError:
                import pyvolve
                tree = pyvolve.read_tree(tree=treestr)
                partition = pyvolve.Partition(models=GC.pyvolve_model, root_sequence=rootseq)
                evolver = pyvolve.Evolver(partitions=partition, tree=tree)
            except AssertionError:
                assert False, "Error setting up Pyvolve. Tree: %s" % treestr
            ratefile = "pyvolve_output/%s_ratefile.txt" % label # set each to None to not generate these files
            infofile = "pyvolve_output/%s_infofile.txt" % label
            seqfile  = "pyvolve_output/%s_seqfile.fasta" % label
            evolver(ratefile=ratefile, infofile=infofile, seqfile=seqfile)
            seqs = evolver.get_sequences() # use anc=True to get internal sequences as well

            # store leaf sequences in GlobalContext
            if not hasattr(GC,'final_sequences'): # GC.final_sequences[cn_node][t] = set of (label,seq) tuples
                GC.final_sequences = {}
            for leaf in seqs:
                seq = seqs[leaf]
                virus_label,cn_label,sample_time = leaf.split('|')
                sample_time = float(sample_time)
                if cn_label not in GC.final_sequences:
                    GC.final_sequences[cn_label] = {}
                if sample_time not in GC.final_sequences[cn_label]:
                    GC.final_sequences[cn_label][sample_time] = []
                GC.final_sequences[cn_label][sample_time].append((leaf,seq))