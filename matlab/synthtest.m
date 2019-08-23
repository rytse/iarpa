FS = 10e6;

% t0_r = 8.83449;
t0_r = 0.1;
f0_r = 2000000;

cr = 70000;

t0_i = 0;
f0_i = (t0_i - t0_r) * cr + f0_r;

el = 5;
t1_i = t0_i + el;
f1_i = f0_i + cr * el;

synth = chirpgen(t0_i, f0_i, t1_i, f1_i, FS, el);
waterfall(synth, FS, 65536/16);