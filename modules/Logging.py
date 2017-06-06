#! /usr/bin/env python3
'''
Niema Moshiri 2016

"Logging" module
'''
import abc

class Logging(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``Logging'' module

    Methods
    -------
    cite()
        Return citation string (or None)
    close()
        Closes the log at the end of the simulation
    init()
        Initialize the module (if need be)
    flush()
        Flush the log stream (if need be)
    write(message)
        Writes ``message'' to the log (without a linebreak)
    writeln(message)
        Writes ``message'' to the log (with a linebreak)
    '''

    @staticmethod
    @abc.abstractmethod
    def init():
        '''
        Initialize the module (if need be)
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    def cite():
        '''
        Return citation string (or None)

        Returns
        -------
        citation : str
            The citation string (or None)
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    def flush():
        '''
        Flush the log stream (if need be)
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    def close():
        '''
        Closes the log at the end of the simulation
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    def write(message=''):
        '''
        Writes ``message'' to the log (without a linebreak)

        Parameters
        ----------
        message : str
            The message to be written to the log
        '''
        pass

    @staticmethod
    @abc.abstractmethod
    def writeln(message=''):
        '''
        Writes ``message'' to the log (with a linebreak)

        Parameters
        ----------
        message : str
            The message to be written to the log
        '''
        pass