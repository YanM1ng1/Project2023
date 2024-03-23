import json
import numpy as np
import time
from scipy.signal import butter, filtfilt
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import neurokit2 as nk

def butter_lowpass_filter(data, cutoff_freq, fs):
    b, a = butter(4, cutoff_freq / (fs / 2), btype='low', analog=False)
    filtered_data = filtfilt(b, a, data)
    return filtered_data
# Specify the path to the JSON file
# Specify the path to the JSON files
file_paths = ['2.json', '2.json', '3.json', '4.json', '5.json', '6.json', '7_1.json', '8.json', '9_1.json', '10.json', '11.json', '12.json', '13.json', '14.json', '15.json', '16.json', '17.json', '18.json', '19.json', '20.json', '21.json', '22_1.json', '23.json', '24.json', '25.json', '26.json']

for file_path in file_paths:
    # Read the contents of the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Print the contents of the JSON file
    ppg = data['data_PPG']
    ecg = data['data_ECG']
    age = data['age']
    height = data['height']
    weight = data['weight']
    BP = data['data_BP']
    # Plot the PPG data

    # Plot the ECG data with a maximum scale of 5000
    for i in range(len(ecg)):
        if -ecg[i] + ecg[i-1]> 1000 or ecg[i] < 1000:
            ecg[i] = (ecg [i-1] + ecg[i+1]) /2
    print(ecg[7900:7950])
    for i in range(len(ppg)):
        if -ppg[i] + ppg[i-1]> 100:
            ppg[i] = (ppg [i-1] + ppg[i+1] ) /2 

    # Apply the bandpass filter to the ECG data
    b, a = butter(3, [1, 40], fs=1000, btype='band')
    filtered_ecg = filtfilt(b, a, ecg)

    # Plot the filtered ECG data
    plt.plot(filtered_ecg)
    plt.ylim(-500, 5000)
    plt.title('Filtered ECG Data')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.show()
    fs = 1000
    # Apply the bandpass filter to the PPG data
    b, a = butter(3, [0.5, 20], fs=1000, btype='band')
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
        if any(peak > peaks_time[i] for peak in peaks):
            rr_interval = min([peak - peaks_time[i] for peak in peaks if peak > peaks_time[i]])
            rr_intervals.append(rr_interval)
    print(len(rr_intervals) - len(pwts))
    while len(rr_intervals) != len(pwts) :
        rr_intervals.append(rr_intervals[-1])
    if len(rr_intervals) != len(pwts) :
        rr_intervals.append(rr_intervals[-1])
    plt.plot(peaks_time, pwts)
    plt.plot(peaks_time, rr_intervals)
    
    plt.xlabel('Time')
    plt.ylabel('Pulse Wave Transit Time (ms)')
    plt.title('Pulse Wave Transit Time vs. Time')
    #plt.show()
    #plt.plot(pwts)
    #plt.show()

    fsr = data['data_FSR']
    if 1:
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
        peaks1, _ = find_peaks(fsr_filtered)
        half_threshold = (max(fsr_filtered) + min(fsr_filtered)) / 2

        # Find peaks above and below the half threshold
        peaks_above = []
        peaks_below = []
        above_threshold = True

        for peak in peaks1:
            if above_threshold and fsr_filtered[peak] > half_threshold:
                peaks_above.append(peak)
                above_threshold = False
            elif not above_threshold and fsr_filtered[peak] < half_threshold:
                peaks_below.append(peak)
                above_threshold = True

        # Plot the filtered fsr with marked peaks
        plt.plot(fsr_filtered)
        plt.plot(peaks_above, fsr_filtered[peaks_above], 'yo', label='Above Threshold')
        plt.plot(peaks_below, fsr_filtered[peaks_below], 'go', label='Below Threshold')
        #plt.legend()
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
