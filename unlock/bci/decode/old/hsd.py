# Copyright (c) Byron Galbraith, James Percent and Unlock contributors.
# All rights reserved.
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#    
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#    3. Neither the name of Unlock nor the names of its contributors may be used
#       to endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from unlock.bci.decode.decode import UnlockDecoder
from unlock.state import TrialState
import numpy as np
from sklearn import lda
import time

class HarmonicSumDecision(UnlockDecoder):
    """
    Harmonic Sum Decision (HSD) computes the frequency power spectrum of EEG
    data over one or more electrodes then sums the amplitudes of target
    frequencies and their harmonics. The target with the highest sum is chosen
    as the attended frequency.
    """
    def __init__(self, task_state=None, targets=(12.0, 13.0, 14.0, 15.0),
                 duration=3, fs=500, electrodes=8, filters=None):
        assert task_state is not None
        super(HarmonicSumDecision, self).__init__(task_state)
        self.targets = targets
        self.target_window = 0.1
        self.fs = fs
        self.electrodes = electrodes
        self.n_samples = int(duration * fs)
        self.overflow = 256
        self.buffer = np.zeros((self.n_samples + self.overflow, electrodes))
        self.cursor = 0
        self.filters = filters

        self.enabled = True

        self.fft_params()

    def fft_params(self):
        """Determine all the relevant parameters for fft analysis"""
        i = 2
        while i <= self.n_samples:
            i *= 2
        self.nfft = i
        self.window = 1 #np.hanning(self.nSamples).reshape((self.nSamples, 1))
        self.nfft = 2048

        # indices for frequency components
        # as the values returned by the fft are in freq space, the resolution
        # is limited to the size of the fft, which in this case is just the
        # next largest power of 2. for a small time window, this results in
        # poor frequency resolution.
        self.nHarmonics = 2
        self.harmonics = []
        f = np.fft.fftfreq(self.nfft, 1.0/self.fs)[0:self.nfft/2]
        f_step = f[1]
        for target in self.targets:
            r = []
            for h in range(1, self.nHarmonics+1):
                q = h * target / f_step
                # q = np.where(np.logical_and(f > h*target - self.target_window,
                #                             f < h*target + self.target_window))
                r.extend([np.floor(q), np.ceil(q)])
            self.harmonics.append(r)

    def classify(self, command):
        """
        command contains a data matrix of samples assumed to be an ndarray of
         shape (samples, electrodes+)
        """
        classify_now = False
        if self.task_state.last_change == TrialState.RestExpiry:
            self.enabled = True
            self.cursor = 0
        elif self.task_state.last_change == TrialState.TrialExpiry:
            self.enabled = False
            if self.cursor >= 0.9*self.n_samples:
                classify_now = True
        elif not self.enabled or not command.is_valid():
            return command

        # this check is a hack to deal with the edge case when the task period
        # expires and we want to classify now but we also have an invalid
        # data command. TODO: find a less ugly way to handle this
        if command.is_valid():
            samples = command.matrix[:, 0:self.electrodes]
            s = samples.shape[0]
            self.buffer[self.cursor:self.cursor+s, :] = samples
            self.cursor += s

        if self.cursor >= self.n_samples or classify_now:
            x = self.buffer[0:self.cursor]
            #if self.filters is not None:
            #    x = self.filters.apply(x)
            x = x[:, 1:4]# - x[:, 6].reshape((len(x), 1))
            x -= np.mean(x, axis=0)
            y = np.abs(np.fft.rfft(self.window * x, n=self.nfft, axis=0))
            sums = np.zeros(len(self.targets))
            for i in range(len(self.targets)):
                sums[i] = np.sum(y[self.harmonics[i], :])
            d = np.argmax(sums)
            np.set_printoptions(precision=2)
            print("HSD: %d (%.1f Hz)" % (d+1, self.targets[d]),
                sums / np.max(sums), self.cursor)
            ## TODO: roll any leftover samples to the beginning of the buffer
            self.cursor = 0
            command.decision = d + 1
            
        return command


