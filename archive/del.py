import json

# Open the original file
with open('1.json', 'r') as file:
    data = json.load(file)

# Delete the data after the 460,000th record
data['data_PPG'] = data['data_PPG'][55000:]
data['data_ECG'] = data['data_ECG'][55000:]
data['data_PCG'] = data['data_PCG'][55000:]
data['data_FSR'] = data['data_FSR'][55000:]
data['data_BP'] = data['data_BP'][1:]

# Save the modified data to a new file
with open('1_1.json', 'w') as file:
    json.dump(data, file)


# 22 80000 1