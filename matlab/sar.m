% Like lfmplot but with less other stuff plotted. Somewhat depreciated
% (i.e. not checked by Ryan after finally getting ionograms to work), so
% you should refer to lfmplot.m

FS = 20e6;
DECIM = 200;
DUR = 10;

WSIZE = 65536;

fid = fopen('../../gr-chirphunter/data/out/mix.out');
m = deinterleve(fread(fid, FS * DUR * 2, 'float32'));
fclose(fid);

wf = waterfall(m, FS, WSIZE);

figure;
rep = diff(sum(wf, 2));
plot(rep);

[a b] = max(rep);
target = b / length(rep) * FS

figure(1);
ylim([target * 0.99 target * 1.01])

sh = target - FS / DECIM / 2