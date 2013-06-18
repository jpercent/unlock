from core.acquisition import UnlockAcquisition
import time
try:
    import pynobio
except ImportError:
    raise Exception('Unable to import the pynobio module!')


class EnobioDAQ(UnlockAcquisition):
    """ The StarLab Enobio
    """
    def __init__(self, channels=(0,1,2,3,4,5,6,7), time=30):
        super(EnobioDAQ, self).__init__(pynobio.Enobio(), 8, 500)
        self._channels = channels
        self._samples = None
        self._running = False
        self._elapsed = 0
        self.time = time
        self._last = 0

    def open(self, *args):
        return self._device.open()

    def init(self, *args):
        self._samples = None
        return self._device.init(1)

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
        self._samples = self._device.acquire()
        return True

    def getdata(self):
        samples = self._device.getdata(self._samples * self.channels)
        samples = samples.reshape((self._samples, self.channels))
        return samples[:, self._channels]
