clear variables
close all
%% Variables
cues = {'Cue: Left', 'Cue: Right', 'Cue: Up', 'Cue: Down'};
box = 25; %size of boxcar filter
box2 = 200;
box3 = 50;
%sample rate of anovio: 500Hz
%approximately 100 samples in the spiking

%% Import Data
fid = fopen('bci_18_70.txt'); %open file
if fid==-1
    disp('File open not successful')
else
    A = fscanf(fid,'%f %f %f %f %f %f %f %f %f %i', [10 inf]);
    fclose(fid);
end

%% Separate Data by Channel and General Cues
B = A';
%B(:,4:8) = []; %erase unwanted data

% %% Separate Channels by Cue Type
% Qorder = B(:,4); %creating indicies of cue type
% Qorder(Qorder==0)=[];
% Qorder(Qorder==5)=[];
% Qorder(Qorder==6)=[];
% Qorder = Qorder(1:end-1);
        
%% Decipher Code
Quarter = [];

Chan1 = B(:,1);
Chan2 = B(:,7);
Chan3 = B(:,3);

% figure(1)
% set(figure(1),'name','In The Beginning...','numbertitle','off')
% subplot(4,1,1)
%     plot(Chan1)
%         hold on
%     plot(Chan2, 'g')
%     plot(Chan3, 'r')
%     title('Unfiltered Signals')

Chan1=Chan1 - mean(Chan1);
Chan2=Chan2 - mean(Chan2);
Chan3=Chan3 - mean(Chan3);
% subplot(4,1,2)
%     plot(Chan1)
%         hold on
%     plot(Chan2, 'g')
%     plot(Chan3, 'r')
%     title('Zero-mean')

Chan1=smooth(Chan1,box);
Chan2=smooth(Chan2,box);
Chan3=smooth(Chan3,box);
% subplot(4,1,3)
%     plot(Chan1)
%         hold on
%     plot(Chan2, 'g')
%     plot(Chan3, 'r')
%     title(sprintf('Boxcar Filter: %d', box))
    
x=[1:1:length(Chan1)]';
p = polyfit(x,Chan1,1);
r = p(1) .* x + p(2);
Chan1 = Chan1-r;
p = polyfit(x,Chan2,1);
r = p(1) .* x + p(2);
Chan2 = Chan2-r;
p = polyfit(x,Chan3,1);
r = p(1) .* x + p(2);
Chan3 = Chan3-r;
% subplot(4,1,4)
%     plot(Chan1)
%         hold on
%     plot(Chan2,'g')
%     plot(Chan3,'r')
%     title('Correcting for Drift (subtracting best fit line)')
%%
% figure(2)
% set(figure(2),'name','Left/Right Analysis','numbertitle','off')
Chan1Ref2 = Chan1 - Chan2;
Chan3Ref2 = Chan3 - Chan2;
% subplot(3,1,1)
%     plot(Chan1Ref2)
%         hold on
%     plot(Chan3Ref2,'r')
%     title('Making Channel 2 Reference for Channels 1 & 3')

Chan1Ref2 = smooth(Chan1Ref2, box2);
Chan3Ref2 = smooth(Chan3Ref2, box2);
% subplot(3,1,2)
%     plot(Chan1Ref2)
%     hold on
%     plot(Chan3Ref2,'r')
%     title(sprintf('Boxcar Filter: %d', box2))
    
Chan1Ref2 = Chan1Ref2/std(Chan1Ref2);
Chan3Ref2 = Chan3Ref2/std(Chan3Ref2);
% subplot(3,1,3)
%     plot(Chan1Ref2)
%     hold on
%     plot(Chan3Ref2,'r')
%     title('Unit Variance')
%%
% figure(3)
% set(figure(3),'name','Left/Right Analysis - Continued','numbertitle','off')
% 
% Chan1Ref2 = diff(Chan1Ref2);
% Chan1Ref2(1:400) = 0;
% Chan1Ref2(end-1000:end) = 0;
% Chan3Ref2 = diff(Chan3Ref2);
% Chan3Ref2(1:400) = 0;
% Chan3Ref2(end-1000:end) = 0;
% subplot(3,1,1)
%     plot(Chan1Ref2)
%     hold on
%     plot(Chan3Ref2,'r')
%     title('Difference')
    
% [pk1max loc1max]= findpeaks(Chan1Ref2, 'minpeakheight', ...
%     (max(Chan1Ref2)-min(Chan1Ref2))/5, 'minpeakdistance',400);
% [pk1min loc1min]= findpeaks(-Chan1Ref2, 'minpeakheight', (max(Chan1Ref2)-min(Chan1Ref2))/5, 'minpeakdistance',400);
% pk1min = -pk1min;
% [pk3max loc3max]= findpeaks(Chan3Ref2, 'minpeakheight', (max(Chan3Ref2)-min(Chan3Ref2))/5, 'minpeakdistance',400);
% [pk3min loc3min]= findpeaks(-Chan3Ref2, 'minpeakheight', (max(Chan3Ref2)-min(Chan3Ref2))/5, 'minpeakdistance',400);
% pk3min = -pk3min;
% subplot(3,1,2)
%     plot(Chan1Ref2)
%     hold on
%     plot(Chan3Ref2,'r')
%     plot(loc1max,pk1max,'go')
%     plot(loc1min,pk1min,'go')
%     plot(loc3max,pk3max,'m*')
%     plot(loc3min,pk3min,'m*')
%     title('Locating Peaks')

