clear all
%close all
%% Variables
cues = {'Cue: Left', 'Cue: Right', 'Cue: Up', 'Cue: Down'};
box = 50; %size of boxcar filter


%% Import Data

fid = fopen('Test Data - Trial 2 - l,r,u,d.txt'); %open file
if fid==-1
    disp('File open not successful')
else

A = fscanf(fid,'%f %f %f %f %i', [5 inf]);
fclose(fid);
end

%% Separate Data by Channel and General Cues

B = A';
index = find(B(:,5)~=0); %locating all cues in data

for i = 1:length(index)-1 %separating data into channels and dividing by cues
    ch1{i} = B(index(i):index(i+1)-1,1);
    ch2{i} = B(index(i):index(i+1)-1,2);
    ch3{i} = B(index(i):index(i+1)-1,3);
    ch4{i} = B(index(i):index(i+1)-1,4);
    i = i+1;
end  %note: dropping data before first cue, and from last cue to end

maxLengthCh = min(cellfun('length',ch1)); %find the smallest vector of cell array

%cutting all vectors of cell array to smallest size (may not be necessary
%depending on type of averaging)
for i = 1:length(ch1)
  if length(ch1{i}) > maxLengthCh
      %ch1{i}=ch1{i}(1:maxLengthCh);
      %ch2{i}=ch2{i}(1:maxLengthCh);
      %ch3{i}=ch3{i}(1:maxLengthCh);
      %ch4{i}=ch4{i}(1:maxLengthCh);
      ch1{i}=ch1{i}(100:200);
      ch2{i}=ch2{i}(100:200);
      ch3{i}=ch3{i}(100:200);
      ch4{i}=ch4{i}(100:200);
  end
end

%% Separate Channels by Cue Type

Qorder = B(:,5); %creating indicies of cue type
Qorder(Qorder==0)=[];
Qorder = Qorder(1:end-1);

Qleft = find(Qorder==1);
Qright = find(Qorder==2);
Qup = find(Qorder==3);
Qdown = find(Qorder==4);
%Qcenter = find(Qorder==5);

%Reading in indicies
ch1L = ch1([Qleft]);
ch1R = ch1([Qright]);
ch1U = ch1([Qup]);
ch1D = ch1([Qdown]);
ch2L = ch2([Qleft]);
ch2R = ch2([Qright]);
ch2U = ch2([Qup]);
ch2D = ch2([Qdown]);
ch3L = ch3([Qleft]);
ch3R = ch3([Qright]);
ch3U = ch3([Qup]);
ch3D = ch3([Qdown]);
ch4L = ch4([Qleft]);
ch4R = ch4([Qright]);
ch4U = ch4([Qup]);
ch4D = ch4([Qdown]);

%% Average Same Cues And Boxcar Filtering

ch1La = mvgAverage(mean(cell2mat(ch1L),2), box);
ch1Ra = mvgAverage(mean(cell2mat(ch1R),2), box);
ch1Ua = mvgAverage(mean(cell2mat(ch1U),2), box);
ch1Da = mvgAverage(mean(cell2mat(ch1D),2), box);
ch2La = mvgAverage(mean(cell2mat(ch2L),2), box);
ch2Ra = mvgAverage(mean(cell2mat(ch2R),2), box);
ch2Ua = mvgAverage(mean(cell2mat(ch2U),2), box);
ch2Da = mvgAverage(mean(cell2mat(ch2D),2), box);
ch3La = mvgAverage(mean(cell2mat(ch3L),2), box);
ch3Ra = mvgAverage(mean(cell2mat(ch3R),2), box);
ch3Ua = mvgAverage(mean(cell2mat(ch3U),2), box);
ch3Da = mvgAverage(mean(cell2mat(ch3D),2), box);
ch4La = mvgAverage(mean(cell2mat(ch4L),2), box);
ch4Ra = mvgAverage(mean(cell2mat(ch4R),2), box);
ch4Ua = mvgAverage(mean(cell2mat(ch4U),2), box);
ch4Da = mvgAverage(mean(cell2mat(ch4D),2), box);

%% Plot
figure('Name', 'Channel 1')

% subplot(4,1,1)
%     plot(ch1La)
%     hold on
%     plot(ch2La, 'r')
%     plot(ch3La, 'g')
%     plot(ch4La, 'm')
%     legend('Channel 1: AF7 (leftmost)', 'Channel 2: FP1 (left)', 'Channel 3: FP2 (right)', 'Channel 4: AF8 (rightmost)')
%     title(cues{1})
%     axis([0 100 -1500 1500])
%     hold off

subplot(4,1,1)
    plot(diff(ch1La))
    hold on
    plot(diff(ch2La), 'r')
    plot(diff(ch3La), 'g')
    plot(diff(ch4La), 'm')
    legend('Channel 1: AF7 (leftmost)', 'Channel 2: FP1 (left)', 'Channel 3: FP2 (right)', 'Channel 4: AF8 (rightmost)')
    title(cues{1})
    axis([0 50 -100 100])
    hold off
    
% subplot(4,1,2)
%     plot(ch1Ra)
%         hold on
%     plot(ch2Ra, 'r')
%     plot(ch3Ra, 'g')
%     plot(ch4Ra, 'm')
%     title(cues{2})
%     axis([0 100 -1500 1500])
%     hold off

subplot(4,1,2)
    plot(diff(ch1Ra))
        hold on
    plot(diff(ch2Ra), 'r')
    plot(diff(ch3Ra), 'g')
    plot(diff(ch4Ra), 'm')
    title(cues{2})
    axis([0 50 -100 100])
    hold off

% subplot(4,1,3)
%     plot(ch1Ua)
%         hold on
%     plot(ch2Ua, 'r')
%     plot(ch3Ua, 'g')
%     plot(ch4Ua, 'm')
%     title(cues{3})
%     axis([0 100 -1500 1500])
%     hold off

subplot(4,1,3)
    plot(diff(ch1Ua))
        hold on
    plot(diff(ch2Ua), 'r')
    plot(diff(ch3Ua), 'g')
    plot(diff(ch4Ua), 'm')
    title(cues{3})
    axis([0 50 -100 100])
    hold off
    
% subplot(4,1,4)
%     plot(ch1Da)
%         hold on
%     plot(ch2Da, 'r')
%     plot(ch3Da, 'g')
%     plot(ch4Da, 'm')
%     title(cues{4})
%     axis([0 100 -1500 1500])
%     hold off
    
subplot(4,1,4)
    plot(diff(ch1Da))
        hold on
    plot(diff(ch2Da), 'r')
    plot(diff(ch3Da), 'g')
    plot(diff(ch4Da), 'm')
    title(cues{4})
    axis([0 50 -100 100])
    hold off