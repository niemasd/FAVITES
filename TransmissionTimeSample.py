#! /usr/bin/env python3
'''
Niema Moshiri 2016

"TransmissionTimeSample" module
'''
import abc # for abstraction

class TransmissionTimeSample(metaclass=abc.ABCMeta):
    '''
    Abstract class defining the ``TransmissionTimeSample`` module

    Methods
    -------
    sample_time(source, target)
        Returns the time of the next transmission event, which is between
        ``source'' and ``target''
    '''

    @staticmethod
    @abc.abstractmethod
    def sample_time(source, target):
        '''
        Returns the time of the next transmission event, which is between
        ``source'' and ``target''

        Parameters
        ----------
        source : ContactNetworkNode
            The node that is the source of the transmission
        target : ContactNetworkNode
            The node that is the target of the transmission

        Returns
        -------
        time : int
            Time of the transmission event (in seconds from time = 0)
        '''
        pass