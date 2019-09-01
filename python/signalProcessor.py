#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import matplotlib
#matplotlib.use('Agg')
from pylab import *
from scipy.signal import *
from scipy.fftpack import fft
from scipy.fftpack import ifft
from datetime import timedelta
import sys
import ntpath
from glob import glob
import os
import numpy as np

import pandas

# Process linear sweep
def processLinearSweep(file,  # name of raw IQ file
                 tStart,       # timedelta to start sounding 
                 tDuration,    # length of sounding
                 fBeg,         # Sweep begining frequency (Hz)
                 sweepRate,    # kHz per second
                 fEnd,         # Sweep end frequency (Hz)
                 outDir,
                 fmaxE=np.nan, foF2=np.nan, hpF2=np.nan  # optional parameters for plotting
                ):

    if not os.path.exists(outDir):
        os.makedirs(outDir)

    fileID = ntpath.basename(file)[0:-4]
    print(fileID)
    fCenter = 7e6
    fSample = 10e6

    # Pick n samples chunks
    bwPerChunk = 10e3/3e8 # (10 km / speed of light)
    nChunk0 = 2**(int(round(log2(fSample/(sweepRate*bwPerChunk))))) # factor of 2 for fft

    # Loop through sweep freq
    ionoPwr = []
    ionoSNR = []
    ionoF = []
    window = []
    print("going from", 0, "to", tDuration.total_seconds()*fSample, nChunk0)
    with open(file, "rb") as fobj:
        for i in arange(0, tDuration.total_seconds()*fSample, nChunk0):
            nChunk = nChunk0

            # Load samples
            try:
                iSample = int(tStart.total_seconds()*fSample + i)
                fobj.seek(4*iSample)
                samples = fromfile(fobj, dtype=int16, count=2*nChunk)
                samples = samples.astype(float32, copy=False)
                samples = samples.view(complex64)
                nChunk = len(samples)
                tSamples = (i + arange(nChunk))/fSample
                if nChunk <= 0:
                    break
            except:
                break

            # Current freq in sweep
            fCurrent = fBeg + sweepRate*tSamples[nChunk//2]
            sys.stdout.write('\rProcessing %0.2f MHz... ' % (fCurrent/1e6))
            if fCurrent > fEnd:
                break

            fMix = fCurrent-fCenter
            refsig = exp(-2j*pi*mod(fMix*tSamples, 1))
            samples = samples*refsig
            fIntermediate = fCurrent
            samplesFFT = fft(samples)
            desiredBW = 40e3
            decimateFactor = int(2**(round(log2(fSample/desiredBW))))
            nDownsamples = nChunk//decimateFactor
            sampleFFTds = append(samplesFFT[0:int(ceil(nDownsamples*0.5))],
                                 samplesFFT[int(-floor(nDownsamples*0.5))::])
            fDownsample = fSample*nDownsamples*1.0/nChunk
            tGridDS = arange(tSamples[0], tSamples[-1], 1/fDownsample)
            samplesDS = ifft(sampleFFTds)


            # Mix samples with mixing signal.
            # Note: 0.5 is for linear sweep's t**2
            fMix = (sweepRate*tGridDS*0.5+fBeg)-fIntermediate
            refsig = exp(-2j*pi*mod(fMix*tGridDS, 1))
            samplesMix = samplesDS*refsig

            # Ionogram processing
            if len(window) != nDownsamples:
                window = windows.hann(nDownsamples)
            samplesMix_fft = fft(window*samplesMix)
            range_res = fSample/(nChunk*sweepRate)*2.99792458e8/1e3
            nr = int(3000/range_res)
            ionoslice = 20*log10(abs(samplesMix_fft[-1:-nr-1:-1]))
            snr_slice = ionoslice-np.nanmedian(ionoslice)
            snr_slice[snr_slice < 0] = 0
            ionoPwr.append(ionoslice)
            ionoSNR.append(snr_slice)
            ionoF.append(fCurrent/1e6)

    # Plotting
    if len(ionoF) > 2:
        figure(27)
        clf()
        Z = array(ionoSNR)
        ionoR = fSample*arange(nr)/(nChunk*sweepRate) * \
            2.99792458e8/1e3/2
        pcolormesh(ionoF, ionoR, Z.T, cmap=cm.jet)
        title("linear sweep sounding, start: "+str(tStart))
        xlabel('MHz')
        ylabel('range (km)')
        clim([0, 45])
        xlim([2, 12])
        ylim([min(ionoR), max(ionoR)])
        grid(True, color='w')
        colorbar(label="SNR (dB)")

        if isfinite(fmaxE):
            plot([fmaxE, fmaxE], [min(ionoR), max(ionoR)], ":w")
            text(fmaxE, 1400, "fmaxE", color="w")
        if isfinite(foF2):
            plot([foF2, foF2], [min(ionoR), max(ionoR)], ":w")
            text(foF2, 1400, "foF2", color="w")
        if isfinite(hpF2):
            plot([2, 12], [hpF2, hpF2], ":w")
            text(11, hpF2, "h'F2", color="w")

    fnPng = ntpath.basename(file)[0:-4] + ".png"
    savefig(outDir + "/" + fnPng) 

# Process Sweep Lite
def processLinearSweepLite(fnDir,
                 sweepRate,  # Hz per second
                 outDir,
                 fmaxE=np.nan, foF2=np.nan, hpF2=np.nan  # optional parameters for plotting
                ):

    if not os.path.exists(outDir):
        os.makedirs(outDir)

    # Loop through sweep freq
    ionoPwr = []
    ionoSNR = []
    ionoF = []
    window = []
    for fnBin  in sorted(glob(fnDir+"/*.bin")):
        # Get file frequencies encoded in file name
        bn = ntpath.basename(fnBin)[0:-4]
        fCenter = float(bn.split('-')[1])*1e3
        fSample = float(bn.split('-')[2])*1e3
        with open(fnBin, "rb") as fobj:
            # Load samples
            samples = fromfile(fobj, dtype=int16)
            samples = samples.astype(float32, copy=False)
            samples = samples.view(complex64)
            nChunk = len(samples)
            tGrid = arange(nChunk)/fSample

            # Current freq in sweep
            fCurrent = fCenter
            sys.stdout.write('\rProcessing %0.2f MHz... ' % (fCurrent/1e6))

            # Mix samples with mixing signal.
            # Note: 0.5 is for linear sweep's t**2
            fBeg = -0.5*sweepRate*nChunk/fSample
            fMix = (sweepRate*tGrid*0.5+fBeg)
            refsig = exp(-2j*pi*mod(fMix*tGrid, 1))
            samples = samples*refsig

            # Ionogram processing
            if len(window) != nChunk:
                window = windows.hann(nChunk)
            samplesMix_fft = fft(window*samples)
            range_res = fSample/(nChunk*sweepRate)*2.99792458e8/1e3
            nr = int(3000/range_res)
            ionoslice = 20*log10(abs(samplesMix_fft[-1:-nr-1:-1]))
            snr_slice = ionoslice-np.nanmedian(ionoslice)
            snr_slice[snr_slice < 0] = 0
            ionoPwr.append(ionoslice)
            ionoSNR.append(snr_slice)
            ionoF.append(fCurrent/1e6)

    # Plotting
    if len(ionoF) > 2:
        figure(27)
        clf()
        Z = array(ionoSNR)
        ionoR = fSample*arange(nr)/(nChunk*sweepRate) * \
            2.99792458e8/1e3/2
        pcolormesh(ionoF, ionoR, Z.T, cmap=cm.jet)
        title("linear sweep sounding")
        xlabel('MHz')
        ylabel('range (km)')
        clim([0, 45])
        xlim([2, 12])
        ylim([min(ionoR), max(ionoR)])
        grid(True, color='w')
        colorbar(label="SNR (dB)")

        if isfinite(fmaxE):
            plot([fmaxE, fmaxE], [min(ionoR), max(ionoR)], ":w")
            text(fmaxE, 1400, "fmaxE", color="w")
        if isfinite(foF2):
            plot([foF2, foF2], [min(ionoR), max(ionoR)], ":w")
            text(foF2, 1400, "foF2", color="w")
        if isfinite(hpF2):
            plot([2, 12], [hpF2, hpF2], ":w")
            text(11, hpF2, "h'F2", color="w")
        fnPng = ntpath.basename(fnBin)[0:-4] + ".png"
        savefig(outDir + "/" + fnPng) 

# Process Pulsed
def processPulsed(fnBin,        # name of raw IQ file
                  tStart,       # timedelta to start sounding 
                  fBeg,         # Sweep begining frequency (Hz)
                  fStep,        # Frequency step (Hz)
                  fEnd,         # Sweep end frequency (Hz)
                  IPP,          # Inter pulse period
                  nRep,         # number of repeated pulses per freq
                  phaseSwitching,
                  OXMode,
                  outDir,
                  fmaxE=np.nan, foF2=np.nan, hpF2=np.nan  # optional parameters for plotting
                 ):

    if not os.path.exists(outDir):
        os.makedirs(outDir)

    # Pulse model (16-bit complementary code pair)
    baudBW = 30e3
    pCode = array([[+1, +1, -1, +1, +1, +1, +1, -1, -1, +1, +1, +1, -1, +1, -1, -1],
                   [-1, -1, +1, -1, -1, -1, -1, +1, -1, +1, +1, +1, -1, +1, -1, -1]])
    pCode = fliplr(pCode) # flip for convolution correlation
    nPCode = len(pCode[0])

    bn = ntpath.basename(fnBin)[0:-4]
    print(bn)
    fCenter = 7e6 # 7MHz always
    fSample = 10e6 # 10MHz always

    # Pick n samples chunks
    nChunk0 = int64(IPP*fSample)

    # Downsample parameters
    desiredBW = baudBW
    decimateFactor = int(2**(floor(log2(fSample/desiredBW))))
    nDownsamples = nChunk0//decimateFactor
    tChips = arange(0, IPP, 1/baudBW)

    # Loop through sweep freq
    fTunes = arange(fBeg, fEnd+fStep, fStep)
    ionoPwr = []
    ionoSNR = []
    ionoF = []
    window = []
    with open(fnBin, "rb") as fobj:
        for iFreq in range(len(fTunes)):
            fTune = fTunes[iFreq]
            sys.stdout.write('\rProcessing %0.2f MHz... ' % (fTune/1e6))
            CITVoltage = {"O": zeros([len(tChips), nRep//2], dtype=complex64),
                          "X": zeros([len(tChips), nRep//2], dtype=complex64)}
            for iRep in range(nRep):
                nChunk = nChunk0

                # Load samples
                try:
                    iSample = int64(round((tStart.total_seconds() +
                                           IPP*(nRep*iFreq + iRep)) * fSample))
                    fobj.seek(4*iSample)
                    samples = fromfile(fobj, dtype=int16, count=2*nChunk)
                    samples = samples.astype(float32, copy=False)
                    samples = samples.view(complex64)
                    nChunk = len(samples)
                    tSamples = arange(nChunk)/fSample
                    if nChunk <= 0:
                        break
                except:
                    print("signal processing. End of file?")
                    break

                # Tune
                fMix = fTune-fCenter
                refsig = exp(-2j*pi*mod(fMix*tSamples, 1))
                samples = samples*refsig

                # Down-sample
                samplesFFT = fft(samples)
                decimateFactor = int(2**(round(log2(fSample/desiredBW))))
                nDownsamples = nChunk//decimateFactor
                sampleFFTds = append(samplesFFT[0:int(ceil(nDownsamples*0.5))],
                                     samplesFFT[int(-floor(nDownsamples*0.5))::])
                fDownsample = fSample*nDownsamples*1.0/nChunk
                if len(window) != nDownsamples :
                    window = fftshift(windows.hamming(nDownsamples))
                samplesDS = ifft(window*sampleFFTds)
                tDS = arange(tSamples[0], tSamples[-1], 1/fDownsample)

                # Interp on chips' time grid (dt = baud)
                samplesChip = interp(tChips, tDS, samplesDS)

                # Correlate against phase code
                if phaseSwitching:
                    if iRep//(2+OXMode*2) % 2 == 0:
                        phaseSign = 1
                    else:
                        phaseSign = -1
                else:
                    phaseSign =1
                samplesChip = fftconvolve(samplesChip, phaseSign*pCode[iRep%2],
                        mode="full")[nPCode-1::]

                # Store voltages in 2D array
                if not OXMode:
                    CITVoltage["O"][:, iRep//2] += samplesChip
                else:
                    if (iRep//2) % 2 == 0:
                        CITVoltage["O"][:, iRep//2] += samplesChip
                    else:

                        CITVoltage["X"][:, iRep//2] += samplesChip

            # Store max dop bin per range gate
            rangePower = zeros(len(tChips))
            for pol in ["O", "X"]:
                rangeDopVoltage = fft(CITVoltage[pol], axis=1)
                maxVoltage = amax(abs(rangeDopVoltage), axis=1)
                #maxVoltage = abs(rangeDopVoltage)[:, 0]
                rangePower += abs(maxVoltage)**2

            ionoPwr.append(rangePower)
            ionoSNR.append(rangePower/median(rangePower))
            ionoF.append(fTune)

    # Plotting
    if len(ionoF) > 2:
        figure(28)
        clf()
        Z = 10*log10(array(ionoSNR))
        ionoR = tChips * 2.99792458e8/1e3/2
        pcolormesh(array(ionoF)*1e-6, ionoR, Z.T, cmap=cm.jet)
        title("pulsed sounding, start: "+str(tStart))
        xlabel('MHz')
        ylabel('range (km)')
        zfloor = 0
        clim([0, 45])
        xlim([2, 12])
        ylim([min(ionoR), max(ionoR)])
        grid(True, color='w')
        colorbar(label="SNR (dB)")

        if isfinite(fmaxE):
            plot([fmaxE, fmaxE], [min(ionoR), max(ionoR)], ":w")
            text(fmaxE, 600, "fmaxE", color="w")
        if isfinite(foF2):
            plot([foF2, foF2], [min(ionoR), max(ionoR)], ":w")
            text(foF2, 600, "foF2", color="w")
        if isfinite(hpF2):
            plot([2, 12], [hpF2, hpF2], ":w")
            text(11, hpF2, "h'F2", color="w")

        fnPng = ntpath.basename(fnBin)[0:-4] + ".png"
        savefig(outDir + "/" + fnPng)


# Process Pulsed
def processPulsedLite(fnDir,
                      IPP,     # Inter pulse period
                      nRep,    # number of repeated pulses per freq
                      phaseSwitching,
                      OXMode,
                      outDir,
                      fmaxE=np.nan, foF2=np.nan, hpF2=np.nan  # optional parameters for plotting
                     ):

    if not os.path.exists(outDir):
        os.makedirs(outDir)

    # Pulse model (16-bit complementary code pair)
    baudBW = 30e3
    pCode = array([[+1, +1, -1, +1, +1, +1, +1, -1, -1, +1, +1, +1, -1, +1, -1, -1],
                   [-1, -1, +1, -1, -1, -1, -1, +1, -1, +1, +1, +1, -1, +1, -1, -1]])
    pCode = fliplr(pCode) # flip for convolution correlation
    nPCode = len(pCode[0])
    tChips = arange(0, IPP, 1/baudBW)

    # Loop through sweep freq
    fTunes = []
    ionoPwr = []
    ionoSNR = []
    ionoF = []
    window = []
    for fnBin  in sorted(glob(fnDir+"/*.bin")):
        # Get file frequencies encoded in file name
        bn = ntpath.basename(fnBin)[0:-4]
        fCenter = float(bn.split('-')[1])*1e3
        fSample = float(bn.split('-')[2])*1e3
        nIPP = int64(round(IPP*fSample))
        with open(fnBin, "rb") as fobj:
            fTune = fCenter 
            sys.stdout.write('\rProcessing %0.2f MHz... ' % (fTune/1e6))
            CITVoltage = {"O": zeros([len(tChips), nRep//2], dtype=complex64),
                          "X": zeros([len(tChips), nRep//2], dtype=complex64)}
            for iRep in range(nRep):
                # Load samples
                iSample = int64(round(IPP*iRep*fSample))
                fobj.seek(4*iSample)
                samples = fromfile(fobj, dtype=int16, count=2*nIPP)
                samples = samples.astype(float32, copy=False)
                samples = samples.view(complex64)
                nChunk = len(samples)
                tSamples = arange(nChunk)/fSample

                # Interp on chips' time grid (dt = baud)
                samplesChip = interp(tChips, tSamples, samples)
                #samplesChip = resample(samples, len(tChips), window="hann")

                # Correlate against phase code
                if phaseSwitching:
                    if iRep//(2+OXMode*2) % 2 == 0:
                        phaseSign = 1
                    else:
                        phaseSign = -1
                else:
                    phaseSign =1
                samplesChip = fftconvolve(samplesChip, phaseSign*pCode[iRep%2],
                        mode="full")[nPCode-1::]

                # Store voltages in 2D array
                if not OXMode:
                    CITVoltage["O"][:, iRep//2] += samplesChip
                else:
                    if (iRep//2) % 2 == 0:
                        CITVoltage["O"][:, iRep//2] += samplesChip
                    else:

                        CITVoltage["X"][:, iRep//2] += samplesChip

            # Store max dop bin per range gate
            rangePower = zeros(len(tChips))
            for pol in ["O", "X"]:
                rangeDopVoltage = fft(CITVoltage[pol], axis=1)
                maxVoltage = amax(abs(rangeDopVoltage), axis=1)
                #maxVoltage = abs(rangeDopVoltage)[:, 0]
                rangePower += abs(maxVoltage)**2

            ionoPwr.append(rangePower)
            ionoSNR.append(rangePower/median(rangePower))
            ionoF.append(fTune)

    # Plotting
    if len(ionoF) > 2:
        figure(27)
        clf()
        Z = 10*log10(array(ionoSNR))
        ionoR = tChips * 2.99792458e8/1e3/2
        pcolormesh(array(ionoF)*1e-6, ionoR, Z.T, cmap=cm.jet)
        title("pulsed sounding")
        xlabel('MHz')
        ylabel('range (km)')
        zfloor = 0
        clim([0, 45])
        xlim([2, 12])
        ylim([min(ionoR), max(ionoR)])
        grid(True, color='w')
        colorbar(label="SNR (dB)")

        if isfinite(fmaxE):
            plot([fmaxE, fmaxE], [min(ionoR), max(ionoR)], ":w")
            text(fmaxE, 600, "fmaxE", color="w")
        if isfinite(foF2):
            plot([foF2, foF2], [min(ionoR), max(ionoR)], ":w")
            text(foF2, 600, "foF2", color="w")
        if isfinite(hpF2):
            plot([2, 12], [hpF2, hpF2], ":w")
            text(11, hpF2, "h'F2", color="w")

        fnPng = ntpath.basename(fnBin)[0:-4] + ".png"
        savefig(outDir + "/" + fnPng)

meta_dir = "data/meta"
linear_dir = "data/linear"

def runLinear(pandasRow):
    print(pandasRow)
    # file-id,   start time, start frequency, sweep rate, end frequency
    # train-007, 3.492539,   2000000,         90000,      12000000
    # train-000,0.643256,2000000,100,20000000
    processLinearSweep(
             file = os.path.join("data/linear", pandasRow["file-id"]) + ".bin",
             tStart = timedelta(seconds=float(pandasRow["start time"])),
             tDuration = timedelta(seconds=200),
             fBeg = pandasRow["start frequency"],
             sweepRate = pandasRow["sweep rate"],  # Hz per second
             fEnd = pandasRow["end frequency"],
             outDir = './output'
        )
    print()

if __name__ == "__main__":

    data = pandas.read_csv(os.path.join(meta_dir, "linear_params.txt"))

    # print(data)
    runLinear(data.iloc[0])

    # file-id,   start time, ipp,  num pulses per freq, start frequency, freq step, end frequency, polarization, phase shifting
    # train-006, 5.536084,   0.01, 64,                  2000000,         70000,     17286000,      O/X,          true
    # processPulsed(
            # fnBin = "train-006.bin",
            # tStart = timedelta(seconds=5, microseconds=536084), # timedelta to start sounding 
            # fBeg = 2000000,   # Sweep begining frequency (Hz)
            # fStep = 70000, # Freq step
            # fEnd = 17286000,  # Sweep end frequency (Hz)
            # IPP = 0.01,   # Inter pulse period
            # nRep = 64,   # number of repeated pulses per freq
            # phaseSwitching = True,
            # OXMode = True,
            # outDir = './'
        # )
