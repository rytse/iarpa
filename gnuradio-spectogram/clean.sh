#!/usr/bin/env bash

env
echo "done"

. ~/.bashrc


# export GNU_RADIO_PATH=/miniconda3/envs/dsp
# export PATH=/opt/qt/bin:$PATH:/miniconda3/envs/dsp/bin
# export LD_LIBRARY_PATH=/opt/qt/lib:/usr/local/lib:$LD_LIBRARY_PATH:/miniconda3/envs/dsp/lib
# export PKG_CONFIG_PATH=/opt/qt/lib/pkgconfig:$PKG_CONFIG_PATH:/miniconda3/envs/dsp/lib/pkgconfig
# export PYTHONPATH=:/lib/python3.7/dist-packages

env

echo "Cleaning up build directory"
rm -rf build
echo "done"