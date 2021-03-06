# Copyright (c) Giang Nguyen, James Percent and Unlock contributors.
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

import argparse
import numpy as np
import matplotlib.pyplot as plt

argParser = argparse.ArgumentParser()
argParser.add_argument('datafile')
argParser.add_argument('--fromtime', type=float, default=0)
argParser.add_argument('--totime', type=float, default=None)
args = argParser.parse_args()

time,signal = [],[]
fin = open(args.datafile, 'r')
for line in fin:
    words = line.split(',')
    time_value = float(words[1])
    signal_value = float(words[0])
    
    if (time_value > args.fromtime and (args.totime == None or time_value < args.totime)):
        time.append(time_value)
        signal.append(signal_value)
fin.close()
time,signal = np.array(time),np.array(signal)

fft = np.fft.fft(signal)
sampleSpacing = time[-1] / time.size

freq = np.fft.fftfreq(signal.size, sampleSpacing)
power = 10*np.log10(np.abs(fft)**2)

plt.plot(freq, power)
plt.ylabel('Power (dB)')
plt.xlabel('Frequency (Hz)')
plt.show()