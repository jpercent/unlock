"""
Launch the decoder and visualizer runtime scripts.
"""
import multiprocessing as mp
import psutil
import os

p = psutil.Process(os.getpid())
p.set_nice(psutil.REALTIME_PRIORITY_CLASS)

electrodes = 8
fs = 500
length = int(31 / 30.0 * 500)
nTemplates = 2
nTrials = 10
time = 25


## The Data Process
def data():
    from core import BCI, FilterChain
    from decoder.tm import TemplateMatch
    from daq import EnobioDAQ

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

    # filter chain for enobio ssvep hsd
    chain = FilterChain()
    chain.add_filter(('bipolar_reference', 6))
    chain.add_filter(('choose', 1, 2, 3))
    chain.add_filter(('zeromean', None))

    # from daq import FunctionDAQ
    # device = FunctionDAQ(sim, electrodes, 0, dt=dt, time=time)

    # from daq import FileDAQ
    # device = FileDAQ("/Users/bgalbraith/Dropbox/School/enobio data/15hz_test.txt",
    #               8, 0, delimiter='\t')

    tm = TemplateMatch(nTemplates, length, nTrials, electrodes, filters=chain)
    device = EnobioDAQ(time=time)
    bci = BCI(device, decider=tm, logfile='mseq2-4')
    bci.run()


## The Visualization Process
def visual():
    from core import Screen, viewport
    from apps.stimuli.ssvep import SSVEP, SSVEPStimulus
    ssvep_screen = Screen(0, 0, viewport.window.width, viewport.window.height)
    stimuli = [
        SSVEPStimulus(ssvep_screen, 60.0, 'center', width=200, height=200,
                      x_freq=4, y_freq=4, filename_reverse=True, y_offset=200,
                      x_offset=000, sequence=(1, 1, 1, 0, 1, 0, 1, 0, 0, 0,
                                              0, 1, 0, 0, 1, 0, 1, 1, 0, 0,
                                              1, 1, 1, 1, 1, 0, 0, 0, 1, 1,
                                              0),
                      color1=(255, 0, 0), color2=(255, 255, 0)),
        SSVEPStimulus(ssvep_screen, 60.0, 'center', width=200, height=200,
                      x_freq=4, y_freq=4, filename_reverse=True, y_offset=-200,
                      x_offset=000,  sequence=(0, 1, 1, 1, 0, 1, 0, 1, 0, 0,
                                               1, 0, 0, 0, 0, 0, 1, 1, 1, 1,
                                               1, 1, 1, 0, 1, 0, 1, 1, 0, 1,
                                               1),
                      color1=(255, 0, 0), color2=(255, 255, 0)),
        # SSVEPStimulus(ssvep_screen, 30.0, 'center', width=200, height=200,
        #               x_freq=2, y_freq=2, filename_reverse=True, y_offset=000,
        #               x_offset=200, sequence=(0, 1, 0, 0, 0, 1, 0, 1, 0, 0,
        #                                       1, 0, 1, 1, 0, 0, 1, 0, 1, 0,
        #                                       0, 1, 0, 0, 0, 1, 0, 0, 1, 1,
        #                                       0),
        #               color1=(255, 0, 0), color2=(255, 255, 0)),
        # SSVEPStimulus(ssvep_screen, 30.0, 'center', width=200, height=200,
        #               x_freq=2, y_freq=2, filename_reverse=True, y_offset=0,
        #               x_offset=-200, sequence=(0, 0, 1, 1, 0, 0, 0, 1, 1, 0,
        #                                        1, 0, 1, 1, 1, 1, 1, 1, 1, 1,
        #                                        1, 1, 1, 0, 0, 1, 1, 0, 0, 0,
        #                                        0),
        #               color1=(255, 0, 0), color2=(255, 255, 0))
    ]
    ssvep = SSVEP(ssvep_screen, stimuli, rest_length=0,
                  trigger_addr=('127.0.0.1', 33448))
    #viewport.window.set_vsync(True)
    viewport.show_fps = True
    viewport.controller.set_apps([ssvep])
    viewport.start()

if __name__ == "__main__":
    v = mp.Process(target=visual)
    d = mp.Process(target=data)
    v.start()
    d.start()
    v.join()
    d.join()
