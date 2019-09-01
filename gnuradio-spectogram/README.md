# gnuradio-spectogram

A simple gnuradio program using solely gnuradio's C++ API to create and run a gnuradio graph.

THe graph outline is as follows:

- File source (reads data from a binary file)
- FFT (does a complex to complex FFT)
- Pooling
- Downsampling (changes the sample rate to reduce the data size + improve efficiency of rest of processing pipeline)
- File sink (will write the straight FFT to a fiel)