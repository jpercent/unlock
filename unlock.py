"""
Launch the decoder and visualizer runtime scripts.
"""
import multiprocessing as mp

electrodes = 4
fs = 500

## The Data Process
def data():
    from core import BCI
    from daq import FunctionDAQ
    from decoder.hsd import HarmonicSumDecision
    import numpy as np

    def sim(t):
        samples = np.array([np.random.randint(-1000, 1000, (1, electrodes))])
        samples += int(100*np.sin(15*2*np.pi*t))
        return samples

    daq = FunctionDAQ(sim, electrodes, fs, time=20)
    hsd = HarmonicSumDecision([12.0, 13.0, 14.0, 15.0], 4.0, fs, electrodes)
    bci = BCI(daq, decider=hsd)
    bci.run()


## The Visualization Process
def visual():
    from core import Screen
    from apps.diagnostic import TimeScope
    from core import viewport
    # Uncomment the following line to see the rate of frames per second.
    #viewport.show_fps = True
    screen = Screen(0, 0, viewport.window.width, viewport.window.height)
    scope = TimeScope(screen, numchan=electrodes, fs=fs)
    viewport.controller.set_apps([scope])
    viewport.start()

if __name__ == "__main__":
    d = mp.Process(target=data)
    v = mp.Process(target=visual)
    d.start()
    v.start()
    d.join()
    v.join()