FS = 10e6;  % 20 MHz sampling rate
DUR = 16;    % We analyze 2 seconds of data
CENTER_F = 7e6; % centered at 7 MHz for pulsed

BAUD = 30e3;
FSTEP = 70000;

fid = fopen('../data/pulsed/train-002.bin');
iq = fread(fid, FS * DUR * 2, 'int16');
% iq = fread(fid, FS * DUR * 2, 'int16');
fclose(fid);
iq = deinterleve(iq);
ispec = fft(iq);

pulse = pulsegen(2e6 * .95, FS, BAUD, 0);
filt = conj(fliplr(pulse));
filt = [filt zeros(1, length(iq)-length(filt))];
fspec = fft(filt);

fo = ifft(ispec .* fspec');
plot(real(fo));

% iwf = waterfall(iq, FS, 65536);

% chirp = chirpgen(0.004137+.125, 2.0e6, 0.23+.125, 2.02e6, FS, DUR) * 2000;
% overlayed = iq + chirp;
% owf = waterfall(overlayed, FS, 65536/16);
% 
% mixed = iq .* conj(chirp);
% figure;
% mwf = waterfall(mixed, FS, 65536/16);