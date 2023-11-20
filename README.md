
# IARPA

Solution to the [IARPA PINS](https://www.iarpa.gov/challenges/pins.html) Master challenge on [Topcoder](https://www.topcoder.com/challenges/30094205).

## Files
### matlab
Matlab utility scripts for developing the algorithm for extracting ionograms from samples given sounder parameters.

* `chirpgen.m` generates a linear frequency modulated (LFM) chirp
* `waterfall.m` generates a spectrogram of a given signal
* `deinterleve.m` separates a real-valued complex vector of the form `[i_0, q_0, i_1, q_1, ...]` into a complex-valued complex vector of the form `[i_0 + j * q_0, i_1 + j * q_1, ...]`
* `lfmplot.m` plots the spectrogram of the first few seconds of train-000.iq
* `pulseplot.m` plots the spectorgram of the first few seconds of train-002.iq
* `synthtest.m` and `mixer.m` don't really do anything interesting yet
### python
Python notebooks for figuring out how to determine sounder parameters given samples (from the old [hcf repo](https://gitlab.com/blair3sat/hcf) and a bunch of assorted (old) scripts.