% count = 1;
% for i=1:length(loc1max)
%     for j = 1:length(loc3min)
%     show = abs(loc1max(i)-loc3min(j));
%     if abs(loc1max(i)-loc3min(j))<=200
%         left(count)=mean([loc1max(i) loc3min(j)]);
%         count = count + 1;
%     end
%     end
% end
%     
% count = 1;
% for i=1:length(loc1min)
%     for j = 1:length(loc3max)
%     show = abs(loc1min(i)-loc3max(j));
%     if abs(loc1min(i)-loc3max(j))<=250
%         right(count)=mean([loc1min(i) loc3max(j)]);
%         count = count + 1;
%     end
%     end
% end  
%     
% subplot(3,1,3)
% plot(Chan1Ref2)
% hold on
% plot(Chan3Ref2,'r')
% plot(right,ones(length(right))*.01,'>')
% plot(left, ones(length(left))*.01,'<g')    

%%
% figure(4)
% set(figure(4),'name','Up/Down Analysis','numbertitle','off')


Chan1 = smooth(Chan1, box2);
Chan2 = smooth(Chan2, box2);
Chan3 = smooth(Chan3, box2);

% subplot(4,1,1)
%     plot(Chan1)
%     hold on
%     plot(Chan2,'g')
%     plot(Chan3,'r')
%     title(sprintf('Boxcar Filter: %d', box2))

Chan1 = smooth(Chan1, box3);
Chan2 = smooth(Chan2, box3);
Chan3 = smooth(Chan3, box3);    
  
% subplot(4,1,2)
%     plot(Chan1)
%     hold on
%     plot(Chan2,'g')
%     plot(Chan3,'r')
%     title(sprintf('Boxcar Filter: %d', box3))
    
Chan1 = Chan1/std(Chan1);
Chan2 = Chan2/std(Chan2);
Chan3 = Chan3/std(Chan3);
% subplot(4,1,3)
%     plot(Chan1)
%     hold on
%     plot(Chan2,'g')
%     plot(Chan3,'r')
%     title('Unit Variance')

Chan1 = diff(Chan1);
Chan1(1:200) = 0;
Chan1(end-200:end) = 0;
Chan2 = diff(Chan2);
Chan2(1:200) = 0;
Chan2(end-200:end) = 0;
Chan3 = diff(Chan3);
Chan3(1:200) = 0;
Chan3(end-200:end) = 0;
%subplot(4,1,4)
    plot(Chan1)
    hold on
    plot(Chan2,'g')
    plot(Chan3,'r')
    title('Difference')
%%
% figure(5)
% set(figure(5),'name','Up/Down Analysis -- Continued','numbertitle','off')
% [pk1max2 loc1max2]= findpeaks(Chan1, 'minpeakheight', (max(Chan1)-min(Chan1))/6, 'minpeakdistance',400);
% [pk1min2 loc1min2]= findpeaks(-Chan1, 'minpeakheight', (max(Chan1)-min(Chan1))/6, 'minpeakdistance',400);
% pk1min2 = -pk1min2;
% [pk2max2 loc2max2]= findpeaks(Chan2, 'minpeakheight', (max(Chan2)-min(Chan2))/6, 'minpeakdistance',400);
% [pk2min2 loc2min2]= findpeaks(-Chan2, 'minpeakheight', (max(Chan2)-min(Chan2))/6, 'minpeakdistance',400);
% pk2min2 = -pk2min2;
% [pk3max2 loc3max2]= findpeaks(Chan3, 'minpeakheight', (max(Chan3)-min(Chan3))/6, 'minpeakdistance',400);
% [pk3min2 loc3min2]= findpeaks(-Chan3, 'minpeakheight', (max(Chan3)-min(Chan3))/6, 'minpeakdistance',400);
% pk3min2 = -pk3min2;
% 
% subplot(2,1,1)
% plot(Chan1)
% hold on
% plot(Chan2,'g')
% plot(Chan3,'r')
% plot(loc1max2,pk1max2,'bo')
% plot(loc1min2,pk1min2,'bo')
% plot(loc2max2,pk2max2,'cd')
% plot(loc2min2,pk2min2,'cd')
% plot(loc3max2,pk3max2,'m*')
% plot(loc3min2,pk3min2,'m*')
% title('Locating Peaks')
% 
% count = 1;
% for i=1:length(loc1max2)
%     for j = 1:length(loc2max2)
%         for k = 1:length(loc3max2)
%             show1 = abs(loc1max2(i)-loc2max2(j));
%             show2 = abs(loc1max2(i)-loc3max2(k));
%             if abs(loc1max2(i)-loc2max2(j))<=150 && abs(loc1max2(i)-loc3max2(k))<=150
%                 up(count)=mean([loc1max2(i) loc2max2(j) loc3max2(k)]);
%                 count = count + 1;
%             end
%         end
%     end
% end
% 
% count = 1;
% for i=1:length(loc1min2)
%     for j = 1:length(loc2min2)
%         for k = 1:length(loc3min2)
%             if abs(loc1min2(i)-loc2min2(j))<=150 && abs(loc1min2(i)-loc3min2(k))<=150
%                 down(count)=mean([loc1min2(i) loc2min2(j) loc3min2(k)]);
%                 count = count + 1;
%             end
%         end
%     end
% end
% 
% subplot(2,1,2)
% plot(Chan1)
% hold on
% plot(Chan2,'g')
% plot(Chan3,'r')
% plot(down,ones(length(down))*.01,'vr')
% plot(up, ones(length(up))*.01,'^g')

%%
% all = sort([left right up down]);
% 
% left2 = ismember(all,left);
% left2 = left2*1;
% right2 = ismember(all,right);
% right2 = right2*2;
% 
% leftright = left2+right2;
% leftright(find(leftright==0))=[];
% 
% up2 = ismember(all,up);
% up2 = up2*3;
% down2 = ismember(all,down);
% down2 = down2*4;
% 
% updown = up2+down2;
% updown(find(updown==0))=[];
% 
% Hope = left2+right2+up2+down2;
% Hope = Hope';