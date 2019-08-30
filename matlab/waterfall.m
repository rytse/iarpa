function [f] = waterfall(cin, fs, wsize, overlap)
% Waterfall plot
%   cin: input signal (complex)
%   fs: sampling rate (Hz)

ELAPSED_TIME = length(cin) / fs;

% win = hanning(wsize);
win = nuttallwin(wsize);
% win = ones(wsize, 1);
f = zeros(length(win),floor(length(cin)/length(win)/2), 'single');
jj = 1;

for ii = 1 : length(win) / 2 : length(cin) - length(win)
    rep = abs(fft(cin(ii : ii + length(win) - 1) .* win)) .^ 2;
    
    rep = rep / median(rep);
    rep = mag2db(rep);
    f(:, jj) = cast(rep, 'single');
%   f(:, jj) = cast(mag2db(abs(fft(cin(ii : ii + length(win) - 1) .* win)) .^ 2), 'single');
    jj = jj + 1;
end

[k,m] = size(f);

% start_freq = 6043612 +29.7e6 + 49.3e6;
% alpha = 100e3;

gr = imagesc(linspace(0, ELAPSED_TIME, m), linspace(0, fs, k), f);
% gr = imagesc(linspace(start_freq, start_freq + alpha * ELAPSED_TIME, m) / 1e6,linspace(0, fs / (fs*100) * 3e8 / 1000, k), f);
% gr = imagesc(linspace(0, ELAPSED_TIME, m),linspace(0, 50e6 / 4, k), f(1:round(length(f)/4),:));
% gr = imagesc(linspace(0, ELAPSED_TIME, m),linspace(0, fs / 4, k), f(1:round(length(f)/4),round(m / 2) : round(m / 2 * 1.3)));

set(gca,'YDir','normal')
colormap(hsv);
colormap;

end

