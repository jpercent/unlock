function [SpecParams] = setDefaultSpecParams(SpecParams)
Fs = SpecParams.Fs;    %From the loaded LFP file
TW = 2;                     %time-bandwidth window
K  = 2;                     %number of slepian functions. K <= 2TW -1, [3,2] better than [2,2], [2,1]
window  =  1;         	%length of window: 50 ms
winstep =  0.1;             %step the window is moved: 50 ms, non-overlapping windows for whole lfp signal, not epochs.

SpecParams.movingWin = [window winstep];
SpecParams.params = struct('tapers',[TW K],...
                         'pad',[],...
                         'Fs',Fs,...
                         'fpass',[SpecParams.freqBand(1) SpecParams.freqBand(2)],...
                         'err',[],...
                         'trialave',[]);

SpecParams.freqResolut = SpecParams.freqBand(2) - SpecParams.freqBand(1) + 1;       % frequency range 
