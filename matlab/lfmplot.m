FS = 10e6;  % 20 MHz sampling rate
DUR = 5;    % We analyze 2 seconds of data

% fid = fopen('../data/linear/train-000.bin');
fid = fopen('../data/pulsed/train-002.bin');
% iq = fread(fid, FS * DUR * 2, 'int16');
% iq = fread(fid, FS * DUR * 2, 'int16');
iq = fread(fid, FS * DUR * 2, 'int16');
fclose(fid);
iq = deinterleve(iq);

waterfall(iq, FS, 65536/16);