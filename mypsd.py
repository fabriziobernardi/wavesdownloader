from obspy.signal.util import nextpow2, smooth
from obspy.signal import cornFreq2Paz
from scipy import fftpack
import numpy as np
import sys,os



def mper(data, win, Nfft, n1=0, n2=0):

    if (n2 == 0):
        n2 = len(data)
    n = n2 - n1
    U = pow(np.linalg.norm([win]), 2) / n
    xw = data * win
    Px = pow(abs(fftpack.fft(xw, Nfft)), 2) / (n * U)
    Px[0] = Px[1]
    return Px

def welch(data, win, Nfft, L=0, over=0):
    if (L == 0):
        L = len(data)
    n1 = 0
    n2 = L
    n0 = (1 - over) * L
    nsect = 1 + int(np.floor((len(data) - L) / (n0)))
    Px = 0
    for _i in xrange(nsect):
        Px = Px + mper(data, win, Nfft) / nsect
        n1 = n1 + n0
        n2 = n2 + n0
    return Px

def cfrequency(data, fs, smoothie, fk):

    nfft = nextpow2(data.shape[0])
    freq = np.arange(0, float(fs) - 1. / (nextpow2(data.shape[0]) / float(fs)),
                                 1. / (nextpow2(data.shape[0]) / float(fs)))
    freqaxis = freq[0:len(freq) / 2 + 1]
    cfreq = np.zeros(data.shape[0])
    if (np.size(data.shape) > 1):
        i = 0
        for row in data:
            Px_wm = welch(row, hamming(len(row)), nextpow2(len(row)))
            Px = Px_wm[0:len(Px_wm) / 2]
            cfreq[i] = np.sqrt(sum(pow(freqaxis, 2) * Px) / (sum(Px)))
            i = i + 1
        cfreq = smooth(cfreq, smoothie)
        cfreq_add = append(append([cfreq[0]] * (size(fk) // 2), cfreq),
                              [cfreq[size(cfreq) - 1]] * (size(fk) // 2))
        dcfreq = signal.lfilter(fk, 1, cfreq_add)
        dcfreq = dcfreq[size(fk) // 2:(size(dcfreq) - size(fk) // 2)]
        return cfreq, dcfreq
    else:
        Px_wm = welch(data, np.hamming(len(data)), nextpow2(len(data)))
        Px = Px_wm[0:len(Px_wm) / 2]
        cfreq = np.sqrt(np.sum(pow(freqaxis, 2) * Px) / (sum(Px)))

    return cfreq
