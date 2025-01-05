import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from scipy.fft import fft, fftfreq
import soundfile as sf
from scipy.signal import find_peaks, peak_prominences, savgol_filter
import json


def truncate_fft(xf, yf, lower_bound=0, upper_bound=1200):
    filtered_xf = [i for i in xf if lower_bound <= i < upper_bound]
    filtered_xf_indices = [filtered_xf.index(i) for i in filtered_xf]
    filtered_yf = [yf[i] for i in filtered_xf_indices]
    return filtered_xf, filtered_yf


# INPUT:
#        file: directory from root of project to a .wav file
#        domain: either time or frequency, latter is the fft
def plot_audio(file, domain="time", truncate=False):
    samplerate, data = wavfile.read(file)
    if domain == "time":
        plt.title(f"{file} - audio")
        f = sf.SoundFile(file)
        plt.plot(np.linspace(0, f.frames / f.samplerate, len(list(data[:, 0]))), data[:, 0])
        plt.xlabel("Time (sec)")
        plt.ylabel("Air Pressure (...)")
    elif domain == "frequency":
        plt.title(f"{file[file.rfind('/') + 1:]} - Discrete Fourier Transform")
        xf = fftfreq(data.shape[0], 1 / samplerate)
        yf = np.abs(fft(data[:, 0]))
        if truncate:
            xf, yf = truncate_fft(xf, yf)
        #yf = np.abs(savgol_filter(yf, window_length=501, polyorder=3))
        #plt.plot(np.linspace(0, 2000, 2000), np.linspace(np.pow(10, 12), np.pow(10, 12), 2000))
        plt.plot(xf, yf)
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Amplitude (...)")
    plt.show()


file = "Guitar/Notes/Gb.wav"
plot_audio(file, domain="frequency", truncate=True)

samplerate, data = wavfile.read(file)
xf = fftfreq(data.shape[0], 1 / samplerate)
yf = np.abs(fft(data[:, 0]))
xf, yf = truncate_fft(xf, yf)


#xf, yf = truncate_fft(xf, np.abs(savgol_filter(yf, window_length=501, polyorder=3)))

# maybe use the global max(s) as a height threshold?
peaks = find_peaks(yf, height=np.pow(10, 0), distance=15 * int(len(xf) / 1200))[0]
peak_freqs = [round(xf[i], 3) for i in peaks if xf[i] >= 0]
proms = peak_prominences(yf, peaks)[0]

peak_prom_dict = {k: v for k, v in (sorted(dict(zip(peak_freqs, proms)).items(), key=lambda item: item[1]))}
"""for key, value in peak_prom_dict.items():
    print(f"{key, } Hz, amp: {'{:.2e}'.format(value)} prominence")"""

peaks_with_freq = [(i, j) for (i, j) in zip(list(peaks), list(peak_freqs))]
for i in peaks_with_freq:
    print(i)


print("\n\n")


# INPUT:
#        f: given frequency of note
#        f0: reference frequency, defaults to the low open E string
# OUTPUT: An integer number of semitones 'f' is away from 'f0'.
#         Its sign is postive for 'f' > 'f0' and negative
#         for 'f' < f0
def get_note(f, f0="E"):
    return int(np.round(12 * np.log2(f / open_string_frequencies[f0])))


# could also define this programmatically based on the tuning of the instrument
open_string_frequencies = {
    "e": 329.63,
    "B": 246.94,
    "G": 196.00,
    "D": 146.83,
    "A": 110.00,
    "E": 82.41,
}


# INPUT:
#        string: one of the names in 'open_string_frequencies'
#        frets: number of frets on the guitar
#        precision: number of decimals the frequencies are round to, default is 3
# OUTPUT: Dictionary with the nth key corresponding to the nth fret's
#         name and the nth value corresponding to the respective
#         frequency of the nth key
def string_freq_dict(string, frets=22, precision=2):
    string_num = range(0, 1 + frets)
    return {k: v for (k, v) in zip([f"{string}{i}" for i in string_num],
                                   [float(round(open_string_frequencies[string] * np.pow(2, i / 12), precision)) for i
                                    in
                                    string_num])}


def string_freq_list(string, frets=22, precision=2):
    string_num = range(0, 1 + frets)
    return [float(round(open_string_frequencies[string] * np.pow(2, i / 12), precision)) for i in string_num]


# Fretboard Dictionary
fretboard_dict_dict = {k: v for (k, v) in zip(list(open_string_frequencies.keys()),
                                              [string_freq_dict(i) for i in list(open_string_frequencies.keys())])}

# Fretboard Dictionary with the values of each string just a list of frequencies, where an index of the list is
# the fret number, starting with the zero index as the open string
fretboard_dict_list = {k: v for (k, v) in zip(list(open_string_frequencies.keys()),
                                              [string_freq_list(i) for i in list(open_string_frequencies.keys())]
                                              )}


# INPUT:
#        note: the frequency of a given note
#        threshold: the amount of deviation from the true value of a fret's
#        frequency that is allowed to still be considered a valid note i.e.
#        if 'note' is ± 'threshold' away from a given note on the fretboard
#        then that note on the fret board will count
# OUTPUT: returns a list of possible notes on the fretboard
#         that given note could have come from
def get_possible_notes(note):
    notes = []
    for string, frets in fretboard_dict_dict.items():
        freq = list(frets.values())
        closest_note = freq[min(range(len(freq)), key=lambda i: abs(freq[i] - note))]
        note_name = list(frets.keys())[list(frets.values()).index(closest_note)]

        if np.abs(closest_note - note) <= closest_note * (0.5 * (np.pow(2, 1/12) - 1)) and np.abs(closest_note - note) <= closest_note * (0.5 * (1 - np.pow(2, -1 / 12))):
            notes.append(list(frets.keys())[list(frets.values()).index(closest_note)])

    return list(reversed(notes))


a = np.abs(196 - 185.98575637757048)
b = 196 * (1 / 2 * (1 - np.pow(2, -1 / 12)))
print(a)
print(b)
print(a - b)


def harmoic_series(val, n):
    return [val * i for i in range(1, n + 1)]


# print(harmoic_series(233.20517589062544, 4))


# Reduces the noise in the peak detection by taking the average of values close to each other
def combine_similar_freq(freqs):
    comfreqs = []
    for f in freqs:
        similar_vals = [i for i in freqs if np.abs(i - f) <= f * (0.5 * (np.pow(2, 1/12) - 1))]
        comfreqs.append(round(sum(similar_vals) / len(similar_vals), 3))
    return list(sorted(set(comfreqs)))



for i in combine_similar_freq(peak_freqs):
    print(f"{i}: {get_possible_notes(i)}")
