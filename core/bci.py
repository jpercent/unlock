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
        self.data = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.data.settimeout(0.001)
        self.trigger = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.trigger.settimeout(0.001)
        self.trigger.bind(('127.0.0.1', 33448))
        self.logging = False
        if logfile is not None:
            self.logging = True
            self.fh = open("%s_%d.txt" % (logfile, time.time()), 'a')
            self.buffer = np.zeros((30 * daq.frequency, daq.channels + 2))
            self.cursor = 0

    def run(self):
        if not self.daq.open():
            raise Exception('DAQ device did not open')
        if not self.daq.init():
            raise Exception('DAQ device did not initialize')
        if not self.daq.start():
            raise Exception('DAQ device did not start streaming')

        # flush any queued trigger signals
        while True:
            try:
                self.trigger.recvfrom(32)
            except socket.timeout:
                break

        while self.daq.acquire():
            samples = self.daq.getdata()
            if samples.shape[0] == 0:
                continue
            trigger = np.zeros(samples.shape[0])
            try:
                trigger[-1], _ = self.trigger.recvfrom(32)
            except socket.timeout:
                pass
            if self.logging:
                self.log(samples, trigger)
            if self.decider is not None:
                self.decider.process(samples)
            if self.selector is not None:
                self.selector.process(samples)
            self.data.sendto(json.dumps(samples.flatten().tolist()),
                            ('127.0.0.1', 33447))

        if self.logging:
            np.savetxt(self.fh, self.buffer[0:self.cursor, :],
                       fmt='%d', delimiter='\t')
            self.fh.close()

        if not self.daq.stop():
            raise Exception('DAQ device encountered an error stopping')
        if not self.daq.close():
            raise Exception('DAQ device encountered an error closing')

    def log(self, samples, trigger):
        s = samples.shape[0]
        if self.cursor + s >= self.buffer.shape[0]:
            np.savetxt(self.fh, self.buffer[0:self.cursor, :],
                       fmt='%d', delimiter='\t')
            self.cursor = 0
        self.buffer[self.cursor:self.cursor + s, 0:-2] = samples
        self.buffer[self.cursor:self.cursor + s, -2] = trigger
        self.buffer[self.cursor:self.cursor + s, -1] = time.time() * 1000
        self.cursor += s