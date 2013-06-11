import numpy as np
import socket
import time
import json

class BCI():
    """
    The core BCI data acquisition, signal processing, and feature decoding
    runtime.
    """
    def __init__(self, daq, decider=None, selector=None, logfile=None):
        self.daq = daq
        self.decider = decider
        self.selector = selector
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(0.001)
        self.logging = False
        if logfile is not None:
            self.logging = True
            self.fh = open("%s_%d.txt" % (logfile, time.time()), 'a')
            self.buffer = np.zeros((30*daq.frequency, daq.channels+1))
            self.cursor = 0

    def run(self):
        if not self.daq.open():
            raise Exception('DAQ device did not open')
        if not self.daq.init():
            raise Exception('DAQ device did not initialize')
        if not self.daq.start():
            raise Exception('DAQ device did not start streaming')

        while self.daq.acquire():
            samples = self.daq.getdata()
            if self.logging:
                self.log(samples)
            if self.decider is not None:
                self.decider.process(samples)
            if self.selector is not None:
                self.selector.process(samples)
            self.socket.sendto(json.dumps(samples.flatten().tolist()),
                               ('127.0.0.1', 33447))

        if self.logging:
            np.savetxt(self.fh, self.buffer[0:self.cursor, :],
                       fmt='%d', delimiter='\t')
            self.fh.close()

        if not self.daq.stop():
            raise Exception('DAQ device encountered an error stopping')
        if not self.daq.close():
            raise Exception('DAQ device encountered an error closing')

    def log(self, samples):
        s = samples.shape[0]
        if self.cursor + s >= self.buffer.shape[0]:
            np.savetxt(self.fh, self.buffer[0:self.cursor, :],
                       fmt='%d', delimiter='\t')
            self.cursor = 0
        self.buffer[self.cursor:self.cursor+s, 0:-1] = samples
        self.buffer[self.cursor:self.cursor+s, -1] = time.time()*1000
        self.cursor += s