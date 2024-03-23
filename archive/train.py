import tensorflow as tf
import numpy as np
import random

# Load the model
model = tf.keras.models.load_model('E:/archive/model.h5')

# Perform prediction
# Add your prediction code here
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