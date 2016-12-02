#! /usr/bin/env python3
'''
Niema Moshiri 2016

"SourceSample" module, dummy implementation
'''
import FAVITES_Global                 # for global access variables
from SourceSample import SourceSample # abstract SourceSample class
from sys import stderr                # to write to standard error

class SourceSample_Dummy(SourceSample):
    def sample_virus(node):
        print('\nWARNING: Using dummy SourceSample implementation!', file=stderr)
        return 'DUMMYSTRINGDUMMYSTRING'