import json
import numpy as np
import time
from scipy.signal import butter, filtfilt
from scipy.signal import find_peaks
import neurokit2 as nk
import tensorflow as tf
import os
import matplotlib.pyplot as plt

# Read the contents of the JSON file
with open('2.json', 'r') as file:
    data = json.load(file)
Fs = 1000
age = 18/50
height = 170/150
weight = 70/70


ppg = data['data_PPG']
ecg = data['data_ECG']
ecg = ecg[1000:3000]
ppg = ppg[1000:3000]
BP = []
b, a = butter(3, [1, 40], fs=Fs, btype='band')
filtered_ecg = filtfilt(b, a, ecg)
b, a = butter(3, [0.5, 20], fs=Fs, btype='band')
filtered_ppg = filtfilt(b, a, ppg)

"""
for i in range(Fs, len(filtered_ecg)-Fs):
    if filtered_ecg[i] > np.max(filtered_ecg[i-Fs:i+Fs])*0.8 and filtered_ecg[i] > filtered_ecg[i-1] and filtered_ecg[i] > filtered_ecg[i+1]:
        if len(peaks) == 0 or i - peaks[-1] > 0.4*Fs:
            peaks.append(i)
for i in range(Fs, len(filtered_ppg)-Fs):
    if filtered_ppg[i] > np.max(filtered_ppg[i-Fs:i+Fs])*0.8 and filtered_ppg[i] > filtered_ppg[i-1] and filtered_ppg[i] > filtered_ppg[i+1]:
        if len(peaks_ppg) == 0 or i - peaks_ppg[-1] > 0.4*Fs:
            peaks_ppg.append(i)
"""

peaks, _ = find_peaks(filtered_ecg, distance=0.4*Fs, height=np.max(filtered_ecg*0.7))
peaks_ppg, _ = find_peaks(filtered_ppg, distance=0.4*Fs, height=np.max(filtered_ppg*0.7))
print('peaks between ecg:',peaks)
print('peaks between ppg:',peaks_ppg)
pwts = []
for peak in peaks:
    closest_ppg_peak = None
    for peak_ppg in peaks_ppg:
        if peak_ppg > peak and peak_ppg - peak <= 600 :
            if closest_ppg_peak is None or peak_ppg - peak < closest_ppg_peak - peak:
                closest_ppg_peak = peak_ppg
    if closest_ppg_peak is not None:
        pwts.append(closest_ppg_peak - peak)
        #peaks_time.append(peak)
print('PWT:',pwts)
rr = []
model_path = 'model.keras'
model = tf.keras.models.load_model(model_path,compile = False)
rr = np.median(rr)
pwts = np.median(pwts)
print('check:',age, weight, height, rr, pwts)
# Preprocess the data
data = np.array([age, weight, height, rr, pwts])
# Predict using the model
predict = model.predict(data)

# Process the predictions
# ... (add your code here to process the predictions)
print('Predict:',predict)
# Print the processed predictions