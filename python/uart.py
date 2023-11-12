import serial 
ser_ble = serial.Serial('COM6',38400,bytesize=8)

  
start = 'ajdewisojfdsaio'
ser_ble.write(start.encode())
data_raw = ser_ble.read(size=1)
print("tranmitdone")