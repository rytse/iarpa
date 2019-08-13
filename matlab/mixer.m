lfmplot
figure
synthtest
figure

mixed = iq .* conj(synth);
waterfall(mixed, FS, 65536/16);