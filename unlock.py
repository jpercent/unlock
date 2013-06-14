"""
Launch the decoder and visualizer runtime scripts.
"""
import multiprocessing as mp

electrodes = 8
fs = 500

## The Data Process
def data():
    from core import BCI, FilterChain
    from daq import FunctionDAQ, FileDAQ
    from decoder.hsd import HarmonicSumDecision
    from decoder.tm import TemplateMatch
    import numpy as np

    # templates = np.random.randint(-1000, 1000, (4, electrodes, fs))
    # samples = np.zeros((electrodes, fs*25))
    # for i in xrange(4):
    #     k = i*fs*5
    #     for j in xrange(5):
    #         l = k + j*fs
    #         samples[:, l:l+fs] = templates[i,:,:]
    #     samples[:,(20+i)*fs:(20+1+i)*fs] = templates[i,:,:]
    # samples[:,24*fs:25*fs] = np.random.randint(-1000, 1000, (electrodes, fs))
    # dt = 1.0/fs
    #
    # def sim(t):
    #     i = int(t/dt)# % fs
    #     return samples[:, i]

    # def sim(t):
    #     samples = np.array([np.random.randint(-1000, 1000, (1, electrodes))])
    #     samples += int(100*np.sin(15*2*np.pi*t))
    #     return samples

    #daq = FunctionDAQ(sim, electrodes, 0, dt=1.0/fs, time=25)
    daq = FileDAQ("/Users/bgalbraith/Dropbox/School/enobio data/m1_15hz.txt",
                  8, 500, delimiter='\t')
    chain = FilterChain()
    chain.add_filter(('bipolar_reference', 6))
    chain.add_filter(('prune', 1, 2, 3))
    chain.add_filter(('zeromean', None))

    tm = TemplateMatch(2, 517, 10, electrodes, filters=chain)

    #hsd = HarmonicSumDecision([12.0, 13.0, 14.0, 15.0], 4.0, fs, electrodes,
    #                          filters=chain)
    #bci = BCI(daq, decider=hsd)
    bci = BCI(daq, decider=tm)
    bci.run()


## The Visualization Process
def visual():
    from core import Screen, viewport
    from apps.diagnostic import TimeScope
    screen = Screen(0, 0, viewport.window.width, viewport.window.height)
    scope = TimeScope(screen, numchan=electrodes, fs=fs)
    viewport.controller.set_apps([scope])
    #viewport.show_fps = True
    #viewport.window.set_vsync(True)
    viewport.start()

if __name__ == "__main__":
    d = mp.Process(target=data)
    #v = mp.Process(target=visual)
    d.start()
    #v.start()
    d.join()
    #v.join()