import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from scipy.fft import fft, fftfreq
import soundfile as sf



samplerate, data = wavfile.read("cmos.wav")
length = data.shape[0] / samplerate
f = sf.SoundFile("Guitar/Notes/Ab.wav")
duration = f.frames / f.samplerate
bin_size = 1000

a = np.array(list(np.fft.fft(data[i * bin_size:(i + 1) * bin_size, 0]) for i in range(data.shape[0] // bin_size)))

#plt.plot(time, data[:, 0])
sec = 8

reduction = 1
audio_bin = data[sec * int(len(a) / duration) * bin_size:(sec + 1) * int(len(a) / duration) * bin_size, 0][::reduction]

yf = fft(audio_bin)
xf = fftfreq(audio_bin.shape[0], 1 / samplerate)

#plt.plot(xf, np.abs(yf))
#plt.xlabel("Frequency (Hz)")
#plt.ylabel("Amplitude")
#plt.show()

