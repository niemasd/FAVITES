#! /usr/bin/env python3
'''
Niema Moshiri 2016

"PostValidation" module, dummy implementation
'''
from modules import FAVITES_Global                # for global access variables
from modules.PostValidation import PostValidation # abstract PostValidation class

class PostValidation_Dummy(PostValidation):
    def score_transmission_network():
        #print('\nWARNING: Using dummy PostValidation implementation!')
        return 0