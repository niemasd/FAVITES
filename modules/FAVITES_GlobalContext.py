#! /usr/bin/env python3
'''
Niema Moshiri 2016

Store global variables to be accessible by all FAVITES modules.
'''

def init(reqs):
    '''
    Initialize global context.

    Parameters
    ----------
    reqs : dict
        Dictionary containing module implementation required variables.
    '''

    global time
    time = 0.0
    for req in reqs:
        globals()[req] = reqs[req]