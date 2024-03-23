import json
import numpy as np
import time
from scipy.signal import butter, filtfilt
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import neurokit2 as nk

# Define the butter_lowpass_filter function
def butter_lowpass_filter(data, cutoff_freq, fs):
    b, a = butter(4, cutoff_freq / (fs / 2), btype='low', analog=False)
    filtered_data = filtfilt(b, a, data)
    return filtered_data

# Specify the path to the JSON file
# Specify the path to the JSON files
file_paths = ['1.json', '2.json', '3.json', '4.json', '5.json', '6.json', '7_1.json', '8.json', '9_1.json', '10.json', '11.json', '12.json', '13.json', '14.json', '15.json', '16.json', '17.json', '18.json', '19.json', '20.json', '21.json', '22_1.json', '23.json', '24.json', '25.json', '26.json']

# Loop through each file path
for file_path in file_paths:
    # Read the contents of the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Print the contents of the JSON file
    fsr = data['data_FSR']
    bp = data['data_BP']

    fsr = np.array(fsr)
    print(bp)
    fsr = 4096 - fsr

    a = max(fsr)*0.9
    for i in range(1,5000):
        if fsr[i] > a:
            fsr[i] = 0

    for i in range(len(fsr)):
        if -fsr[i] + fsr[i-1] > 100 or fsr[i] - fsr[i-1] > 100:
            fsr[i] = (fsr[i-1] + fsr[i+1]) / 2

    #plt.plot(fsr)
    plt.title(file_path)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
 #   plt.show()
    # Apply lowpass filter to fsr
    fsr_filtered = butter_lowpass_filter(fsr, cutoff_freq=1, fs=1000)

    # Plot the filtered fsr
    #plt.plot(fsr_filtered)
    # Find peaks in the filtered fsr signal
    peaks, _ = find_peaks(fsr_filtered)
    half_threshold = (max(fsr_filtered) + min(fsr_filtered)) / 2

    # Find peaks above and below the half threshold
    peaks_above = []
    peaks_below = []
    above_threshold = True

    for peak in peaks:
        if above_threshold and fsr_filtered[peak] > half_threshold:
            peaks_above.append(peak)
            above_threshold = False
        elif not above_threshold and fsr_filtered[peak] < half_threshold:
            peaks_below.append(peak)
            above_threshold = True

    # Plot the filtered fsr with marked peaks
    plt.plot(fsr_filtered)
    plt.plot(peaks_above, fsr_filtered[peaks_above], 'ro', label='Above Threshold')
    plt.plot(peaks_below, fsr_filtered[peaks_below], 'bo', label='Below Threshold')
    plt.legend()
    plt.show()
