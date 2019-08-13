FS = 20e6;  % 20 MHz sampling rate
DUR = 2;    % We analyze 2 seconds of data

fid = fopen('../data/train-000.bin');
iq = fread(fid, FS * DUR * 2, 'int16');
fclose(fid);
iq = deinterleve(iq);

waterfall(iq, FS);