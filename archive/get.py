import ast
import random
import tensorflow as tf
import numpy as np
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '3'
from tensorflow.keras.layers import Input


"""
Age
Weight
Height
index
PWTS
RR
"""
Ages = []
Weights = []
Heights = []
indexs = []
PWTSs = []
RRs = []
a = 0 
# Open the file in read mode
with open('output2.txt', 'r') as file:
    # Read the contents of the file
    contents = file.read()
    # Print the contents
    # Split the contents by newline character
    lines = contents.split('\n')
    age_one= []
    weight_one = []
    height_one = []
    # Iterate over each line
for line in lines:
    # Print the line
    if line[:3] == 'Age':
        age_one.append(int(line[5:]))
        age = age_one[0]
        
    if line[:6] == 'Weight':
        weight_one.append(int(line[8:]))
        weight = weight_one[0]
        
    if line[:6] == 'Height':
        height_one.append(int(line[8:]))
        height = height_one[0]
        
    if line[:5] == 'index':
        BP = ast.literal_eval(line[7:])
        lenbp = len(BP)

    if line[:4] == 'PWTS':
        PWTS = ast.literal_eval(line[6:])
        PWTSs.append(PWTS)
    if line[:2] == 'RR':
        RR = ast.literal_eval(line[14:])
        RRs.append(RR)
        
        while(lenbp != len(age_one)):
            age_one.append(age)
            weight_one.append(weight)
            height_one.append(height)

        Ages.append(age_one)
        Weights.append(weight_one)
        indexs.append(BP)
        Heights.append(height_one)
        age_one = []
        weight_one = []
        height_one = []

        
        
# Convert the string to a list of dictionaries
#data = ast.literal_eval(a)
final_ages = []
final_weights = []
final_heights = []
final_RRs = []
final_PWTSs = []
final_SBP = []
final_DBP = []

for i in range(len(Ages)):
    for j in range(len(Ages[i])):
        final_ages.append(Ages[i][j])
        final_weights.append(Weights[i][j])
        final_heights.append(Heights[i][j])
        final_RRs.append(RRs[i][j])
        final_PWTSs.append(PWTSs[i][j])
        final_SBP.append(indexs[i][j]['SBP'])
        final_DBP.append(indexs[i][j]['DBP'])

# Shuffle the data with the same random seed
random.seed(42)
data_count = len(final_ages)
a = [i for i in range(data_count)]
random.shuffle(a)
final_ages = [final_ages[i] for i in a]
final_weights = [final_weights[i] for i in a]
final_heights = [final_heights[i] for i in a]
final_RRs = [final_RRs[i] for i in a]
final_PWTSs = [final_PWTSs[i] for i in a]
final_SBP = [final_SBP[i] for i in a]
final_DBP = [final_DBP[i] for i in a]
final_ages = np.array(final_ages)/50
final_weights = np.array(final_weights)/70
final_heights = np.array(final_heights)/150
final_RRs = np.array(final_RRs)/1000
final_PWTSs = np.array(final_PWTSs)/200
final_SBP = np.array(final_SBP)/100
final_DBP = np.array(final_DBP)/100
# Calculate the sizes of each dataset
total_samples = data_count
train_size = int(0.7 * total_samples)
test_size = int(0.2 * total_samples)
val_size = int(0.1 * total_samples)

# Split the data into train, test, and validation sets
train_ages = final_ages[:train_size]
train_weights = final_weights[:train_size]
train_heights = final_heights[:train_size]
train_RRs = final_RRs[:train_size]
train_PWTSs = final_PWTSs[:train_size]
train_SBP = final_SBP[:train_size]
train_DBP = final_DBP[:train_size]

test_ages = final_ages[train_size:train_size + test_size]
test_weights = final_weights[train_size:train_size + test_size]
test_heights = final_heights[train_size:train_size + test_size]
test_RRs = final_RRs[train_size:train_size + test_size]
test_PWTSs = final_PWTSs[train_size:train_size + test_size]
test_SBP = final_SBP[train_size:train_size + test_size]
test_DBP = final_DBP[train_size:train_size + test_size]

val_ages = final_ages[train_size + test_size:]
val_weights = final_weights[train_size + test_size:]
val_heights = final_heights[train_size + test_size:]
val_RRs = final_RRs[train_size + test_size:]
val_PWTSs = final_PWTSs[train_size + test_size:]
val_SBP = final_SBP[train_size + test_size:]
val_DBP = final_DBP[train_size + test_size:]
print(train_ages[0])
print(train_weights[0])
print(train_heights[0])
print(train_RRs[0])
print(train_PWTSs[0])
print(train_SBP[0])
print(train_DBP[0])
# Print the sizes of each dataset
# Define the model architecture
model = tf.keras.Sequential([
    tf.keras.layers.Dense(512, activation='relu', input_shape=(5,)),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(2)
])

# Convert the data to numpy arrays
train_data = tf.convert_to_tensor(list(zip(train_ages, train_weights, train_heights, train_RRs, train_PWTSs)))
train_labels = tf.convert_to_tensor(np.array([train_SBP, train_DBP]).T)  # Convert train_labels to have shape (32, 2)

val_data = tf.convert_to_tensor(list(zip(val_ages, val_weights, val_heights, val_RRs, val_PWTSs)))
val_labels = tf.convert_to_tensor(np.array([val_SBP, val_DBP]).T)  # Convert val_labels to have shape (32, 2)

# Define the model architecture
# Compile the model
model.compile(optimizer='adam', loss='mse', metrics=['mae'])
# Set the batch size
batch_size = 16

# Train the model
history = model.fit(train_data, train_labels, validation_data=(val_data, val_labels), epochs=50, batch_size=batch_size)
# Save the model
model.save('model.keras')
import matplotlib.pyplot as plt

# Plot the loss curve
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

test_data = tf.convert_to_tensor(list(zip(test_ages, test_weights, test_heights, test_RRs, test_PWTSs)))
test_labels = tf.convert_to_tensor(np.array([test_SBP, test_DBP]).T)
val_data = tf.convert_to_tensor(list(zip(val_ages, val_weights, val_heights, val_RRs, val_PWTSs)))
val_labels = tf.convert_to_tensor(np.array([val_SBP, val_DBP]).T)
# Evaluate the model
loss = model.evaluate(test_data, test_labels)
print('Test loss:', loss)
# Make predictions
predictions = model.predict(val_data)
error = predictions - val_labels
# Calculate the mean absolute error
mae = np.mean(np.abs(error), axis=0)

# Print the mean absolute error for SBP and DBP
print('Mean Absolute Error (SBP):', mae[0])
print('Mean Absolute Error (DBP):', mae[1])

# Plot the error for SBP and DBP
import matplotlib.pyplot as plt

# Plot the error for SBP and DBP
plt.scatter(val_labels[:, 0]*100, predictions[:, 0]*100, label='SBP')
plt.scatter(val_labels[:, 1]*100, predictions[:, 1]*100, label='DBP')
plt.xlabel('Actual')
plt.ylabel('Target')
plt.legend()
plt.show()

# Calculate the correlation coefficient (r) for SBP and DBP
r_sbp = np.corrcoef(val_labels[:, 0], predictions[:, 0])[0, 1]
r_dbp = np.corrcoef(val_labels[:, 1], predictions[:, 1])[0, 1]

print('Correlation coefficient (SBP):', r_sbp)
print('Correlation coefficient (DBP):', r_dbp)