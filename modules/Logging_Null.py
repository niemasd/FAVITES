#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Logging" module, where no log messages are written.
'''
from Logging import Logging # abstract Logging class

class Logging_Null(Logging):
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