import json
import numpy as np
import time
from scipy.signal import butter, filtfilt
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import neurokit2 as nk

# Specify the path to the JSON file
file_path = '7_1.json'

# Read the contents of the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)

# Print the contents of the JSON file
ppg = data['data_PPG']
ecg = data['data_ECG']

# Plot the PPG data

# Plot the ECG data with a maximum scale of 5000
for i in range(len(ecg)):
    if -ecg[i] + ecg[i-1]> 1000 or ecg[i] < 1000:
        ecg[i] = (ecg [i-1] + ecg[i+1]) /2
print(ecg[7900:7950])
for i in range(len(ppg)):
    if -ppg[i] + ppg[i-1]> 100:
        ppg[i] = (ppg [i-1] + ppg[i+1] ) /2 

# Define the bandpass filter parameters
lowcut = 1  # Lower cutoff frequency (Hz)
highcut = 40  # Upper cutoff frequency (Hz)
fs = 1000  # Sampling frequency (Hz)

# Apply the bandpass filter to the ECG data
b, a = butter(3, [lowcut, highcut], fs=fs, btype='band')
filtered_ecg = filtfilt(b, a, ecg)

# Plot the filtered ECG data
plt.plot(filtered_ecg)
plt.ylim(-500, 5000)
plt.title('Filtered ECG Data')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.show()

# Apply the bandpass filter to the PPG data
b, a = butter(3, [0.5, 20], fs=fs, btype='band')
filtered_ppg = filtfilt(b, a, ppg)

# Calculate the difference of filtered_ecg:
diff_filtered_ecg = np.diff(filtered_ecg)

# Find the peaks in the filtered ECG data

peaks = []
for i in range(1000, len(filtered_ecg)-1000):
    if filtered_ecg[i] > np.max(filtered_ecg[i-1000:i+1000])*0.8 and filtered_ecg[i] > filtered_ecg[i-1] and filtered_ecg[i] > filtered_ecg[i+1]:
        if len(peaks) == 0 or i - peaks[-1] > 400:
            peaks.append(i)

#peaks, _ = find_peaks(filtered_ecg, distance=400)


peaks_ppg = []

for i in range(1000, len(filtered_ppg)-1000):
    if filtered_ppg[i] > np.max(filtered_ppg[i-1000:i+1000])*0.8 and filtered_ppg[i] > filtered_ppg[i-1] and filtered_ppg[i] > filtered_ppg[i+1]:
        if len(peaks_ppg) == 0 or i - peaks_ppg[-1] > 400:
            peaks_ppg.append(i)

#$peaks_ppg, _ = find_peaks(filtered_ppg, distance=400, height=np.max(filtered_ppg[i-500:i+500])*0.7)
print('peaks_ppg len', len(peaks_ppg))
print('peaks len', len(peaks))

#print(max(ecg)/2)
"""
for peak in peaks:
    for peak_ppg in peaks_ppg:
        if peak_ppg > peak :
            pwts.append(peak_ppg - peak)
            break
"""
print(len(peaks))
pwts = []
peaks_time = []
rr_intervals = []
for peak in peaks:
    closest_ppg_peak = None
    for peak_ppg in peaks_ppg:
        if peak_ppg > peak and peak_ppg - peak <= 600 :
            if closest_ppg_peak is None or peak_ppg - peak < closest_ppg_peak - peak:
                closest_ppg_peak = peak_ppg
    if closest_ppg_peak is not None:
        pwts.append(closest_ppg_peak - peak)
        peaks_time.append(peak)

for i in range(1, len(peaks_time)):
    rr_interval = min([peak - peaks_time[i] for peak in peaks if peak > peaks_time[i]])
    rr_intervals.append(rr_interval)

rr_intervals.append(rr_intervals[-1])
print(len(pwts))
print(len(rr_intervals))


plt.plot(rr_intervals)
plt.plot(pwts)
plt.show()

#print(pwts)

# Plot the R-peaks of the filtered ECG data
plt.plot(filtered_ecg)
plt.plot(peaks, filtered_ecg[peaks], 'ro')
plt.title('R-Peaks of Filtered ECG Data')
plt.xlabel('Time')
plt.ylabel('Amplitude')

plt.plot(filtered_ppg)
plt.plot(peaks_ppg, filtered_ppg[peaks_ppg], 'bo')
plt.title('R-Peaks of Filtered PPG Data')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.show()

# Slowly slide the plot to the right until the last data point
for i in range(1000, len(ecg), 500):               
    #plt.plot(filtered_ecg[i-10000:i])
    #plt.plot(ecg[i-10000:i])
    #plt.plot(diff_filtered_ecg[i-10000:i])
    plt.plot(filtered_ecg[i-10000:i])

    plt.title('ECG1 Data')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    #plt.plot(filtered_ppg[i-10000:i])
    plt.plot(filtered_ppg[i-10000:i])
#    plt.ylim(-100, 100)

    plt.title('ppG1 Data')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.xticks(np.arange(0, 10000, 1000), np.arange(i-10000, i, 1000))
    plt.pause(0.1)
    plt.waitforbuttonpress()
    plt.clf()
