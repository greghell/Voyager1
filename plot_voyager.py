import struct
import numpy as np
import matplotlib.pyplot as plt
fname = 'voyager_1_signal'
nTotSam = 2**24 # pretty much...

## PLOT PSD
nResol = 8192   # resolution of Fourier transform
nReal = nTotSam / nResol  # number of realizations
f = open(fname, "rb")
spec = np.zeros((nResol),dtype=float)
for k in range(nReal):
    data = f.read(8*2*nResol)
    signal = struct.unpack('d'*(len(data)/8), data)
    signal = np.reshape(signal, (2,len(signal)/2), order='F')
    signal = signal[0,:] + 1j*signal[1,:]
    spec = spec + abs(np.fft.fftshift(np.fft.fft(signal)))**2
f.close()
plt.figure()
plt.plot(np.abs(spec))

## PLOT SPECTROGRAM
nResol = 2048   # frequency resolution
nInt = 16       # number of integrations
nTimes = nTotSam / nResol / nInt  # number of time samples
spectro = np.zeros((nResol,nTimes))
f = open(fname, "rb")
for k in range(nTimes):
    spec = np.zeros((nResol),dtype=float)
    for kk in range(nInt):
        data = f.read(8*2*nResol)
        signal = struct.unpack('d'*(len(data)/8), data)
        signal = np.reshape(signal, (2,len(signal)/2), order='F')
        signal = signal[0,:] + 1j*signal[1,:]
        spec = spec + abs(np.fft.fftshift(np.fft.fft(signal)))**2
    spectro[:,k] = spec
f.close()
plt.figure()
plt.imshow(spectro,aspect='auto',interpolation='none')
