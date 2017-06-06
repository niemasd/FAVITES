#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Logging" module, where no log messages are written.
'''
from Logging import Logging # abstract Logging class
import FAVITES_GlobalContext as GC

class Logging_Null(Logging):
    def cite():
        return GC.CITATION_FAVITES

    def init():
        pass

    def flush():
        pass

    def close():
        pass

    def write(message=''):
        pass

    def writeln(message=''):
        pass