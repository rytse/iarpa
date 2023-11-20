FROM blair3sat/gnuradio

WORKDIR /workdir

# ENV CMAKE_PREFIX_PATH /miniconda3/envs/dsp/lib/cmake/gnuradio

COPY . /workdir

# RUN env

RUN ./clean.sh

RUN ./build.sh

FROM blair3sat/gnuradio

COPY --from=0 /workdir/bin/gnuradio-spectogram /usr/local/bin/gnuradio-spectogram

CMD /usr/local/bin/gnuradio-spectogram