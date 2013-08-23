clear all
%close all
%% Variables
cues = {'Cue: Left', 'Cue: Right', 'Cue: Up', 'Cue: Down'};
box = 25; %size of boxcar filter
%sample rate of anovio: 500Hz

%% Import Data

fid = fopen('bci_9.txt'); %open file
if fid==-1
    disp('File open not successful')
else
    A = fscanf(fid,'%f %f %f %f %f %f %f %f %i', [9 inf]);
    fclose(fid);
end

%% Separate Data by Channel and General Cues

B = A;
B(:,4:8) = []; %erase unwanted data

index = find(B(:,4)==1||2||3||4); %locating all cues in data

for i = 1:length(index)-1 %separating data into channels and dividing by cues
    ch1{i}=B(index(i):index(i+1)-1,1);
    ch2{i}=B(index(i):index(i+1)-1,2);
    ch3{i}=B(index(i):index(i+1)-1,3);
end  %note: dropping data before first cue, and from last cue to end


maxLengthCh = min(cellfun('length',ch1)); %find the smallest vector of cell array

%cutting all vectors of cell array to smallest size (may not be necessary
%depending on type of averaging)
for i = 1:length(ch1)
  if length(ch1{i}) > maxLengthCh
      ch1{i}=ch1{i}(1:maxLengthCh);
      ch2{i}=ch2{i}(1:maxLengthCh);
      ch3{i}=ch3{i}(1:maxLengthCh);
  end
end

%% Separate Channels by Cue Type

Qorder = B(:,4); %creating indicies of cue type
Qorder(Qorder==0)=[];
Qorder = Qorder(1:end-1);

Qleft = find(Qorder==1);
Qright = find(Qorder==2);
Qup = find(Qorder==3);
Qdown = find(Qorder==4);
Qreset = find(Qorder==6);

%Reading in indicies & faking reference for Left/Right
ch1L = ch1([Qleft]) - ch2([Qleft]);
ch1R = ch1([Qright])- ch2([Qright]);
ch1U = ch1([Qup]);
ch1D = ch1([Qdown]);

ch2U = ch2([Qup]);
ch2D = ch2([Qdown]);

ch3L = ch3([Qleft]) - ch2([Qleft]);
ch3R = ch3([Qright])- ch2([Qright]);
ch3U = ch3([Qup]);
ch3D = ch3([Qdown]);

%% Average Same Cues And Boxcar Filtering

ch1La = mvgAverage(mean(cell2mat(ch1L),2), box);
ch1Ra = mvgAverage(mean(cell2mat(ch1R),2), box);
ch1Ua = mvgAverage(mean(cell2mat(ch1U),2), box);
ch1Da = mvgAverage(mean(cell2mat(ch1D),2), box);

ch2Ua = mvgAverage(mean(cell2mat(ch2U),2), box);
ch2Da = mvgAverage(mean(cell2mat(ch2D),2), box);

ch3La = mvgAverage(mean(cell2mat(ch3L),2), box);
ch3Ra = mvgAverage(mean(cell2mat(ch3R),2), box);
ch3Ua = mvgAverage(mean(cell2mat(ch3U),2), box);
ch3Da = mvgAverage(mean(cell2mat(ch3D),2), box);

%% Plot
figure('Name', 'Channel 1')

subplot(4,1,1)
    plot(ch1La)
        hold on
    plot(ch3La, 'r')
    legend('Channel 1: AF7 (left)', 'Channel 3: AF8 (right)')
    title(cues{1})
        hold off
    
subplot(4,1,2)
    plot(ch1Ra)
        hold on
    plot(ch3Ra, 'r')
    legend('Channel 1: AF7 (left)', 'Channel 3: AF8 (right)')
    title(cues{2})
        hold off

subplot(4,1,3)
    plot(ch1Ua)
        hold on
    plot(ch2Ua, 'g')
    plot(ch3Ua, 'r')
    legend('Channel 1: AF7 (left)', 'Channel 2: FPz','Channel 3: AF8 (right)')
    title(cues{3})
        hold off
    
subplot(4,1,4)
    plot(ch1Da)
        hold on
    plot(ch2Da, 'g')
    plot(ch3Da, 'r')
    legend('Channel 1: AF7 (left)', 'Channel 2: FPz','Channel 3: AF8 (right)')
    title(cues{4})
        hold off
        
%% Decipher Code
Quarter = 'Start';

ChanChan1 = mvgAverage(B(:,1));
ChanChan2 = mvgAverage(B(:,2));
ChanChan3 = mvgAverage(B(:,3));

ChanChan1Ref2 = ChanChan1 - ChanChan2;
ChanChan3Ref2 = ChanChan3 - ChanChan2;

for i = 1:length(ChanChan1)-10
    if ChanChan1Ref2(i+10)-ChanChan1Ref2(i)>0 && ChanChan3Ref2(i+10)-ChanChan3Ref2(i)<0
        countL = countL + 1;
    else
        countL = 0;
    end
    
    if ChanChan1Ref2(i+10)-ChanChan1Ref2(i)<0 && ChanChan3Ref2(i+10)-ChanChan3Ref2(i)>0
        countR = countR + 1;
    else
        countR = 0;
    end
    
    if countL == 5
        Quarter = [Quarter 'Left'];
        countL = 0;
    elseif countR == 5
        Quarter = [Quarter 'Right'];
        countR = 0;
    elseif countR==5&&countL==5
        Quarter = [Quarter 'Error: L/R'];
    end
    
    if ChanChan1(i+10)-ChanChan1(i)>0 && ChanChan2(i+10)-ChanChan2(i+10)>0&&ChanChan2(i+10)-ChanChan2(i)>0
        countU = countU+1;
    else
        countU = 0;
    end
    
    if ChanChan1(i+10)-ChanChan1(i)<0 && ChanChan2(i+10)-ChanChan2(i+10)<0 && ChanChan2(i+10)-ChanChan2(i)<0
        countD = countD+1;
    else
        countD = 0;
    end

 	if countU == 5
        Quarter = [Quarter 'Up'];
        countU = 0;
    elseif countD == 5
        Quarter = [Quarter 'Down'];
        countD = 0;
    elseif countU==5&&countD==5
        Quarter = [Quarter 'Error: U/D'];
    end
end
