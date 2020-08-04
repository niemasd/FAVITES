#! /usr/bin/env python3
'''
Niema Moshiri 2020

"TimeSample" module, where a node is sampled when they are first exposed.
Individuals who are never exposed are (understandably) never sampled.
'''
from TimeSample import TimeSample
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC

class TimeSample_SAAPPHIIREFirstExposed(TimeSample):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        assert "NumTimeSample_Once" in str(MF.modules['NumTimeSample']), "Must use NumTimeSample_Once module"
        assert "TransmissionTimeSample_SAAPPHIIREGEMF" in str(MF.modules['TransmissionTimeSample']) or "TransmissionTimeSample_SAPHIREGEMF" in str(MF.modules['TransmissionTimeSample']), "Must use TransmissionTimeSample_SAAPPHIIREGEMF or TransmissionTimeSample_SAPHIREGEMF module"

    def sample_times(node, num_times):
        if not hasattr(GC,'saapphiire_exp_time'):
            GC.saapphiire_exp_time = {}
            for line in open("%s/output.txt" % GC.gemf_out_dir):
                t,rate,vNum,pre,post,num0,num1,num2,num3,num4,num5,num6,num7,num8,num9,lists = [i.strip() for i in line.split()]
                v = GC.gemf_num2node[int(vNum)]
                if v not in GC.saapphiire_exp_time and GC.gemf_num_to_state[int(post)] == 'E':
                    GC.saapphiire_exp_time[v] = float(t)
        if node not in GC.saapphiire_exp_time:
            return []
        else:
            return [GC.saapphiire_exp_time[node]]
