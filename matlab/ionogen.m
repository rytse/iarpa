% Sampling consts
FS = 20e6;
DECIM = 200;

% Spectrogram consts
WSIZE = 2^17;
OVERLAP = WSIZE * 15 / 16;

% Read the mixed output file
fid = fopen('../../gr-chirphunter/data/out/mdo.out');
m = deinterleve(fread(fid, 'float32'));
fclose(fid);

% Get spectrogram and normalize across col
[~,f,t,p] = spectrogram(m, nuttallwin(WSIZE), OVERLAP, WSIZE, FS / DECIM, 'yaxis');
for k = 1:size(p, 2)
    p(:,k) = p(:, k) / median(p(:, k));
end

% Plot spectrogram
imagesc(t / 60, f / 1e3, mag2db(p .^ 2));
xlabel('Time (minutes)')
ylabel('Frequency (kHz)')
set(gca,'YDir','normal')