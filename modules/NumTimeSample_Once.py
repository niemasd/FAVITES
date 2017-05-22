#! /usr/bin/env python3
'''
Niema Moshiri 2017

"NumTimeSample" module, where any node is sampled exactly once
'''
from NumTimeSample import NumTimeSample
import modules.FAVITES_ModuleFactory as MF

class NumTimeSample_Once(NumTimeSample):
    def init():
        pass

    def sample_num_times(node):
        if node.is_infected():
            return 1
        else:
            return 0