#!/usr/bin/env bash


export GNU_RADIO_PATH=/miniconda3/envs/dsp
export PATH=/opt/qt/bin:$PATH:/miniconda3/envs/dsp/bin
export LD_LIBRARY_PATH=/opt/qt/lib:/usr/local/lib:$LD_LIBRARY_PATH:/miniconda3/envs/dsp/lib
export PKG_CONFIG_PATH=/opt/qt/lib/pkgconfig:$PKG_CONFIG_PATH:/miniconda3/envs/dsp/lib/pkgconfig
export PYTHONPATH=:/lib/python3.7/dist-packages

echo "Setting up build directory"
mkdir build
cd build

echo "running cmake"
cmake ../

echo "compiling"
make

# make install