class HarmonicSumDecisionDiagnostic(UnlockDecoder):
    """
    Harmonic Sum Decision (HSD) computes the frequency power spectrum of EEG
    data over one or more electrodes then sums the amplitudes of target
    frequencies and their harmonics. The target with the highest sum is chosen
    as the attended frequency.
    """
    def __init__(self, targets=(12.0, 13.0, 14.0, 15.0),
                 duration=3, fs=500, electrodes=8, filters=None, label='HSD'):
        super(HarmonicSumDecisionDiagnostic, self).__init__()
        self.targets = targets
        self.target_window = 0.1
        self.fs = fs
        self.electrodes = electrodes
        self.n_samples = int(duration * fs)
        self.overflow = 256
        self.buffer = np.zeros((self.n_samples + self.overflow, electrodes))
        self.cursor = 0
        self.filters = filters
        self.label = label

        self.enabled = True
        self.classify_now = False
        self.target_label = None

        self.fft_params()

    def fft_params(self):
        """Determine all the relevant parameters for fft analysis"""
        i = 2
        while i <= self.n_samples:
            i *= 2
        self.nfft = i
        self.window = 1 #np.hanning(self.nSamples).reshape((self.nSamples, 1))
        self.nfft = 2048

        # indices for frequency components
        # as the values returned by the fft are in freq space, the resolution
        # is limited to the size of the fft, which in this case is just the
        # next largest power of 2. for a small time window, this results in
        # poor frequency resolution.
        self.nHarmonics = 2
        self.harmonics = []
        f = np.fft.fftfreq(self.nfft, 1.0/self.fs)[0:self.nfft/2]
        f_step = f[1]
        for target in self.targets:
            r = []
            for h in range(1, self.nHarmonics+1):
                q = h * target / f_step
                # q = np.where(np.logical_and(f > h*target - self.target_window,
                #                             f < h*target + self.target_window))
                r.extend([np.floor(q), np.ceil(q)])
            self.harmonics.append(r)

    def start(self):
        self.enabled = True
        self.cursor = 0
        self.classify_now = False

    def stop(self):
        self.enabled = False
        if self.cursor >= 0.9*self.n_samples:
            self.classify_now = True

    def classify(self, command):
        """
        command contains a data matrix of samples assumed to be an ndarray of
         shape (samples, electrodes+)
        """
        if self.classify_now:
            return self.decode()

        if not self.enabled or not command.is_valid():
            return

        samples = command.matrix[:, 0:self.electrodes]
        s = samples.shape[0]
        self.buffer[self.cursor:self.cursor+s, :] = samples
        self.cursor += s

        if self.cursor >= self.n_samples:
            return self.decode()

    def decode(self):
        log = {
            'targets': self.targets,
            'fs': self.fs,
            'n_samples': self.n_samples,
            'nfft': self.nfft,
            'n_harmonics': self.nHarmonics,
            'feature_width': 2,
            'channel_weights': [0, 1, 1, 1, 0, 0, 0, 0],
            'feature_method': 'fft',
            'classify_method': 'argmax of sums',
        }
        x = self.buffer[0:self.cursor]
        log['data'] = x
        #if self.filters is not None:
        #    x = self.filters.apply(x)
        x = x[:, 1:4]  # - x[:, 6].reshape((len(x), 1))
        x -= np.mean(x, axis=0)
        y = np.abs(np.fft.rfft(self.window * x, n=self.nfft, axis=0))
        sums = np.zeros(len(self.targets))
        for i in range(len(self.targets)):
            sums[i] = np.sum(y[self.harmonics[i], :])
        log['sums'] = sums
        d = np.argmax(sums)
        log['class_label'] = d
        if self.target_label is not None:
            log['target_label'] = self.target_label
        np.set_printoptions(precision=2)
        print("%s: %d (%.1f Hz)" % (self.label, d+1, self.targets[d]),
            sums / np.max(sums), self.cursor)
        ## TODO: roll any leftover samples to the beginning of the buffer
        self.cursor = 0
        self.classify_now = False
        np.savez("%s-%d" % (self.label, time.time()), **log)
        #command.decision = d + 1
        return "%s: %.1f Hz" % (self.label, self.targets[d])
