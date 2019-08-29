FS = 20e6;  % 20 MHz sampling rate
DUR = 5;    % We analyze 2 seconds of data

fid = fopen('../data/linear/train-000.bin');
% fid = fopen('../data/pulsed/train-002.bin');
iq = fread(fid, FS * DUR * 2, 'int16');
iq = fread(fid, FS * DUR * 2, 'int16');
iq = fread(fid, FS * DUR * 2, 'int16');
iq = fread(fid, FS * DUR * 2 * 2, 'int16');
fclose(fid);
iq = deinterleve(iq);

wf = waterfall(iq, FS, 65536/16);

figure;
pooled = blockproc(wf, [20 20], @(block_struct) max(block_struct.data));
imagesc(linspace(0, 5, size(pooled, 1)), linspace(0, 20, size(pooled, 2)), pooled);
set(gca,'YDir','normal')
colormap(hsv);