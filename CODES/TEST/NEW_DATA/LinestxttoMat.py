import numpy as np
from scipy.io import savemat

# Path to your .txt file
file_path = '/Volumes/TIMKA/NEW_CNN/matfiles/lines000000_1.jpeg.txt'

# Read the data from the .txt file into a numpy array
with open(file_path, 'r') as f:
    data_array = np.array([list(map(float, line.split())) for line in f])

# Save the numpy array to a .mat file
savemat('/Volumes/TIMKA/NEW_CNN/matfiles/data.mat', {'data': data_array})
