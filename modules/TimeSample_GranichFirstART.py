#! /usr/bin/env python3
'''
Niema Moshiri 2017

"TimeSample" module, where a given node is sampled when they first begin ART.
Individuals who never begin ART are never sampled.
'''
from TimeSample import TimeSample
import modules.FAVITES_ModuleFactory as MF
import FAVITES_GlobalContext as GC
from random import uniform

class TimeSample_GranichFirstART(TimeSample):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        assert "NumTimeSample_Once" in str(MF.modules['NumTimeSample']), "Must use NumTimeSample_Once module"
        assert "TransmissionTimeSample_HIVARTGranichGEMF" in str(MF.modules['TransmissionTimeSample']), "Must use TransmissionTimeSample_HIVARTGranichGEMF module"

    def sample_times(node, num_times):
        if not hasattr(GC,'granich_art_time'):
            GC.granich_art_time = {}
            for line in open(GC.gemf_out_dir + "/output.txt"):
                t,rate,vNum,pre,post,num0,num1,num2,num3,num4,num5,num6,num7,num8,num9,num10,lists = [i.strip() for i in line.split()]
                v = GC.gemf_num2node[int(vNum)]
                if v not in GC.granich_art_time and GC.gemf_num_to_state[int(post)] in {'A1','A2','A3','A4'}:
                    GC.granich_art_time[v] = float(t)
        if node not in GC.granich_art_time:
            return []
        else:
            return [GC.granich_art_time[node]]