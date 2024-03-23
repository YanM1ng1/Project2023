import serial
import struct
from scipy import signal
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt 
ser_ble = serial.Serial('COM4',115200,bytesize=8)

plt.ion()
fig,ax=plt.subplots(3,1)

while 1 :
    iir_data = []
    ecg_data = []
    ppg_data = []
    for i in range(500):
        print(i)
        while 1 :

            a = ser_ble.read(size=1)
            if a == b'1' :
                break
        data_raw = ser_ble.read(size=4)
        iir_byte = bytearray()
        iir_byte.append(data_raw[3])
        iir_byte.append(data_raw[2])
        iir_byte.append(data_raw[1])
        iir_byte.append(data_raw[0])
        iir_data.append(struct.unpack('!f', iir_byte)[0])

        data_raw = ser_ble.read(size=4)
        ppg_byte = bytearray()
        ppg_byte.append(data_raw[3])
        ppg_byte.append(data_raw[2])
        ppg_byte.append(data_raw[1])
        ppg_byte.append(data_raw[0])
        ppg_data.append(struct.unpack('!f', ppg_byte)[0])

        data_raw = ser_ble.read(size=4)
        print(data_raw)
        ecg_byte = bytearray()
        ecg_byte.append(data_raw[3])
        ecg_byte.append(data_raw[2])
        ecg_byte.append(data_raw[1])
        ecg_byte.append(data_raw[0])
        ecg_data.append((struct.unpack('!f', ecg_byte)[0]))
        #ecg_data.append((data_raw[0]<<24 | data_raw[1]<<16 | data_raw[2]<<8 | data_raw[3]))
        #ecg_data.append((data_raw[0]<<24 | data_raw[1]<<16 | data_raw[2]<<8 | data_raw[3])*12.247e-6/76)
    ax[0].cla()
    ax[0].plot(iir_data)
    ax[1].cla()
    ax[1].plot(ppg_data)
    ax[2].cla()
    ax[2].plot(ecg_data)
    plt.pause(0.01)

    # Apply 60Hz band stop filter to ecg_data
