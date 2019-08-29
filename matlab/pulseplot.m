FS = 10e6;  % 20 MHz sampling rate
DUR = 8;    % We analyze 2 seconds of data
CENTER_F = 7e6; % centered at 7 MHz for pulsed

fid = fopen('../data/pulsed/train-002.bin');
iq = fread(fid, FS * DUR * 2, 'int16');
fclose(fid);
iq = deinterleve(iq);

iwf = waterfall(iq, FS, 65536/256);

% chirp = chirpgen(0.004137+.125, 2.0e6, 0.23+.125, 2.02e6, FS, DUR) * 2000;
% overlayed = iq + chirp;
% owf = waterfall(overlayed, FS, 65536/16);
% 
% mixed = iq .* conj(chirp);
% figure;
% mwf = waterfall(mixed, FS, 65536/16);