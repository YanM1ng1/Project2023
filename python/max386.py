import serial
import struct
import matplotlib.pyplot as plt 
ser_ble = serial.Serial('COM6',38400,bytesize=8)

start = 'ajdewisojfdsaio'
#ser_ble.write(start.encode())
print("tranmitdone")
ecg_data = []
ppg_data = []

for i in range(100):
    while 1 :
        a =ser_ble.read(size=1)

        if a == b'1' :
            break
    data_raw = ser_ble.read(size=4)
    ppg_byte = bytearray()
    ppg_byte.append(data_raw[3])
    ppg_byte.append(data_raw[2])
    ppg_byte.append(data_raw[1])
    ppg_byte.append(data_raw[0])
    ppg_data.append(struct.unpack("!f",ppg_byte)[0])

    data_raw = ser_ble.read(size=4)

    ecg_byte = bytearray()
    ecg_byte.append(data_raw[3])
    ecg_byte.append(data_raw[2])
    ecg_byte.append(data_raw[1])
    ecg_byte.append(data_raw[0])
 #   print(struct.unpack("!f",ecg_byte)[0])
    ecg_data.append(struct.unpack("!f",ecg_byte)[0])   
print(ecg_data)
fig,ax=plt.subplots(2,1)
ax[0].plot(ecg_data)
ax[1].plot(ppg_data)
fig.suptitle('ECG and PPG DATA',fontsize=16)
plt.show()