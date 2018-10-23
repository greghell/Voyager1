import struct
import numpy as np
import matplotlib.pyplot as plt

fname = 'voyager_1_signal'
fname2 = 'voyager_1_signal_dechirped'
nTotSam = 2**24
bandwidth = 0.0976563
fc = 8415.


newFile = open(fname2, "wb")
# TRY TO DE-CHIRP
dDrift = (16385. - 16364.)/8192./4./nTotSam     #  drift rate evaluated on spectrogram
nResol = 8192*4
nInt = 32
nTimes = nTotSam / nResol / nInt
spectro_dechirp = np.zeros((nResol,nTimes))
f = open(fname, "rb")
time_idx = 0.
for k in range(nTimes):
    tmp = np.zeros((2,nResol),dtype=float)
    for kk in range(nInt):
        data = f.read(8*2*nResol)
        signal = struct.unpack('d'*(len(data)/8), data)
        signal = np.reshape(signal, (2,len(signal)/2), order='F')
        signal = signal[0,:] + 1j*signal[1,:]
        signal = signal * np.exp(-1j*2.*np.pi*(dDrift / 2.)*(np.arange(nResol)+time_idx)**2)
        signal = np.asarray(signal)
        time_idx = time_idx + nResol
        tmp[0,:] = signal.real
        tmp[1,:] = signal.imag
        signal = np.reshape(tmp, (1,nResol*2), order='F')
        signal.tofile(newFile)

f.close()
newFile.close()


nResol = 8192*4
nInt = 16
nTimes = nTotSam / nResol / nInt
spectro = np.zeros((nResol,nTimes))
f = open(fname2, "rb")
for k in range(nTimes):
    spec = np.zeros((nResol),dtype=float)
    for kk in range(nInt):
        data = np.fromfile(f, count = 2*nResol)
        signal = np.reshape(data, (2,len(data)/2), order='F')
        signal = signal[0,:] + 1j*signal[1,:]
        spec = spec + abs(np.fft.fftshift(np.fft.fft(signal)))**2
    spectro[:,k] = spec
f.close()
plt.figure()
plt.imshow(spectro,aspect='auto',interpolation='none',extent=[0,nTotSam/bandwidth/1000000.,fc-bandwidth/2.,fc+bandwidth/2.])
plt.xlabel('time [s]')
plt.ylabel('frequency [MHz]')
plt.figure()
plt.plot(np.linspace(fc-bandwidth/2,fc+bandwidth/2,nResol),np.abs(spec))
plt.xlabel('frequency [MHz]')
plt.ylabel('power spectral density [arbitrary]')
plt.grid()
