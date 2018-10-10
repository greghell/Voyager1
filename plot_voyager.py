import struct
import numpy as np
import matplotlib.pyplot as plt
fname = 'voyager_1_signal'
nTotSam = 2**24
bandwidth = 0.0976563
fc = 8415.

## PLOT PSD
nResol = 8192
nReal = nTotSam / nResol
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
plt.plot(np.linspace(fc-bandwidth/2,fc+bandwidth/2,nResol),np.abs(spec))
plt.xlabel('frequency [MHz]')
plt.ylabel('power spectral density [arbitrary]')
plt.grid()


## PLOT SPECTROGRAM
nResol = 8192*4
nInt = 16
nTimes = nTotSam / nResol / nInt
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
plt.imshow(spectro,aspect='auto',interpolation='none',extent=[0,nTotSam/bandwidth/1000000.,fc-bandwidth/2.,fc+bandwidth/2.])
plt.xlabel('time [s]')
plt.ylabel('frequency [MHz]')


# TRY TO DE-CHIRP
dDrift = (16385. - 16364.)/8192./4./nTotSam     #  drift rate evaluated on spectrogram
nResol = 8192*4
nInt = 32
nTimes = nTotSam / nResol / nInt
spectro_dechirp = np.zeros((nResol,nTimes))
f = open(fname, "rb")
time_idx = 0.
for k in range(nTimes):
    spec = np.zeros((nResol),dtype=float)
    for kk in range(nInt):
        data = f.read(8*2*nResol)
        signal = struct.unpack('d'*(len(data)/8), data)
        signal = np.reshape(signal, (2,len(signal)/2), order='F')
        signal = signal[0,:] + 1j*signal[1,:]
        signal = signal * np.exp(-1j*2.*np.pi*(dDrift / 2.)*(np.arange(nResol)+time_idx)**2)
        time_idx = time_idx + nResol
        spec = spec + abs(np.fft.fftshift(np.fft.fft(signal)))**2
    spectro_dechirp[:,k] = spec
f.close()
plt.figure()
plt.imshow(spectro_dechirp,aspect='auto',interpolation='none',extent=[0,nTotSam/bandwidth/1000000.,fc-bandwidth/2.,fc+bandwidth/2.])
plt.xlabel('time [s]')
plt.ylabel('frequency [MHz]')

plt.figure()
plt.plot(np.linspace(fc-bandwidth/2,fc+bandwidth/2,nResol),np.mean(spectro_dechirp,axis = 1),label='de-chirped signal')
plt.plot(np.linspace(fc-bandwidth/2,fc+bandwidth/2,nResol),np.mean(spectro,axis = 1),label='non-processed signal')
plt.legend()
plt.xlabel('frequency [MHz]')
plt.ylabel('power spectral density [arbitrary]')
plt.grid()
