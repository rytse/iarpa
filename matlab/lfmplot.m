% Use this script on data *before* downsampling to find where the LFM is in
% the raw bandwidth. This script prints the frequency by which you should
% shift the signal in order to get the LFM within the decimated bandwidth,
% and shift.m will simulate that shift.

% Sampling consts
FS = 20e6;
DUR = 10;
DECIM = 200;

% Read the input data
fid = fopen('../data/linear/train-000.bin');
tfid = fopen('../../gr-chirphunter/data/out/templ.out');
for skip = 1:2
    iq = fread(fid, FS * DUR * 2, 'int16');
    templ = fread(tfid, FS * DUR * 2, 'float32');
end
fclose(fid);
fclose(tfid);
iq = deinterleve(iq);
templ = deinterleve(templ);

% NOTE: uncommenting this will make more pretty plots! Or you might run out
% of RAM. Good luck!
% figure;
% iwf = waterfall(iq, FS, 65536/16);
% title('In');
% 
% figure;
% twf = waterfall(templ, FS, 65536/16);
% title('Template');

% Plot mixed output
figure;
mixed = iq .* conj(templ);
mwf = waterfall(mixed, FS, 65536);
title('Mixed');

% Sum across rows to find the frequency at which the LFM is
figure;
sar = sum(mwf, 2);
plot(sar);
title('Sum Across Rows of Mixed Spectrogram');
[a b] = max(sar);
target = b / length(sar) * FS

% Zoom in appropriately on the LFM
figure(1)
ylim([target * 0.99 target * 1.01])