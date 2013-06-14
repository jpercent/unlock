"""
Launch the decoder and visualizer runtime scripts.
"""
import multiprocessing as mp

electrodes = 8
fs = 500
nTemplates = 4
nTrials = 5
time = 25

## The Data Process
def data():
    from core import BCI, FilterChain

    # import numpy as np
    #
    # templates = np.random.randint(-1000, 1000, (nTemplates, electrodes, fs))
    # samples = np.zeros((electrodes, fs*time))
    # for i in xrange(nTemplates):
    #     k = i*fs*nTrials
    #     for j in xrange(nTrials):
    #         l = k + j*fs
    #         samples[:, l:l+fs] = templates[i,:,:]
    #     samples[:,(20+i)*fs:(20+1+i)*fs] = templates[i,:,:]
    # samples[:,24*fs:25*fs] = np.random.randint(-1000, 1000, (electrodes, fs))
    # dt = 1.0/fs
    #
    # def sim(t):
    #     i = int(t/dt)  # % fs
    #     return samples[:, i]

    # def sim(t):
    #     samples = np.array([np.random.randint(-1000, 1000, (1, electrodes))])
    #     samples += int(100*np.sin(15*2*np.pi*t))
    #     return samples


    # filter chain for enobio ssvep hsd
    chain = FilterChain()
    chain.add_filter(('bipolar_reference', 6))
    chain.add_filter(('choose', 1, 2, 3))
    chain.add_filter(('zeromean', None))

    # from daq import FunctionDAQ
    # daq = FunctionDAQ(sim, electrodes, 0, dt=dt, time=time)

    from daq import FileDAQ
    daq = FileDAQ("/Users/bgalbraith/Dropbox/School/enobio data/15hz_test.txt",
                  8, 0, delimiter='\t')

    # from decoder.tm import TemplateMatch
    # tm = TemplateMatch(nTemplates, fs, nTrials, electrodes, filters=None)
    # bci = BCI(daq, decider=tm)

    from decoder.hsd import HarmonicSumDecision
    hsd = HarmonicSumDecision([12.0, 13.0, 14.0, 15.0], 4.0, fs, electrodes,
                              filters=chain)
    bci = BCI(daq, decider=hsd)

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