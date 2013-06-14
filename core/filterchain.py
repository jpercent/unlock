import numpy as np

class FilterChain(object):
    """
    The idea here is to have an object that encapsulates the filtering stages
    that are applied to the raw acquired signal. This would contain a list
    of functions that perform some transformation to the signals, such as
    band pass filters, detrending, channel selection, bipolar referencing, etc
    """
    def __init__(self):
        self._filters = []

    def add_filter(self, f):
        self._filters.append(f)

    def apply(self, signal):
        for f in self._filters:
            function = self.__getattribute__(f[0])
            signal = function(signal, f[1])

        return signal

    def choose(self, signal, *args):
        return signal[:, args]

    def bipolar_reference(self, signal, *args):
        y = signal - signal[:, args]
        return np.delete(y, args, 1)

    def zeromean(self, signal, *args):
        return signal - np.mean(signal, axis=0)
