% Use this script to check the effect of freq shifting your mixed signal in
% order to get the LFM within decimated bandwidth

% Calculate shift needed to put the LFM in the middle of the decimated BW
sh = target - FS / DECIM / 2;
carrier = exp(2.0j * pi * linspace(0, DUR, length(m)) * sh);

% Mix and calculate the spectrogram
mm = carrier' .* m;
mwf = waterfall(mm, FS, WSIZE);

% Sum across rows to find / confirm the frequency that the LFM is at
figure;
mrep = diff(sum(mwf, 2));
plot(mrep);
[ma mb] = max(mrep);
mtarget = mb / length(mrep) * FS