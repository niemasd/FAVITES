#! /usr/bin/env python3
'''
Niema Moshiri 2016

"EndCriteria" module, where the transmission network is simulated by EpiModel
'''
from EndCriteria import EndCriteria
from EndCriteria_TransmissionFile import EndCriteria_TransmissionFile
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from os import chdir,getcwd

class EndCriteria_GEMF(EndCriteria):
    def cite():
        return GC.CITATION_GEMF

    def init():
        assert "GEMF" in str(MF.modules['TransmissionNodeSample']), "Must use a GEMF TransmissionNodeSample module"
        assert "GEMF" in str(MF.modules['TransmissionTimeSample']), "Must use a GEMF TransmissionTimeSample module"
        GC.gemf_out_dir = ('%s/GEMF_output' % GC.out_dir).replace('//','/')

    def done():
        return EndCriteria_TransmissionFile.done()

    def not_done():
        return EndCriteria_TransmissionFile.not_done()

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
