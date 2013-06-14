from core.acquisition import UnlockAcquisition
import time
try:
    import pygtec
except ImportError:
    raise Exception('Unable to import the pygtec module!')


class MOBIlabDAQ(UnlockAcquisition):
    """ The gtec MOBIlab
    """
    def __init__(self, com, channels, time=30):
        super(MOBIlabDAQ, self).__init__(pygtec.MOBIlab(),
                                         self.unpack(channels), 256)
        self.com = com
        self.analog_channels = channels
        self.digital_channels = 0
        self._samples = 1
        self._running = False
        self._elapsed = 0
        self.time = time
        self._last = 0

    def open(self, *args):
        return self._device.open(self.com)

    def init(self, *args):
        self._samples = None
        return self._device.init(self.analog_channels,
                                 self.digital_channels)

    def start(self):
        self._running = self._device.start()
        return self._running

    def stop(self):
        self._running = self._device.stop()
        return self._running

    def close(self):
        return self._device.close()

    def acquire(self):
        now = time.time()
        if self._last > 0:
            self._elapsed += now - self._last
            if self._elapsed > self.time:
                return False
        self._last = now
        return self._device.acquire()

    def getdata(self):
        samples = self._device.getdata(self.channels)
        return samples.reshape((1, self.channels))

    def unpack(self, channels):
        nChannels = 0
        for i in xrange(8):
            nChannels += ((channels >> i) & 0x1)
        return nChannels
