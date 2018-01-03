#! /usr/bin/env python3
'''
Niema Moshiri 2016

"EndCriteria" module, where the transmission network is simulated by GEMF
(Sahneh et al. 2016).
'''
from EndCriteria import EndCriteria
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from os import chdir,getcwd

gemf_general_help = "This file contains general helpful information about the GEMF output."
gemf_output_txt_help = '''=== output.txt ===
This is the main file of interest. It contains the GEMF simulation output. The columns of the output file are as follows (in the exact order):
* Time of event
* Total rate
* Node that was infected
* Previous state of the node
* New state of node
* Number of nodes in each state (one column per state)
* Comma-delimited lists of inducer nodes from each state (one state per list)'''
gemf_state_translate_help = "=== State Number Translations ==="

class EndCriteria_GEMF(EndCriteria):
    def cite():
        return GC.CITATION_GEMF

    def init():
        assert not hasattr(GC, "d_or_u") or GC.d_or_u.strip() != "d", "GEMF does not currently handle directed contact networks properly. Please use an undirected contact network"
        assert "GEMF" in str(MF.modules['TransmissionNodeSample']), "Must use a GEMF TransmissionNodeSample module"
        assert "GEMF" in str(MF.modules['TransmissionTimeSample']), "Must use a GEMF TransmissionTimeSample module"
        GC.gemf_out_dir = ('%s/GEMF_output' % GC.out_dir).replace('//','/')

    def done():
        return GC.transmission_num == len(GC.transmission_file)

    def not_done():
        return not EndCriteria_TransmissionFile.done()

    def finalize_time():
        # write GEMF output README for user
        f = open('%s/README.TXT' % GC.gemf_out_dir, 'w')
        f.write('%s\n\n' % gemf_general_help)
        f.write('%s\n\n' % gemf_output_txt_help)
        f.write('%s\n' % gemf_state_translate_help)
        for state in GC.gemf_state_to_num:
            f.write('%s = %s\n' % (state,str(GC.gemf_state_to_num[state])))
        f.close()

        # update global time
        GC.time = GC.end_time